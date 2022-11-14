from enum import Enum
from pathlib import Path
import os
import csv
from datetime import datetime, timedelta
import calendar
import locale
import time


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
    "II": ['Invoice ID', 'Invoice Status', 'Amount Due', 'Patient Info', 'Carrier Info', 'Unpaid Services', 'Date Invoiced', 'Due Date', 'Date Paid', 'Days Overdue'],
}
IB_DB_FIELD_DELIMITER = ","
NONE = ["", "None", None, []]

USER_FILE = 'users.csv'
USER_FIELD = ['ID', 'First Name', 'Last Name', 'Email', 'Password', 'Phone Number', 'Address', 'Insurance Carrier', 'Date of Birth', 'Gender', 'Primary Care Physician', 'Medication', 'Appointments']
USER_FIELD_DELIMITER = ","

IN_DELIMITER = "+"
OUT_DELIMITER = "="

# set locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

def to_dollar(amount, grouping=True) -> str:
    if type(amount) is str:
        for r in ["$", ","]:
            amount = amount.replace(r, '')
    return locale.currency(float(amount), grouping)

#
#
#   Insurance Classes
#
#
class PaymentStatus(Enum):
    """
        Payments status of an Insurance Carrier, a Service, or an Invoice.
        
        This Enum inherited class was created for better representation of data stored in the database.
        
        #### Available enums:
        - `PAID`
        - `UNPAID`
        - `ONTIME`
        - `LATE`
        - `DIFFICULT`
        - `DELINQUENT`
    """ 
    PAID = 0
    UNPAID = 1
    PENDING = 2
    ONTIME = 3
    LATE = 4
    DIFFICULT = 5
    DELINQUENT = 6
    
    def __eq__(self, other) -> bool:
        return str(self.value) == (other if other.__class__ == str else str(other))
    
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
    def __init__(self, id, description, cost, date: datetime=None) -> None:
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
        return self.cost if type(self.cost) == float else float(self.cost.split("$")[1])
            
    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.description}{delimiter}{self.cost}{delimiter}{self.date}{delimiter}{self.payment_status.name}"
    
    def __str__(self) -> str:
        return f"""'Service ID': {self.id}\
                   \n'Service Description': {self.description}\
                   \n'Service Cost': {to_dollar(self.cost)}\
                   \n'Service Date': {self.date}\
                   \n'Payment Status': {self.payment_status}\
                """
    
    def __repr__(self) -> str:
        """
            Set the object representation of this class to its `id` (customizable).
        """
        return self.repr


class InsuranceInvoice:
    def __init__(self, id=0, status: PaymentStatus=PaymentStatus.UNPAID, amount_due="$0", patient_info: list[str]=None, carrier_info: list[str]=None, unpaid_services: list[InsuranceService]=None, date_invoiced: datetime = None, date_paid: datetime = None) -> None:
        self.id = id
        self.amount_due = to_dollar(amount_due)

        # info variables
        # [0: name
        #  1: address]
        self.patient_info = patient_info
        self.patient_info_csv = IN_DELIMITER.join(self.patient_info)
        self.carrier_info = carrier_info
        self.carrier_info_csv = IN_DELIMITER.join(carrier_info)
        
        self.unpaid_services = []
        if unpaid_services not in NONE:
            for service in unpaid_services:
                self.unpaid_services.append(service.as_csv_entry(delimiter=OUT_DELIMITER))
        
        self.unpaid_services_csv = IN_DELIMITER.join(self.unpaid_services)
        self.unpaid_services = unpaid_services
            
        self.status = status
        self.date_invoiced = date_invoiced
        self.due_date = (date_invoiced + timedelta(days=self.get_last_day_of_month(date_invoiced.year, date_invoiced.month))) if date_invoiced is not None else None
        self.date_paid = date_paid
        self.days_overdue = 0            
    
    def mark_as_invoiced(self, date_invoiced: datetime = None) -> None:
        """
            Mark today as invoiced date and set due Date to on the same day of next month.
        """
        self.date_invoiced = datetime.now() if date_invoiced is None else date_invoiced
        self.due_date = self.date_invoiced + timedelta(days=self.get_last_day_of_month())
    
    def mark_as_paid(self, date_paid: datetime = None) -> None:
        """
            Mark today as paid date and set status to `PAID`.
        """
        self.status = PaymentStatus.PAID
        self.date_paid = datetime.now() if date_paid is None else date_paid
        
    def get_last_day_of_month(self, year=None, month=None):
        """
            Return the last day of specified year and month of invoiced date
        """
        if year is not None and month is not None:
            return calendar.monthrange(year, month)[1]
        return calendar.monthrange(self.date_invoiced.year, self.date_invoiced.month)[1]
    
    def as_receipt(self) -> str:
        unpaid_services = ""
        total_cost = 0
        for service in self.unpaid_services:
            total_cost += service.get_cost()
            unpaid_services += f"""\t - ID: {service.id}\
                               \n\t\t + Date: {service.date}\
                               \n\t\t + Description: {service.description}\
                               \n\t\t + Cost: {to_dollar(service.get_cost())}\n"""
            
        return f"""Invoice ID: {self.id}\
                 \n\tStatus: {self.status.name}\
                 \nPatient's information:\
                 \n\tName: {self.patient_info[0]}\t\tAddress: {self.patient_info[1]}\
                 \nCarrier information:\
                 \n\tName: {self.carrier_info[0]}\t\tAddress: {self.carrier_info[1]}\
                 \nUnpaid services:\
                 \n{unpaid_services}\
                 \r{"-"*16}\
                 \nAmount due: {self.amount_due}\t\tTotal cost: {to_dollar(total_cost)}""".expandtabs(4)
        
        
    
    def as_csv_entry(self, delimiter=IB_DB_FIELD_DELIMITER) -> str:
        return f"{self.id}{delimiter}{self.status.name}{delimiter}{self.amount_due}{delimiter}{self.patient_info_csv}{delimiter}{self.carrier_info_csv}{delimiter}{self.unpaid_services_csv}{delimiter}{self.date_invoiced}{delimiter}{self.due_date}{delimiter}{self.date_paid}{delimiter}{self.days_overdue}"
    
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
        Store patients' bill(s) of insurance carriers for services provided by the medical clinic.
        
        #### Notes:
        - `id` can mean `user_id` or `patient_id` as it will use the same id to get data from database.
        - When `id` is not given, a new and unique id will be generated along with its new databases.
        - Use `commit_to_db()` in order to save local changes to the database.
    """
    def __init__(self, id=None) -> None:
        if id is not None:
            self.id = id
        else:
            # generate new id by retrieving all used ids from database folder
            used_ids = []
            for file in os.listdir(IB_DB_DIR):
                if file.endswith(".csv"):
                    used_id = file.split("_")[0].split("id")[1]
                    if used_id.isnumeric():
                        used_ids.append(int(used_id))
            
            self.id = 0
            while any(self.id == used_id for used_id in used_ids):
                self.id += 1
        
        # retrieve data of `id` from the database
        self.retrieve_data()
            
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
        self.services = list()
        with open(self.__service_db, 'r') as f:
            for service in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_FIELD_DELIMITER):
                r_service = InsuranceService(id=        service['Service ID'], 
                                            description=service['Service Description'], 
                                            cost=       service['Service Cost'])
                
                r_service.date = datetime.strptime(service['Service Date'], '%Y-%m-%d %H:%M:%S.%f')
                r_service.status = PaymentStatus[service['Payment Status']]
                self.services.append(r_service)
        
        # carrier database file
        self.__carrier_db = IB_DB_DIR + f"/id{self.id:08}" + "_carriers.csv"
        if not Path(self.__carrier_db).is_file():
            open(self.__carrier_db, "a").close()
            
        # retrieve carrier list from db
        self.carriers = list()
        with open(self.__carrier_db, 'r') as f:
            for carrier in csv.DictReader(f, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_FIELD_DELIMITER):
                r_carrier = InsuranceCarrier(id=            carrier['Insurance Carrier ID'],
                                             name=          carrier['Insurance Carrier name'],
                                             address=       carrier['Insurance Carrier Address'],
                                             primary=       True if carrier['Primary Carrier'] == 'PRIMARY' else False)
                
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
        self.invoices = list()
        
        with open(self.__invoice_db, 'r') as f:
            for invoice in csv.DictReader(f, fieldnames=IB_DB_FIELDS['II'], delimiter=IB_DB_FIELD_DELIMITER):
                unpaid_services = []
                if invoice['Unpaid Services'] not in NONE:
                    for service_csv in invoice['Unpaid Services'].split(IN_DELIMITER):
                        service_d = service_csv.split(OUT_DELIMITER)
                        unpaid_service = InsuranceService(id=         service_d[0], 
                                                          description=service_d[1],
                                                          cost=       service_d[2],
                                                          date=       datetime.strptime(service_d[3], '%Y-%m-%d %H:%M:%S.%f'))
                        unpaid_services.append(unpaid_service)
                
                r_invoice = InsuranceInvoice(id=                invoice['Invoice ID'],
                                             status=            PaymentStatus[invoice['Invoice Status']],
                                             amount_due=        invoice['Amount Due'],
                                             patient_info=      invoice['Patient Info'].split(IN_DELIMITER),
                                             carrier_info=      invoice['Carrier Info'].split(IN_DELIMITER),
                                             unpaid_services=   unpaid_services)
                        
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
    
    #---------------
    #   DATABASE
    #---------------
    def commit_to_db(self) -> None:
        """
            Commit local changes to the database by rewriting all data to its databases, 
            including `services`, `carriers`, and `invoices`.
        """
        with open(self.__service_db, 'w') as fs, open(self.__carrier_db, 'w') as fc, open(self.__invoice_db, 'w') as fi:
            for service in self.services:
                fs.write(service.as_csv_entry() + "\n")
            for carrier in self.carriers:
                fc.write(carrier.as_csv_entry() + "\n")
            for invoice in self.invoices:
                fi.write(invoice.as_csv_entry() + "\n")
    
    def sort_local_db(self, sort_by_id=False, sort_by_name=False, sort_by_cost=False, reversed=False) -> None:
        """
            Sort the local database according to the argument.
            
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
        elif sort_by_name:
            self.carriers = sorted(self.carriers, key=lambda x: x.name, reverse=reversed)
        elif sort_by_cost:
            self.services = sorted(self.services, key=lambda x: x.cost, reverse=reversed)
    
    #---------------
    #   CARRIERS
    #---------------
    def new_carrier(self, carrier_name, carrier_address, primary=False) -> str:
        """ 
            Add a row of new Insurance Carrier to the local database.
            
            If `primary` is `True`, set all other carriers' `primary` key to `False`.
            
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
        
        while any(carrier.id == carrier_id for carrier in self.carriers):
            carrier_id = str(int(carrier_id) + 1)
            
        has_primary = False
        for carrier in self.carriers:
            if carrier.primary:
                has_primary = True
                break
        
        # mark insurance carrier as primary if there isnt one yet
        if not has_primary:
            primary = True
        
        if primary:
            # set all other carriers' primary to False in local list
            for carrier in self.carriers:
                if carrier.primary:
                    carrier.primary = False
            
        n_carrier = InsuranceCarrier(id=carrier_id, name=carrier_name, address=carrier_address, primary=primary)
        # add carrier to local list
        self.carriers.append(n_carrier)
        
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
            if carrier.id == carrier_id:
                # mark the most recent carrier as primary if a primary Carrier is being removed
                if carrier.primary: 
                    self.carriers[-1].primary = True
                self.carriers.remove(carrier)
                return True
        
        return False
    
    #---------------
    #   SERVICES
    #---------------
    def new_service(self, service_description, service_cost, fillin_id=True) -> str:
        """ 
            Add a row of new Service to the local database.
            
            Note: use `commit_to_db()` in order to save local changes to the database.
            
            #### Parameters:
            - `service_description` description of the new service.
            - `service_cost` cost of the new service (format: `$___`).
            - `fillin_id` indicates if the new service id should be higher than the most recent one.
            
            #### Returns: 
            - a new and unique `service_id`.
        """
        service_id = "0" if fillin_id else max(self.services, key=lambda x: x.id).id
        while any(service.id == service_id for service in self.services):
            service_id = str(int(service_id) + 1)
        
        n_service = InsuranceService(id=service_id, description=service_description, cost=service_cost)
        
        # add service to local list
        self.services.append(n_service)
        
        return service_id
    
    def remove_service(self, service_id) -> bool:
        """ 
            Remove the row of where `service_id` is found in the local database.
            
            Note: use `commit_to_db()` in order to save local changes to the database.
            
            #### Parameters:
            - `service_id` to find in database.
            
            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        service_id = str(service_id)
        for service in self.services:
            if service.id == service_id:
                self.services.remove(service)
                return True

        return False
    
    #---------------
    #   INVOICES
    #---------------
    def generate_invoice(self, month_to_be_billed=None) -> str:
        """ 
            Generate invoice from this **current** billing cycle (customizable through
            `month=` argument) then append it to local invoice list.
            
            Billing cycles typically start from the end of the month 
            (on the 30th or 31st) until the next month.
            
            Note: to retrieve invoice info, use `invoice_info()`. 
            
            #### Parameters:
            - `month_to_be_billed` to specify a month to collect unpaid services.
            Leave as `None` for the current month.
            
            #### Returns:
            - `invoice_id`.
            - `-1` if all services are paid or no services found.
        """
        patient_info = [self.user['First Name'] + ' ' + self.user['Last Name'], self.user['Address']]
        carrier_info = [self.carriers[-1].name, self.carriers[-1].address]
        if not self.carriers[-1].primary:
            for carrier in self.carriers:
                if carrier.primary:
                    self.primary_carrier = carrier
                    carrier_info = [carrier.name, carrier.address]
                    break
        
        unpaid_services = []
        total_cost = 0
        if month_to_be_billed is None: 
            month_to_be_billed = datetime.now().month
        
        for service in self.services:
            if service.payment_status is PaymentStatus.UNPAID:
                if service.date.month == month_to_be_billed:
                    last_day_of_month = calendar.monthrange(service.date.year, month_to_be_billed)[1]
                    if service.date.day <= last_day_of_month:
                        total_cost += service.get_cost()
                        unpaid_services.append(service)
        
        if not unpaid_services or not self.services:
            return '-1'
        
        invoice_id = "0"
        while any(invoice.id == invoice_id for invoice in self.invoices):
            invoice_id = str(int(invoice_id) + 1)
            
        n_invoice = InsuranceInvoice(id=invoice_id, amount_due=total_cost, patient_info=patient_info, carrier_info=carrier_info, 
                                     unpaid_services=unpaid_services)
        n_invoice.mark_as_invoiced()
        
        # add invoice to local list
        self.invoices.append(n_invoice)
        
        return invoice_id
    
    def invoice_info(self, invoice_id) -> str:
        """ 
            Return invoice as string. Format as below:
            
            Invoice ID: `id`
            \tStatus: `status`
            Patient's information:
            \tName: `name`\t\tAddress: `address`
            Carrier information:
            \tName: `name`\t\tAddress: `address`
            Unpaid services:\n
            \t \- ID: `id`
            \t\t + Date: `date`
            \t\t + Description: `description`
            \t\t + Cost: `cost`
            \----------------\n
            Amount due: `amt`\t\tTotal cost: `cost`
        
        """
        invoice_id = str(invoice_id)
        
        for invoice in self.invoices:
            if invoice.id == invoice_id:
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
            if invoice.id == invoice_id:
                diff = float(invoice.amount_due.replace("$", '')) - amount
                if diff <= 0 or pay_in_full:
                    invoice.status = PaymentStatus.PAID
                    invoice.date_paid = datetime.now()
                    invoice.days_overdue = 0
                    invoice.amount_due = "$0"
                else:
                    invoice.status = PaymentStatus.PENDING
                    invoice.amount_due = to_dollar(diff)
                
                carrier = self.carriers[-1]
                for _carrier in self.carriers:
                    if _carrier.primary:
                        carrier = _carrier
                if datetime.now() - invoice.due_date > timedelta(days=15):
                    carrier.status = PaymentStatus.DIFFICULT
                elif datetime.now() - invoice.due_date > timedelta(days=0):
                    carrier.status = PaymentStatus.LATE
                else:
                    carrier.status = PaymentStatus.ONTIME
                return True
            
        return False
        
    #---------------
    #   REPORTS
    #---------------
    def generate_report(self, patient_name=None, carrier: InsuranceCarrier=None, carrier_name=None, carrier_address=None) -> str:
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
            if invoice.status is PaymentStatus.DELINQUENT:
                if patient_name is not None:
                    if invoice.patient_info[0] == patient_name:
                        delinquent_reports += self.invoice_info(invoice.id) + "\n"
                else:
                    if invoice.carrier_info == [carrier.name, carrier.address]:
                        delinquent_reports += self.invoice_info(invoice.id) + "\n"

        return delinquent_reports
            
#
#
#   Test/Debug Section
#
#
def service_tests(bill):
    print(bill.services)
    if bill.remove_service(1): 
        print("<<< removed service with id=1")
        print(bill.services)

    print(">>> add new service: ear piecing with the cost of $1000 id =", bill.new_service('ear piercing', '$1000'))
    print(bill.services)
    print(">>> add new service: gym membership with the cost of $10 id =", bill.new_service('gym membership', '$10'))
    print(bill.services)
    if bill.remove_service(1): 
        print("<<< removed service with id=1")
        print(bill.services)
    print(">>> add new service: wifi plans with the cost of $580 id =", bill.new_service('wifi plans', '$580'))
    print(bill.services)
    
def carrier_tests(bill):
    print()
    print(bill.carriers)
    print(">>> add new carrier: PRIMARY Medical @111 1st st id =", bill.new_carrier('Medical', '111 1st st', primary=True))
    print(bill.carriers)
    print(">>> add new carrier: PRIMARY Care @222 2nd st id =", bill.new_carrier('Care', '222 2nd st', primary=True))
    
    print(bill.carriers)
    
    if bill.remove_carrier(0): 
        print("<<< removed carrier with id=0")
        print(bill.carriers)
    
    print(">>> add new carrier: non-primary SupCare @333 3rd st with id =", bill.new_carrier('SupCare', '333 3rd st', primary=False))
    print(bill.carriers)

def invoice_tests(bill, pay=True):
    print()
    bill.new_carrier("Jessica", '@home', primary=True)
    bill.new_service('ear piercing', '$1000')
    bill.new_service('wifi plans', '$580')
    bill.new_service('gym membership', '$20')
    
    print(">>> list of invoices:", bill.invoices)
    print(">>> new invoice with id =", bill.generate_invoice())
    print(">>> new list of invoices:", bill.invoices)
    print("\n>>> new invoice csv entry:")
    print(bill.invoices[-1].as_csv_entry())
    print()
    print(">>> last unpaid service on invoice:")
    print(bill.invoices[-1].unpaid_services[-1])
    bill.commit_to_db()
    if pay:
        print()
        print("paying invoice id =", bill.invoices[-1].id, "in full amount!")
        time.sleep(3)
        bill.pay_for_invoice(bill.invoices[-1].id, pay_in_full=True)
        print(bill.invoices[-1].as_csv_entry())
    
    print(">>> delinquent invoices by patient name:")
    print(bill.generate_report(patient_name=bill.user_name))
    
    print(">>> delinquent invoices by carrier:")
    print(bill.generate_report(carrier=bill.primary_carrier))

def clean_up():
    # remove all csv files in `IB_DB_DIR` directory 
    if Path(IB_DB_DIR).is_dir():
        for file in os.listdir(IB_DB_DIR):
            if file.endswith(".csv"):
                os.remove(IB_DB_DIR + "/" + file)

def run_tests() -> None:
    clean_up()
    bill = InsuranceBilling(69658883)

    service_tests(bill) # service tests
    bill.commit_to_db()
    carrier_tests(bill) # carrier tests
    bill.commit_to_db()
    invoice_tests(bill, pay=True) # invoice tests
    bill.commit_to_db()

    # clean_up()

if __name__ == "__main__":
    run_tests()