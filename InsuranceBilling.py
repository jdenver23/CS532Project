from enum import Enum
from datetime import datetime, timedelta
import calendar
from pathlib import Path
import os
import locale
import csv
from ib_gui import ib_gui


# IB_DB key format:
#   IC: Insurance Carrier
#   IS: Insurance Service
#   II: Insurace Invoice
# IB_DB value:
#   Corresponding field names
IB_DB_DIR = "IB_DB"
IB_DB_FIELDS = {
    "IC": ['Carrier ID', 'Carrier Name', 'Carrier Address', 'Carrier Status', 'Primary Carrier'],
    "IS": ['Service ID', 'Service Description', 'Service Cost', 'Service Date', 'Payment Status'],
    "II": ['Invoice ID', 'Invoice Status', 'Amount Due', 'Patient Info', 'Carrier Info', 'Invoiced Services', 'Date Invoiced', 'Due Date', 'Date Paid', 'Days Overdue'],
}
IB_DB_FIELD_DELIMITER = ","
IB_DB_II_FIELD_DELIMITER = "&"
NONE = ["", "None", None, []]

USER_FILE = 'users.csv'
USER_FIELD = ['ID', 'First Name', 'Last Name', 'Email', 'Password', 'Phone Number', 'Address',
              'Insurance Carrier', 'Date of Birth', 'Gender', 'Primary Care Physician', 'Medication', 'Appointments']
USER_FIELD_DELIMITER = ","

IN_DELIMITER = "+"
OUT_DELIMITER = "="

DATETIME_FORMAT_F = '%Y-%m-%d %H:%M:%S.%f'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%m-%d-%Y'
DATE_TIME_FORMAT = '%m-%d-%Y %H:%M:%S'
DATE_TIME_FORMAT_F = '%m-%d-%Y %H:%M:%S.%f'

# set locale for currency formatting
locale.setlocale(locale.LC_ALL, '')


def to_dollar(amount, grouping=True) -> str:
    """ 
        Convert `amount` into a proper dollar currency format. 

        Examples:
        - `$1000` -> `$1,000.00`
        - `123.1` -> `$123.10`

        Use `grouping = False` to remove `,` for every 3 digits (`$1,000.00` to `$1000.00`).
    """
    if type(amount) is str:
        for r in ["$", ","]:
            amount = amount.replace(r, '')
    return locale.currency(float(amount), grouping=grouping)


def dollar_to_float(amount) -> float:
    for r in ["$", ","]:
        amount = amount.replace(r, '')
    return float(amount)


def date_convert(_date: str, _type="date"):
    if _date in NONE: return ""
    _date = str(_date)
    for format in [DATETIME_FORMAT_F, DATETIME_FORMAT, DATE_FORMAT, DATE_TIME_FORMAT, DATE_TIME_FORMAT_F]:
        try:
            r = datetime.strptime(_date, format)
            if _type == "datetime":
                return r
            elif _type == "str":
                return str(r)
            else:
                return datetime.strftime(r, DATE_FORMAT)
        except:
            pass
    return ""
            


#
#
#   Insurance Classes
#
#


class PaymentStatus(Enum):
    """
        Payments status of an Insurance Carrier, a Service, or an Invoice.\n
        This Enum inherited class was created for better representation of data stored in the database.
    """
    PAID = 0
    UNPAID = 1
    PENDING = 2
    ONTIME = 3
    LATE = 4
    DIFFICULT = 5
    DELINQUENT = 6

    def __eq__(self, other) -> bool:
        return self.value == other.value if type(other) == PaymentStatus else int(other)


class InsuranceCarrier:
    def __init__(self, id, name, address, primary=False) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.status = PaymentStatus.ONTIME
        self.primary = primary
        self.set_repr(self.id)

    def set_repr(self, repr) -> None:
        self.repr = repr

    def as_list(self) -> list[str]:
        return [self.id, self.name, self.address, 'PRIMARY' if self.primary else 'NON-PRIMARY']

    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.name}{delimiter}{self.address}{delimiter}{self.status.name}{delimiter}{'PRIMARY' if self.primary else 'NON-PRIMARY'}"

    def __repr__(self) -> str:
        """
            Set the object representation of this class to its `id` (customizable).
        """
        return self.repr


class InsuranceService:
    def __init__(self, id, description, cost, date: datetime = None) -> None:
        self.id = id
        self.description = description
        self.cost = to_dollar(cost)
        self.set_date(date)
        self.payment_status = PaymentStatus.UNPAID
        self.set_repr(self.id)
        
    def set_date(self, date: datetime or str) -> None:
        self.date = datetime.now() if date is None else date
        if type(date) != datetime:
            for format in [DATETIME_FORMAT_F, DATETIME_FORMAT, DATE_FORMAT, DATE_TIME_FORMAT, DATE_TIME_FORMAT_F]:
                try:
                    self.date = datetime.strptime(str(self.date), format)
                except:
                    pass

    def set_repr(self, repr) -> None:
        self.repr = repr

    def as_list(self) -> list[str]:
        return [self.id, self.description, str(self.date.strftime('%m-%d-%Y')) if self.date is not None else "", self.cost, self.payment_status.name]

    def get_cost(self) -> float:
        """ Return `cost` as a float. """
        return dollar_to_float(self.cost)

    def mark_as_paid(self) -> None:
        self.payment_status = PaymentStatus.PAID

    def mark_as_unpaid(self) -> None:
        self.payment_status = PaymentStatus.UNPAID

    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.description}{delimiter}{self.get_cost()}{delimiter}{self.date}{delimiter}{self.payment_status.name}"

    def __repr__(self) -> str:
        """
            Set the object representation of this class to its `id` (customizable).
        """
        return self.repr


class InsuranceInvoice:
    def __init__(self, id=0, status: PaymentStatus = PaymentStatus.UNPAID, amount_due="$0", patient_info: list[str] = None, carrier_info: list[str] = None, invoiced_services: list[InsuranceService] = None, date_invoiced: datetime = None, date_paid: datetime = None) -> None:
        self.id = id
        self.amount_due = to_dollar(amount_due)

        # info variables
        # [0: name
        #  1: address]
        self.patient_info = patient_info
        self.patient_info_csv = IN_DELIMITER.join(self.patient_info)
        self.carrier_info = carrier_info
        self.carrier_info_csv = IN_DELIMITER.join(carrier_info)

        self.invoiced_services = []
        if invoiced_services not in NONE:
            for service in invoiced_services:
                self.invoiced_services.append(
                    service.as_csv_entry(delimiter=OUT_DELIMITER))

        self.invoiced_services = invoiced_services

        self.status = status
        self.date_invoiced = date_invoiced
        self.due_date = (date_invoiced + timedelta(days=self.get_last_day_of_month(
            date_invoiced.year, date_invoiced.month))) if date_invoiced is not None else None
        self.date_paid = date_paid
        self.days_overdue = 0

    def mark_as_invoiced(self, date_invoiced: datetime = None) -> None:
        """
            Mark today as invoiced date and set due Date to on the same day of next month.
        """
        self.date_invoiced = datetime.now() if date_invoiced is None else date_invoiced
        self.due_date = self.date_invoiced + \
            timedelta(days=self.get_last_day_of_month())

    def mark_as_paid(self, date_paid: datetime = None) -> None:
        """
            Mark today as paid date and set status to `PAID`.
        """
        self.amount_due = to_dollar(0)
        self.status = PaymentStatus.PAID
        self.date_paid = datetime.now() if date_paid is None else date_paid
        self.days_overdue = max(0, (self.date_paid - self.due_date).days)

    def get_last_day_of_month(self, year=None, month=None):
        """
            Return the last day of specified year and month of invoiced date
        """
        if year is not None and month is not None:
            return calendar.monthrange(year, month)[1]
        return calendar.monthrange(self.date_invoiced.year, self.date_invoiced.month)[1]

    def as_list(self) -> list[str]:
        return [self.id, str(self.date_invoiced.strftime('%m/%d/%Y')), str(self.due_date.strftime('%m-%d-%Y')) if self.due_date is not None else "",
                self.amount_due, self.carrier_info[0], self.status.name, str(self.date_paid.strftime('%m-%d-%Y')) if self.date_paid is not None else "", self.days_overdue]

    def as_receipt(self) -> str:
        invoiced_services = ""
        total_cost = 0
        for service in self.invoiced_services:
            total_cost += service.get_cost()
            invoiced_services += f"""\t - ID: {service.id}\
                               \n\t\t + Date: {service.date}\
                               \n\t\t + Description: {service.description}\
                               \n\t\t + Cost: {to_dollar(service.get_cost())}\n"""

        return f"""Invoice ID: {self.id}\
                 \n\tStatus: {self.status.name}\
                 \nPatient's information:\
                 \n\tName: {self.patient_info[0]}\t\t\tAddress: {self.patient_info[1]}\
                 \nCarrier information:\
                 \n\tName: {self.carrier_info[0]}\t\t\tAddress: {self.carrier_info[1]}\
                 \nInvoiced services:\
                 \n{invoiced_services}\
                 \r{"-"*16}\
                 \nAmount due: {self.amount_due}\t\tTotal cost: {to_dollar(total_cost)}""".expandtabs(4)

    def as_csv_entry(self, delimiter=IB_DB_II_FIELD_DELIMITER) -> str:
        invoiced_services_csv = IN_DELIMITER.join(
            s.as_csv_entry() for s in self.invoiced_services)
        return f"{self.id}{delimiter}{self.status.name}{delimiter}{self.amount_due}{delimiter}{self.patient_info_csv}{delimiter}{self.carrier_info_csv}{delimiter}{invoiced_services_csv}{delimiter}{self.date_invoiced}{delimiter}{self.due_date}{delimiter}{self.date_paid}{delimiter}{self.days_overdue}"

    def __repr__(self) -> str:
        return self.id


#
#
#   Main Class
#
#


class InsuranceBilling:
    """
        ### Insurance Billing Class
        Store patients' information of insurance carriers and services provided by the medical clinic.\n
        Generate monthly invoices as well as reports on delinquent invoices made by patient or carrier.

        #### Notes:
        - `id` can mean `user_id` or `patient_id` as it will use this id to retrieve data from other databases.
        - Use `commit_to_db()` in order to save local changes to the database.
    """

    def __init__(self, id: str or int = None) -> None:
        self.id = id
        assert self.id is not None, f"User ID cannot be None."
        assert str(self.id).isnumeric(), f"Invalid user ID format: {self.id}. It should only contain digits 0-9."
        # if id is None:
        #     # generate new id by retrieving all used ids from database folder
        #     used_ids = []
        #     for file in os.listdir(IB_DB_DIR):
        #         if file.endswith(".csv"):
        #             used_id = file.split("_")[0].split("id")[1]
        #             if used_id.isnumeric():
        #                 used_ids.append(int(used_id))

        #     self.id = 0
        #     while any(self.id == used_id for used_id in used_ids):
        #         self.id += 1

        # retrieve data of `id` from the database
        self.retrieve_data()
        self.local_changes_made = False

    def retrieve_data(self) -> None:
        """
            Retrieve data from the database and store them as lists.
            This includes lists of `services` and `carriers`.

            Currently database file names are in this format:
                `id{self.id:08}_services.csv`
                      `__________`  <- front padding so that string length is `8`

        """
        # make sure `IB_DB_DIR` exists
        if not Path(IB_DB_DIR).is_dir():
            os.mkdir(IB_DB_DIR)

        # user database file
        if not Path(USER_FILE).is_file():
            open(USER_FILE, "a").close()

        # retrieve user with self.id from database
        self.user = None
        with open(USER_FILE, 'r') as f:
            for user in csv.DictReader(f, fieldnames=USER_FIELD, delimiter=USER_FIELD_DELIMITER):
                if user['ID'] == str(self.id):
                    self.user = user
                    self.user_name = user['First Name'] + \
                        ' ' + user['Last Name']
                    break

        assert self.user is not None, f"Cannot find specified user ID in database ({self.id})."

        # service database file
        self.__service_db = IB_DB_DIR + f"/id{self.id:0>8}" + "_services.csv"
        if not Path(self.__service_db).is_file():
            open(self.__service_db, "a").close()

        # retrieve service list from db
        self.services = []
        with open(self.__service_db, 'r') as f:
            for service in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_FIELD_DELIMITER):
                r_service = InsuranceService(id=service['Service ID'],
                                             description=service['Service Description'],
                                             cost=service['Service Cost'])

                try:
                    r_service.date = datetime.strptime(service['Service Date'], DATETIME_FORMAT_F)
                except:
                    r_service.date = datetime.strptime(service['Service Date'], '%Y-%m-%d %H:%M:%S')
                r_service.payment_status = PaymentStatus[service['Payment Status']]
                self.services.append(r_service)

        # carrier database file
        self.__carrier_db = IB_DB_DIR + f"/id{self.id:0>8}" + "_carriers.csv"
        if not Path(self.__carrier_db).is_file():
            open(self.__carrier_db, "a").close()

        # retrieve carrier list from db
        self.carriers = []
        with open(self.__carrier_db, 'r') as f:
            for carrier in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_FIELD_DELIMITER):
                r_carrier = InsuranceCarrier(id=carrier['Carrier ID'],
                                             name=carrier['Carrier Name'],
                                             address=carrier['Carrier Address'],
                                             primary=True if carrier['Primary Carrier'] == 'PRIMARY' else False)

                r_carrier.status = PaymentStatus[carrier['Carrier Status']]
                self.carriers.append(r_carrier)

        self.primary_carrier = None
        if len(self.carriers) > 0:
            self.primary_carrier = self.carriers[-1]
            if not self.primary_carrier.primary:
                for carrier in self.carriers:
                    if carrier.primary:
                        self.primary_carrier = carrier
                        break

        # invoice database file
        self.__invoice_db = IB_DB_DIR + f"/id{self.id:0>8}" + "_invoices.csv"
        if not Path(self.__invoice_db).is_file():
            open(self.__invoice_db, "a").close()

        # retrieve invoice list from db
        self.invoices = []

        with open(self.__invoice_db, 'r') as f:
            for invoice in csv.DictReader(f, fieldnames=IB_DB_FIELDS['II'], delimiter=IB_DB_II_FIELD_DELIMITER):
                invoiced_services = []
                if invoice['Invoiced Services'] not in NONE:
                    for service_csv in invoice['Invoiced Services'].split(IN_DELIMITER):
                        service_d = service_csv.split(IB_DB_FIELD_DELIMITER)
                        invoiced_services.append(InsuranceService(id=service_d[0],
                                                                  description=service_d[1],
                                                                  cost=service_d[2],
                                                                  date=datetime.strptime(service_d[3], DATETIME_FORMAT_F)))

                r_invoice = InsuranceInvoice(id=invoice['Invoice ID'],
                                             status=PaymentStatus[invoice['Invoice Status']],
                                             amount_due=invoice['Amount Due'],
                                             patient_info=invoice['Patient Info'].split(
                                                 IN_DELIMITER),
                                             carrier_info=invoice['Carrier Info'].split(
                                                 IN_DELIMITER),
                                             invoiced_services=invoiced_services)

                if invoice['Date Invoiced'] not in NONE:
                    r_invoice.date_invoiced = datetime.strptime(
                        invoice['Date Invoiced'], DATETIME_FORMAT_F)
                if invoice['Date Paid'] not in NONE:
                    r_invoice.date_paid = datetime.strptime(
                        invoice['Date Paid'], DATETIME_FORMAT_F)
                if invoice['Due Date'] not in NONE:
                    r_invoice.due_date = datetime.strptime(
                        invoice['Due Date'], DATETIME_FORMAT_F)
                if r_invoice.due_date not in NONE and r_invoice.date_paid in NONE:
                    r_invoice.days_overdue = datetime.now(
                    ) - r_invoice.due_date if datetime.now() > r_invoice.due_date else 0
                    if r_invoice.days_overdue > 0:
                        r_invoice.status = PaymentStatus.DELINQUENT

                self.invoices.append(r_invoice)

    # ---------------
    #   DATABASE
    # ---------------
    def commit_to_db(self) -> None:
        """
            Commit local changes to the database by rewriting all data to its databases, 
            including `services`, `carriers`, and `invoices`.
        """
        with open(self.__service_db, 'w') as fs, open(self.__carrier_db, 'w') as fc, open(self.__invoice_db, 'w') as fi:
            actions = 0
            for service in self.services:
                if service is not None:
                    fs.write(service.as_csv_entry() + "\n")
                    actions += 1
            for carrier in self.carriers:
                if carrier is not None:
                    fc.write(carrier.as_csv_entry() + "\n")
                    actions += 1
            for invoice in self.invoices:
                if invoice is not None:
                    fi.write(invoice.as_csv_entry() + "\n")
                    actions += 1
            if actions > 0:
                self.local_changes_made = False

    def sort_local_db(self, sort_by_id=False, sort_by_name=False, sort_by_cost=False, reversed=False) -> None:
        """
            Sort the local database according to the argument.\n
            Note: only one `sort_by_[]` can be used at a time.

            #### Parameters:
            - `sort_by_id` sort both `services` and `carriers` lists by its `id`.
            - `sort_by_name` sort only `carriers` list by its `name`.
            - `sort_by_cost` sort only `services` list by its `cost`.
            - `reversed` should lists should be sorted in ascending or descending order.
        """
        if sort_by_id:
            self.services = sorted(self.services, key=lambda x: x.id, reverse=reversed)
            self.carriers = sorted(self.carriers, key=lambda x: x.id, reverse=reversed)
            self.local_changes_made = True
        elif sort_by_name:
            self.carriers = sorted(self.carriers, key=lambda x: x.name, reverse=reversed)
            self.local_changes_made = True
        elif sort_by_cost:
            self.services = sorted(self.services, key=lambda x: x.cost, reverse=reversed)
            self.local_changes_made = True

    # ---------------
    #   CARRIERS
    # ---------------
    def new_carrier(self, carrier_name, carrier_address, primary=False) -> str:
        """ 
            Add a row of new Insurance Carrier to the local database.\n
            If `primary` is `True`, set all other carriers' `primary` key to `False`.\n
            Note: use `commit_to_db()` in order to save local changes to the database.

            #### Parameters:
            - `carrier_name` name of the carrier.
            - `carrier_address` address of the carrier.
            - `service_description` description of the new carrier.
            - `primary` is this a primary insurance?

            #### Returns: 
            - a new `InsuranceService` instance.
        """
        carrier_id = "0"

        while any(carrier.id == carrier_id for carrier in self.carriers if carrier is not None):
            carrier_id = str(int(carrier_id) + 1)

        has_primary = False
        for carrier in self.carriers:
            if carrier is not None and carrier.primary:
                has_primary = True
                break

        # mark insurance carrier as primary if there isnt one yet
        if not has_primary:
            primary = True

        if primary:
            # set all other carriers' primary to False in local list
            for carrier in self.carriers:
                if carrier is not None and carrier.primary:
                    carrier.primary = False

        n_carrier = InsuranceCarrier(
            id=carrier_id, name=carrier_name, address=carrier_address, primary=primary)
        # add carrier to local list
        self.carriers.append(n_carrier)
        self.local_changes_made = True

        return n_carrier

    def remove_carrier(self, carrier_id) -> bool:
        """ 
            Remove the row of where `carrier_id` is found in the local database.

            If the to-be removed carrier has its `primary` key as `True`, 
            then the most recent `carrier_id` will be selected to be the 
            primary Carrier for this insurance bill.

            Note: use `commit_to_db()` in order to save local changes to the database.

            #### Parameters:
            - `carrier_id` to find in database.

            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        carrier_id = str(carrier_id)
        for carrier in self.carriers:
            if carrier is not None and carrier.id == carrier_id:
                # mark the most recent carrier as primary if a primary Carrier is being removed
                if carrier.primary:
                    self.carriers[-1].primary = True
                self.carriers.remove(carrier)
                self.local_changes_made = True
                return True

        return False

    def get_carrier(self, carrier_id) -> InsuranceCarrier:
        """ Return the instance of `InsuranceCarrier` that has the same `carrier_id`. """
        carrier_id = str(carrier_id)
        for carrier in self.carriers:
            if carrier is not None and carrier.id == carrier_id:
                return carrier
        return None
    
    def edit_carrier(self, carrier_id, to_carrier: InsuranceCarrier) -> bool:
        """ Replace an instance of `InsuranceCarrier` with a new `InsuranceCarrier`. """
        carrier_id = str(carrier_id)
        for i in range(len(self.carriers)):
            if self.carriers[i] is not None and self.carriers[i].id == carrier_id:
                self.carriers[i] = to_carrier
                return True
        return False
    
    def edit_carrier(self, carrier_id, n_name=None, n_address=None, n_primary: bool=None) -> bool:
        """ Replace an instance of `InsuranceCarrier` with specified options. """
        carrier_id = str(carrier_id)
        for i in range(len(self.carriers)):
            if self.carriers[i] is not None and self.carriers[i].id == carrier_id:
                if n_name not in NONE: self.carriers[i].name = n_name
                if n_address not in NONE: self.carriers[i].address = n_address
                if n_primary not in NONE: self.carriers[i].n_primary = n_primary
                return True
        return False

    def set_primary(self, carrier_id, primary=True) -> bool:
        """ Set a carrier primary status. Return `False` if `carrier_id` is not found. """
        for carrier in self.carriers:
            if carrier is not None and carrier.id == carrier_id:
                for all_carrier in self.carriers:
                    if all_carrier is not None:
                        all_carrier.primary = not primary
                carrier.primary = primary
                self.local_changes_made = True
                return True
        return False

    # ---------------
    #   SERVICES
    # ---------------
    def new_service(self, service_description, service_cost, date=datetime.now(), fillin_id=True) -> str:
        """ 
            Add a row of new Service to the local database.\n
            Note: use `commit_to_db()` in order to save local changes to the database.

            #### Parameters:
            - `service_description` description of the new service.
            - `service_cost` cost of the new service (format: `$___`).
            - `fillin_id` indicates if the new service id should be higher than the most recent one.

            #### Returns: 
            - a new `InsuranceService` instance.
        """
        service_id = "0" if fillin_id else max(
            self.services, key=lambda x: x.id).id
        while any(service.id == service_id for service in self.services if service is not None):
            service_id = str(int(service_id) + 1)

        n_service = InsuranceService(
            id=service_id, description=service_description, cost=service_cost, date=date)

        # add service to local list
        self.services.append(n_service)
        self.local_changes_made = True

        return n_service

    def remove_service(self, service_id) -> bool:
        """ 
            Remove the row of where `service_id` is found in the local database.\n
            Note: use `commit_to_db()` in order to save local changes to the database.

            #### Parameters:
            - `service_id` to find in database.

            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        service_id = str(service_id)
        for service in self.services:
            if service is not None and service.id == service_id:
                self.services.remove(service)
                self.local_changes_made = True
                return True

        return False

    def get_service(self, service_id) -> InsuranceService:
        service_id = str(service_id)
        """ Return the instance of `InsuranceService` that has the same `service_id`. """
        for service in self.services:
            if service is not None and service.id == service_id:
                return service
        return None
    
    def edit_service(self, service_id, to_service: InsuranceService) -> bool:
        """ Replace an instance of `InsuranceService` with a new `InsuranceService`. """
        service_id = str(service_id)
        for i in range(len(self.services)):
            if self.services[i] is not None and self.services[i].id == service_id:
                self.services[i] = to_service
                return True
        return False
    
    def edit_service(self, service_id, n_description=None, n_cost=None, n_date=None) -> bool:
        """ Replace an instance of `InsuranceService` with a new `InsuranceService`. """
        service_id = str(service_id)
        for i in range(len(self.services)):
            if self.services[i] is not None and self.services[i].id == service_id:
                if n_description not in NONE: self.services[i].description = n_description
                if n_cost not in NONE: self.services[i].cost = n_cost
                if n_date not in NONE: self.services[i].set_date(n_date)
                return True
        return False

    # ---------------
    #   INVOICES
    # ---------------
    def generate_invoice(self, month=None) -> str:
        """ 
            Generate invoice from this **current** billing cycle (customizable through
            `month=` argument) then append it to local invoice list.

            Billing cycles typically start from the end of the month 
            (on the 30th or 31st) until the next month.

            Note: to retrieve invoice info, use `invoice_info()`. 

            #### Parameters:
            - `month` to specify a month to collect unpaid services.
            Leave as `None` for the current month.

            #### Returns:
            - `InsuranceInvoice` instance.
            - `-1` if all services are paid or no services found.
        """
        patient_info = [self.user['First Name'] + ' ' +
                        self.user['Last Name'], self.user['Address']]
        carrier_info = [self.carriers[-1].name, self.carriers[-1].address]
        if not self.carriers[-1].primary:
            for carrier in self.carriers:
                if carrier is not None and carrier.primary:
                    self.primary_carrier = carrier
                    carrier_info = [carrier.name, carrier.address]
                    break

        invoiced_services = []
        total_cost = 0
        if month is None:
            month = datetime.now().month

        for service in self.services:
            if service is not None and service.date.month == month:
                if service.payment_status is PaymentStatus.UNPAID:
                    last_day_of_month = calendar.monthrange(
                        service.date.year, month)[1]
                    if service.date.day <= last_day_of_month:
                        total_cost += service.get_cost()
                        invoiced_services.append(service)

        if not invoiced_services or not self.services:
            return '-1'

        invoice_id = "0"
        while any(invoice.id == invoice_id for invoice in self.invoices if invoice is not None):
            invoice_id = str(int(invoice_id) + 1)

        n_invoice = InsuranceInvoice(id=invoice_id, amount_due=total_cost, patient_info=patient_info, carrier_info=carrier_info,
                                     invoiced_services=invoiced_services)
        n_invoice.mark_as_invoiced()

        # add invoice to local list
        self.invoices.append(n_invoice)
        self.local_changes_made = True

        return n_invoice

    def remove_invoice(self, invoice_id) -> bool:
        """ 
            Remove the row of where `invoice_id` is found in the local database.\n
            Note: use `commit_to_db()` in order to save local changes to the database.

            #### Parameters:
            - `invoice_id` to find in database.

            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        invoice_id = str(invoice_id)
        for invoice in self.invoices:
            if invoice is not None and invoice.id == invoice_id:
                self.invoices.remove(invoice)
                self.local_changes_made = True
                return True

        return False

    def invoice_info(self, invoice_id=None) -> str:
        """ 
            Return invoice as string. Format as below:

            Invoice ID: `id`
            \tStatus: `status`
            Patient's information:
            \tName: `name`\t\t\tAddress: `address`
            Carrier information:
            \tName: `name`\t\t\tAddress: `address`
            Invoiced services:\n
            \t \- ID: `id`
            \t\t + Date: `date`
            \t\t + Description: `description`
            \t\t + Cost: `cost`
            \----------------\n
            Amount due: `amt`\t\tTotal cost: `cost`

            :func:`InsuranceBilling`
        """
        if invoice_id is None and len(self.invoices) > 0:
            invoice_id = self.invoices[-1].id
        invoice_id = str(invoice_id)

        for invoice in self.invoices:
            if invoice is not None and invoice.id == invoice_id:
                return invoice.as_receipt()

        return ""

    def pay_for_invoice(self, invoice_id, amount="$0", pay_in_full=False) -> bool:
        """
            Make a payment to `invoice_id` with specified `amount`.

            #### Parameters:
            - `invoice_id` to find in database.
            - `amount` to pay the invoice.
            - `pay_in_full` set to `True` to pay the invoice in full.

            #### Returns:
            - `True` if payment was successful.
            - `False` otherwise.
        """
        amount = float(amount.replace("$", ''))
        if amount <= 0 and not pay_in_full:
            return False

        invoice_id = str(invoice_id)
        for invoice in self.invoices:
            if invoice is not None and invoice.id == invoice_id:
                diff = float(invoice.amount_due.replace("$", '')) - amount
                if diff <= 0 or pay_in_full:
                    invoice.mark_as_paid()
                    for invoiced_service in invoice.invoiced_services:
                        invoiced_service.mark_as_paid()
                        self.services[int(invoiced_service.id)].mark_as_paid()
                else:
                    invoice.status = PaymentStatus.PENDING
                    invoice.amount_due = to_dollar(diff)

                carrier = self.carriers[-1]
                for _carrier in self.carriers:
                    if _carrier is not None and _carrier.primary:
                        carrier = _carrier
                if datetime.now() - invoice.due_date > timedelta(days=15):
                    carrier.status = PaymentStatus.DIFFICULT
                elif datetime.now() - invoice.due_date > timedelta(days=0):
                    carrier.status = PaymentStatus.LATE
                else:
                    carrier.status = PaymentStatus.ONTIME
                self.local_changes_made = True
                return True

        return False

    # ---------------
    #   REPORTS
    # ---------------
    def generate_report(self, patient_name=None, carrier: InsuranceCarrier = None, carrier_name=None, carrier_address=None) -> str:
        """ 
            Generate reports of delinquent invoices either by `patient_name` or `carrier`.

            #### Parameters:
            - `patient_name` to find in database.
            - `carrier` to find in database.
            - `carrier_name` is used when `carrier` is not provided.
            - `carrier_address` is used when `carrier` is not provided.

            #### Returns:
            - delinquent reports as a string.
        """
        delinquent_reports = ""
        for invoice in self.invoices:
            if invoice is not None and invoice.status is PaymentStatus.DELINQUENT:
                if patient_name is not None:
                    if invoice.patient_info[0] == patient_name:
                        delinquent_reports += self.invoice_info(
                            invoice.id) + "\n"
                else:
                    if invoice.carrier_info == [carrier.name, carrier.address]:
                        delinquent_reports += self.invoice_info(
                            invoice.id) + "\n"

        return delinquent_reports


def init_gui(uid: str or int):
    insurance_bill = InsuranceBilling(id=uid)
    app = ib_gui.MainGUI(bill=insurance_bill)
    app.run()


#
#
#   Test/Debug Section
#
#


def __service_tests__(bill: InsuranceBilling):
    print(bill.services)
    if bill.remove_service(1):
        print("<<< removed service with id = 1")
        print(bill.services)

    print(">>> add new service: labs with the cost of $627 id =",
          bill.new_service('labs', '$627', date=datetime(2011, 12, 2)))
    print(bill.services)
    print(">>> add new service: vaccines with the cost of $288 id =",
          bill.new_service('vaccines', '$288'))
    print(bill.services)
    if bill.remove_service(1):
        print("<<< removed service with id = 1")
        print(bill.services)
    print(">>> add new service: medicines with the cost of $141 id =",
          bill.new_service('medicines', '$141'))
    print(bill.services)


def __carrier_tests__(bill: InsuranceBilling):
    print()
    print(bill.carriers)
    print(">>> add new carrier: PRIMARY Medical @111 1st st id =",
          bill.new_carrier('Medical', '111 1st st', primary=True))
    print(bill.carriers)
    print(">>> add new carrier: PRIMARY Care @222 2nd st id =",
          bill.new_carrier('Care', '222 2nd st', primary=True))
    print(bill.carriers)

    if bill.remove_carrier(0):
        print("<<< removed carrier with id = 0")
        print(bill.carriers)

    print(">>> add new carrier: non-primary SupCare @333 3rd st with id =",
          bill.new_carrier('SupCare', '333 3rd st', primary=False))
    print(bill.carriers)


def __invoice_tests__(bill: InsuranceBilling, month=datetime.now().month, pay=True, deq=False):
    print()
    if len(bill.carriers) == 0:
        bill.new_carrier("kaiser", '@home', primary=True)

    print(">>> list of invoices:", bill.invoices)
    id = bill.generate_invoice(month=month)
    if id != "-1":
        print(">>> new invoice with id =", id)
        print(">>> new list of invoices:", bill.invoices)
        print(bill.invoice_info(id) or None)
        print()
        print(">>> last invoiced service:")
        print(bill.invoices[-1].invoiced_services[-1] or None)

        bill.commit_to_db()
        if pay:
            print()
            print(">>> paying invoice id =",
                  bill.invoices[-1].id, "in full amount...", end=' ')
            time.sleep(0.7)
            bill.pay_for_invoice(bill.invoices[-1].id, pay_in_full=True)
            print(bill.invoices[-1].status.name + '!!')
            time.sleep(0.4)

            # delinquent test
            if deq:
                print(">> setting new primary carrier:".expandtabs(
                    4), bill.set_primary(bill.carriers[-1].id))
                print('', "-"*32, "\n>>> START delinquent test...\n", "-"*32, end='')
                bill.new_service('deqlin', '$1234.56')
                time.sleep(0.3)
                __invoice_tests__(bill, pay=False)
                bill.invoices[-1].status = PaymentStatus.DELINQUENT
                print('', "-"*32, "\n>>> END delinquent test...\n", "-"*32)
                time.sleep(0.1)
    else:
        print("\n>>> INVOICE INFO:")
        print(bill.invoice_info() or None)

    time.sleep(0.3)
    print("\n>>> delinquent invoices by patient name:", bill.user_name)
    print(bill.generate_report(patient_name=bill.user_name) or None)

    time.sleep(0.1)
    print(">>> delinquent invoices by carrier name:", bill.carriers[-2].name)
    print(bill.generate_report(carrier=bill.carriers[-2]) or None)


def __clean_up__():
    count = 0
    if Path(IB_DB_DIR + '\ib-test-users.csv').is_file():
        count += 1
        os.remove(IB_DB_DIR + '\ib-test-users.csv')

    # remove used csv files in `IB_DB_DIR` directory
    if Path(IB_DB_DIR).is_dir():
        for file in os.listdir(IB_DB_DIR):
            if file.endswith(".csv") and f"id{uid:08}_" in file:
                os.remove(IB_DB_DIR + "/" + file)
                count += 1
    return count


def __run_gui__(bill: InsuranceBilling) -> None:
    app = ib_gui.MainGUI(bill=bill)
    app.run()


def __run_tests__(bill: InsuranceBilling) -> None:
    __service_tests__(bill)  # service tests
    bill.commit_to_db()
    __carrier_tests__(bill)  # carrier tests
    bill.commit_to_db()
    __invoice_tests__(bill, pay=True, deq=True)  # invoice tests
    bill.commit_to_db()

    print(f"\n{bcolors.BOLD + bcolors.OKGREEN}All tests completed!{bcolors.ENDC}")
    try:
        for sec in range(5, 0, -1):
            print(f"Cleaning up after {sec}s...", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print(
            f"Cleaning up after {sec}s... {bcolors.FAIL}cancelled.{bcolors.ENDC}")
        exit(0)

    print(
        f"Cleaning up after 0s... {bcolors.BOLD}removed {__clean_up__()} test files!{bcolors.ENDC}")


def __test_init__():
    global test_uid
    global USER_FILE

    test_uid = 1111
    USER_FILE = IB_DB_DIR + '\ib-test-users.csv'
    __clean_up__()
    if not Path(IB_DB_DIR).is_dir():
        os.mkdir(IB_DB_DIR)
    with open(USER_FILE, mode='w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([test_uid, "TRI", "TRAN", "tree@test.com", "123456",
                        "1234567890", "123@4th Ave", "CS 532", "11/11/1111", "Male"])
    bill = InsuranceBilling(test_uid)
    # bill.new_carrier('Medical', '111 1st st', primary=True)
    # bill.new_carrier('Care', '222 2nd st', primary=True)
    # bill.new_carrier('SupCare', '333 3rd st', primary=False)
    # bill.commit_to_db()

    __service_tests__(bill)  # service tests
    bill.commit_to_db()
    __carrier_tests__(bill)  # carrier tests
    bill.commit_to_db()
    bill.generate_invoice()
    bill.commit_to_db()

    return bill


if __name__ == "__main__":
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    # only import time package for testing
    import time

    uid = 1111
    bill = __test_init__()
    backend_tests = False

    __run_gui__(bill)

    if backend_tests:
        try:
            for sec in range(3, 0, -1):
                print(f"Running backend tests after {sec}s...", end='\r')
                time.sleep(1)
        except KeyboardInterrupt:
            print(
                f"Running backend tests after {sec}s... {bcolors.FAIL}cancelled.{bcolors.ENDC}")
            exit(0)

        print(f"\n{bcolors.BOLD}Running backend tests...{bcolors.ENDC}")
        __run_tests__(bill=bill)
    else:
        __clean_up__()
