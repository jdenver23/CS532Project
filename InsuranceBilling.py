from enum import Enum
from datetime import datetime, timedelta
import calendar
from pathlib import Path
import os
import locale
import csv
import tkinter as tk
from tkinter import messagebox


# IB_DB key format:
#   IC: Insurance Carrier
#   IS: Insurance Service
#   II: Insurace Invoice
# IB_DB value:
#   Corresponding field names
IB_DB_DIR = "IB_DB"
IB_DB_FIELDS = {
    "IC": ['Insurance Carrier ID', 'Insurance Carrier name', 'Insurance Carrier Address', 'Insurance Carrier Status', 'Primary Carrier'],
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

    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.name}{delimiter}{self.address}{delimiter}{self.status.name}{delimiter}{'PRIMARY' if self.primary else 'NON-PRIMARY'}"

    def __str__(self) -> str:
        return f"""'Insurance Carrier ID': {self.id}\
                    \n'Insurance Carrier name': {self.name}\
                    \n'Insurance Carrier Address': {self.address}\
                    \n'Insurance Carrier Status': {self.status.name}\
                    \n'Primary Carrier': {'PRIMARY' if self.primary else 'NON-PRIMARY'}\
                """

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
        self.date = datetime.now() if date is None else date
        self.payment_status = PaymentStatus.UNPAID
        self.set_repr(self.id)

    def set_repr(self, repr) -> None:
        self.repr = repr

    def get_cost(self) -> float:
        """ Return `cost` as a float. """
        return dollar_to_float(self.cost)

    def mark_as_paid(self) -> None:
        self.payment_status = PaymentStatus.PAID

    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.description}{delimiter}{self.get_cost()}{delimiter}{self.date}{delimiter}{self.payment_status.name}"

    def __str__(self) -> str:
        return f"""'Service ID': {self.id}\
                   \n'Service Description': {self.description}\
                   \n'Service Cost': {to_dollar(self.cost)}\
                   \n'Service Date': {self.date}\
                   \n'Payment Status': {self.payment_status.name}\
                """

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

    def __init__(self, id=None) -> None:
        self.id = id
        assert self.id is not None
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
                    self.user_name = user['First Name'] + ' ' + user['Last Name']
                    break

        assert self.user is not None, f"Cannot find specified user ID in database ({self.id})."

        # service database file
        self.__service_db = IB_DB_DIR + f"/id{self.id:08}" + "_services.csv"
        if not Path(self.__service_db).is_file():
            open(self.__service_db, "a").close()

        # retrieve service list from db
        self.services = []
        with open(self.__service_db, 'r') as f:
            for service in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_FIELD_DELIMITER):
                r_service = InsuranceService(id=service['Service ID'],
                                             description=service['Service Description'],
                                             cost=service['Service Cost'])

                r_service.date = datetime.strptime(service['Service Date'], '%Y-%m-%d %H:%M:%S.%f')
                r_service.payment_status = PaymentStatus[service['Payment Status']]
                self.services.append(r_service)

        # carrier database file
        self.__carrier_db = IB_DB_DIR + f"/id{self.id:08}" + "_carriers.csv"
        if not Path(self.__carrier_db).is_file():
            open(self.__carrier_db, "a").close()

        # retrieve carrier list from db
        self.carriers = []
        with open(self.__carrier_db, 'r') as f:
            for carrier in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_FIELD_DELIMITER):
                r_carrier = InsuranceCarrier(id=carrier['Insurance Carrier ID'],
                                             name=carrier['Insurance Carrier name'],
                                             address=carrier['Insurance Carrier Address'],
                                             primary=True if carrier['Primary Carrier'] == 'PRIMARY' else False)

                r_carrier.status = PaymentStatus[carrier['Insurance Carrier Status']]
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
        self.__invoice_db = IB_DB_DIR + f"/id{self.id:08}" + "_invoices.csv"
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
                                                                  date=datetime.strptime(service_d[3], '%Y-%m-%d %H:%M:%S.%f')))

                r_invoice = InsuranceInvoice(id=invoice['Invoice ID'],
                                             status=PaymentStatus[invoice['Invoice Status']],
                                             amount_due=invoice['Amount Due'],
                                             patient_info=invoice['Patient Info'].split(IN_DELIMITER),
                                             carrier_info=invoice['Carrier Info'].split(IN_DELIMITER),
                                             invoiced_services=invoiced_services)

                if invoice['Date Invoiced'] not in NONE:
                    r_invoice.date_invoiced = datetime.strptime(invoice['Date Invoiced'], '%Y-%m-%d %H:%M:%S.%f')
                if invoice['Date Paid'] not in NONE:
                    r_invoice.date_paid = datetime.strptime(invoice['Date Paid'], '%Y-%m-%d %H:%M:%S.%f')
                if invoice['Due Date'] not in NONE:
                    r_invoice.due_date = datetime.strptime(invoice['Due Date'], '%Y-%m-%d %H:%M:%S.%f')
                if r_invoice.due_date not in NONE and r_invoice.date_paid in NONE:
                    r_invoice.days_overdue = datetime.now() - r_invoice.due_date if datetime.now() > r_invoice.due_date else 0
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
            if actions > 0: self.local_changes_made = False

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
            - a new and unique `service_id`.
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

        n_carrier = InsuranceCarrier(id=carrier_id, name=carrier_name, address=carrier_address, primary=primary)
        # add carrier to local list
        self.carriers.append(n_carrier)
        self.local_changes_made = True

        return carrier_id

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
            - a new and unique `service_id`.
        """
        service_id = "0" if fillin_id else max(
            self.services, key=lambda x: x.id).id
        while any(service.id == service_id for service in self.services if service is not None):
            service_id = str(int(service_id) + 1)

        n_service = InsuranceService(id=service_id, description=service_description, cost=service_cost, date=date)

        # add service to local list
        self.services.append(n_service)
        self.local_changes_made = True

        return service_id

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
            - `invoice_id`.
            - `-1` if all services are paid or no services found.
        """
        patient_info = [self.user['First Name'] + ' ' + self.user['Last Name'], self.user['Address']]
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
                    last_day_of_month = calendar.monthrange(service.date.year, month)[1]
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

        return invoice_id

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
                        delinquent_reports += self.invoice_info(invoice.id) + "\n"
                else:
                    if invoice.carrier_info == [carrier.name, carrier.address]:
                        delinquent_reports += self.invoice_info(invoice.id) + "\n"

        return delinquent_reports


#
#
#   GUI Section
#
#
MAIN_FONT = ('Verdana', 14)
MAIN_BG = 'grey'
BTN_COLOR = '#2980b9'

# TODO: this :3
class IBGUI:
    def __init__(self, bill: InsuranceBilling, root=None):
        self.bill = bill
        self.root = root
        self.gui_w = 600
        self.gui_h = 600
        # build ui
        self.ib_gui = tk.Frame(root)
        self.ib_gui.configure(
            background="grey",
            borderwidth=0,
            height=self.gui_h,
            width=self.gui_w)
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width/2) - (self.gui_w/2)
        y = (screen_height/2) - (self.gui_h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.gui_w, self.gui_h, x, y))
        
        self.user_info_container = tk.LabelFrame(self.ib_gui)
        self.user_info_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=50,
            text='Info',
            width=580)
        self.lb_user_id = tk.Label(self.user_info_container)
        self.lb_user_id.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='ID:')
        self.lb_user_id.pack(
            anchor="center",
            expand="false",
            padx=10,
            side="left")
        self.lb_user_name = tk.Label(self.user_info_container)
        self.lb_user_name.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='Name:')
        self.lb_user_name.pack(
            anchor="center",
            expand="false",
            padx=80,
            side="left")
        self.lb_user_address = tk.Label(self.user_info_container)
        self.lb_user_address.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='Address:')
        self.lb_user_address.pack(
            anchor="center",
            expand="false",
            padx=50,
            side="left")
        self.lb_user_dob = tk.Label(self.user_info_container)
        self.lb_user_dob.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='DOB:')
        self.lb_user_dob.pack(
            anchor="center",
            expand="false",
            padx=60,
            side="left")
        self.user_info_container.grid(
            column=0, padx=10, pady=10, row=0, sticky="nw")
        self.user_info_container.pack_propagate(0)
        
        self.carrier_container = tk.LabelFrame(self.ib_gui)
        self.carrier_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Carrier',
            width=550)
        
        self.fr_carrier_info = tk.Frame(self.carrier_container)
        self.fr_carrier_info.configure(
            background="grey", height=200, width=200)
        self.fr_carrier_info.grid(column=0, ipadx=10, row=0)
        self.fr_carrier_info.grid_anchor("center")
        
        self.generate_carrier_info()
        
        self.carrier_container.grid(column=0, row=1)
        self.carrier_container.grid_propagate(0)
        self.carrier_container.grid_anchor("n")
        self.service_container = tk.LabelFrame(self.ib_gui)
        self.service_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Service',
            width=500)
        self.service_container.grid(column=0, row=2)
        self.invoice_container = tk.LabelFrame(self.ib_gui)
        self.invoice_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Invoice',
            width=500)
        self.invoice_container.grid(column=0, row=3)
        self.fr_gui_control = tk.Frame(self.ib_gui)
        self.fr_gui_control.configure(background="grey", height=50, width=500)
        self.btn_back_to_home = tk.Button(self.fr_gui_control)
        self.btn_back_to_home.configure(
            background="#2980b9",
            font="{Verdana} 12 {}",
            foreground="white",
            highlightbackground="black",
            highlightcolor="blue",
            relief="flat",
            text='⬅ Home',
            command=lambda: self.on_closing())
        self.btn_back_to_home.grid(column=0, padx=20, pady=10, row=0)
        self.btn_save_changes = tk.Button(self.fr_gui_control)
        self.btn_save_changes.configure(
            background="#2980b9",
            font="{Verdana} 12 {}",
            foreground="white",
            relief="flat",
            takefocus=True,
            text='Save Changes ✓',
            command=lambda: self.save_changes())
        self.btn_save_changes.grid(column=1, padx=20, pady=10, row=0)
        self.fr_gui_control.grid(column=0, pady=15, row=4)
        self.ib_gui.pack(side="top")
        self.ib_gui.grid_propagate(0)

        # Main widget
        self.mainwindow = self.ib_gui
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.local_changes_made = False

    def run(self):
        self.mainwindow.mainloop()

    def generate_carrier_info(self):
        carrier_field_names = ["Name", "Address", "Primary"]
        for i in range(3):
            lb_carrier_fields = tk.Label(self.fr_carrier_info)
            lb_carrier_fields.configure(
                background="grey",
                font="{Verdana} 8 {}",
                justify="center",
                text=f'{carrier_field_names[i]}')
            lb_carrier_fields.grid(column=i, padx=48, row=0)
            
        lb_carrier_fields = tk.Label(self.fr_carrier_info)
        lb_carrier_fields.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="center",
            text='Action')
        lb_carrier_fields.grid(column=4, padx=2, row=0)
        
        self.fr_carrier_list = []
        for r in range(len(self.bill.carriers)):
            fr_carrier_list_item = tk.Frame(self.carrier_container)
            fr_carrier_list_item.configure(background="grey", height=50, width=550)
            fr_carrier_list_item.grid(column=0, row=r+1)
            fr_carrier_list_item.grid_anchor("center")
            for c in range(3):
                # create carrier info using multiple entries on the same row
                entry_carrier_info = tk.Entry(fr_carrier_list_item)
                entry_carrier_info.configure(
                    font="{Verdana} 8 {}",
                    justify="center",
                    state="readonly")
                _text_ = ""
                if c == 0: _text_ = f'{self.bill.carriers[r].name}'
                if c == 1: _text_ = f'{self.bill.carriers[r].address}'
                if c == 2: _text_ = f'{"PRIMARY" if self.bill.carriers[r].primary else "NON-PRIMARY"}'
                entry_carrier_info["state"] = "normal"
                entry_carrier_info.delete("0", "end")
                entry_carrier_info.insert("0", _text_)
                entry_carrier_info["state"] = "readonly"
                entry_carrier_info.grid(column=c, row=r, padx=1)
            
            # create carrier remove btns
            btn_remove_carrier = tk.Button(fr_carrier_list_item)
            btn_remove_carrier.configure(
                activeforeground="red",
                font="{Verdana} 7 {}",
                height=1,
                justify="center",
                text='X',
                width=1)
            btn_remove_carrier.grid(column=c+1, row=r, padx=10, ipadx=5)
            btn_remove_carrier.configure(command=lambda idx=r: self.remove_carrier(idx))
            self.fr_carrier_list.append(fr_carrier_list_item)
        
    def remove_carrier(self, idx):
        self.fr_carrier_list[idx].destroy()
        self.bill.carriers[idx] = None
        self.local_changes_made = True

    def save_changes(self):
        self.bill.commit_to_db()
        self.local_changes_made = False
        print("changes saved to database")
    
    def on_closing(self):
        if self.bill.local_changes_made or self.local_changes_made:
            if messagebox.askokcancel("Quit", "You have unsaved changes. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

#
#
#   Test/Debug Section
#
#


def __service_tests__(bill):
    print(bill.services)
    if bill.remove_service(1):
        print("<<< removed service with id = 1")
        print(bill.services)

    print(">>> add new service: labs with the cost of $627 id =",
          bill.new_service('labs', '$627'))
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


def __carrier_tests__(bill):
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


def __invoice_tests__(bill, month=datetime.now().month, pay=True, deq=False):
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


def __run_gui__(bill) -> None:
    root = tk.Tk()
    app = IBGUI(bill=bill, root=root)
    app.run()


def __run_tests__(bill) -> None:

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
        print(f"Cleaning up after {sec}s... {bcolors.FAIL}cancelled.{bcolors.ENDC}")
        exit(0)

    print(f"Cleaning up after 0s... {bcolors.BOLD}removed {__clean_up__()} test files!{bcolors.ENDC}")


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
    USER_FILE = IB_DB_DIR + '\ib-test-users.csv'
    __clean_up__()
    with open(USER_FILE, mode='w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([uid, "TRI", "TRAN", "tree@test.com", "123456",
                        "1234567890", "123@4th Ave", "CS 532", "11/11/1111", "Male"])
    bill = InsuranceBilling(uid)
    bill.new_carrier('Medical', '111 1st st', primary=True)
    bill.new_carrier('Care', '222 2nd st', primary=True)
    bill.new_carrier('SupCare', '333 3rd st', primary=False)
    bill.commit_to_db()
    
    __run_gui__(bill)
    
    try:
        for sec in range(3, 0, -1):
            print(f"Running backend tests after {sec}s...", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Running backend tests after {sec}s... {bcolors.FAIL}cancelled.{bcolors.ENDC}")
        exit(0)
        
    print(f"\n{bcolors.BOLD}Running backend tests...{bcolors.ENDC}")
    __run_tests__(bill=bill)
