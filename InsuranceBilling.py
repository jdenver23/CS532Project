from enum import Enum
from pathlib import Path
import os
import csv
from datetime import datetime


# IB_DB key format:
#   IC: Insurance Carrier
#   IS: Insurance Service
# IB_DB value:
#   field names
IB_DB_DIR = "IB_DB"
IB_DB_FIELDS = {
    "IC": ['Insurance carrier ID', 'Insurance carrier name', 'Insurance carrier address', 'Insurance carrier status', 'Primary carrier'],
    "IS": ['Service ID', 'Service description', 'Service cost', 'Service date'],
}
IB_DB_DELIMITER = "~"

#
#
#   Insurance Classes
#
#
class CarrierStatus(Enum):
    """
        Payments status of an Insurance carrier.
        #### Available enums:
        - `ONTIME` (index = 0)
        - `LATE` (index = 1)
        - `DIFFICULT` (index = 2)
    """ 
    ONTIME = 0
    LATE = 1
    DIFFICULT = 2
    
    def __eq__(self, other) -> bool:
        return str(self.value) == (other if other.__class__ == str else str(other))
    
class InsuranceCarrier:
    def __init__(self, id, name, address, primary=False) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.status = CarrierStatus.ONTIME
        self.primary = primary
        
    def as_csv_entry(self) -> str:
        return f"{self.id}{IB_DB_DELIMITER}{self.name}{IB_DB_DELIMITER}{self.address}{IB_DB_DELIMITER}{self.status.value}{IB_DB_DELIMITER}{self.primary}"
    
    def __str__(self) -> str:
        return f"""'Insurance carrier ID': {self.id}, \
                    \n'Insurance carrier name': {self.name}, \
                    \n'Insurance carrier address': {self.address}, \
                    \n'Insurance carrier status': {self.status.name}, \
                    \n'Primary carrier': {self.primary}\
                """

class InsuranceService:
    def __init__(self, id, description, cost, date=None) -> None:
        self.id = id
        self.description = description
        self.cost = cost
        self.date = datetime.now() if date is None else date
        
    def as_csv_entry(self) -> str:
        return f"{self.id}{IB_DB_DELIMITER}{self.description}{IB_DB_DELIMITER}{self.cost}{IB_DB_DELIMITER}{self.date}"
        
    def __str__(self) -> str:
        return f"""'Service ID': {self.id}, \
                   \n'Service description': {self.description}, \
                   \n'Service cost': {self.cost}, \
                   \n'Service date': {self.date}\
                """

#
#
#   Main Class
#
#
class InsuranceBilling:
    def __init__(self, id=None, name=None, address=None) -> None:
        if id is not None:
            self.id = id
        else:
            # generate new id by retrieving all used ids from database folder
            used_ids = []
            for file in os.listdir(IB_DB_DIR):
                if file.endswith(".csv"):
                    used_ids.append(int(file.split("_")[0].split("id")[1]))
            
            self.id = 0
            while any(self.id == used_id for used_id in used_ids):
                self.id += 1
            
        
        # service database file
        # currently db file name is in this format:
        #       id{self.id:07}_services.csv
        #          __________  <- front padding so that string len is 7
        self.service_db = IB_DB_DIR + f"/id{self.id:07}" + "_services.csv"
        if not Path(self.service_db).is_file():
            open(self.service_db, "a").close()
        
        # retrieve service list from db
        self.services = list()
        with open(self.service_db, 'r') as inp:
            for service in csv.DictReader(inp, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_DELIMITER):
                self.services.append(InsuranceService(service['Service ID'], 
                                                      service['Service description'], 
                                                      service['Service cost'], 
                                                      service['Service date']))
        
        # carrier database file
        self.carrier_db = IB_DB_DIR + f"/id{self.id:07}" + "_carriers.csv"
        if not Path(self.carrier_db).is_file():
            open(self.carrier_db, "a").close()
            
        # retrieve carrier list from db
        self.carriers = list()
        with open(self.carrier_db, 'r') as inp:
            for carrier in csv.DictReader(inp, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_DELIMITER):
                r_carrier = InsuranceCarrier(carrier['Insurance carrier ID'],
                                             carrier['Insurance carrier name'],
                                             carrier['Insurance carrier address'],
                                             carrier['Primary carrier'])
                r_carrier.status = CarrierStatus(int(carrier['Insurance carrier status']))
                self.carriers.append(r_carrier)
                
    def commit_to_db(self) -> None:
        with open(self.service_db, 'w') as f:
            for service in self.services:
                f.write(service.as_csv_entry())
        with open(self.carrier_db, 'w') as f:
            for carrier in self.carriers:
                f.write(carrier.as_csv_entry())
    
    #---------------
    #   CARRIERS
    #---------------
    def new_carrier(self, carrier_name, carrier_address, primary=False) -> None:
        """ 
            Add a row of new Insurance Carrier to the database.
            
            If `primary` is `True`, set all other carriers' `primary` key to `False`.
            
            #### Parameters:
            - `carrier_name` name of the carrier
            - `carrier_address` address of the carrier
            - `service_description` description of the new carrier
            - `primary` is this a primary insurance?
            
            #### Returns: 
            - a new and unique `service_id`
        """
        carrier_id = "0"
        
        while any(carrier.id == carrier_id for carrier in self.carriers):
            carrier_id = str(int(carrier_id) + 1)
            
        primary_count = 0
        for carrier in self.carriers:
            if carrier.primary:
                primary_count += 1
        
        # mark insurance carrier as primary if there isnt one yet
        if primary_count == 0 and primary:
            primary = True
        
        if primary:
            # set all other carriers' primary to False in local list
            for carrier in self.carriers:
                if carrier.primary:
                    carrier.primary = False
            # set all other carriers' primary to False in the database
            with open(self.carrier_db, 'w') as f:
                for carrier in self.carriers:
                    f.write(carrier.as_csv_entry() + "\n")
            
        n_carrier = InsuranceCarrier(carrier_id, carrier_name, carrier_address, primary)
        # add carrier to local list
        self.carriers.insert(0 if primary else len(self.carriers), n_carrier)
        
        # add carrier to db
        with open(self.carrier_db, 'a') as f:
            f.write(n_carrier.as_csv_entry() + "\n")
        
        return carrier_id
    
    def remove_carrier(self, carrier_id) -> bool:
        """ 
            Remove the row of where `carrier_id` is found in the database.
            
            If the to-be removed carrier has its `primary` key as `True`, 
            then the most recent `carrier_id` will be selected to be the 
            primary carrier for this insurance bill.
            
            #### Parameters:
            - `carrier_id` to find in database
            
            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        if Path(self.carrier_db + ".tmp").is_file(): 
            os.remove(self.carrier_db + ".tmp")
        
        carrier_id = str(carrier_id)
        found_idx = None
        count = 0
        with open(self.carrier_db, 'r') as inp, open(self.carrier_db + ".tmp", 'w', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_DELIMITER)
            for row in csv.DictReader(inp, fieldnames=IB_DB_FIELDS['IC'], delimiter=IB_DB_DELIMITER):
                if row['Insurance carrier ID'] != carrier_id:
                    writer.writerow(row)
                else:
                    is_primary = row['Primary carrier']
                    found_idx = count
                count += 1
        
        if found_idx is not None:
            # print(f"found {found_idx} {'carrier' if found_idx == 1 else 'carriers'}")
            os.remove(self.carrier_db)
            os.rename(self.carrier_db + ".tmp", self.carrier_db)
            for carrier in self.carriers:
                if carrier.id == carrier_id:
                    self.carriers.remove(carrier)
                    break
                
            # mark the most recent carrier as primary if a primary carrier is being removed
            if is_primary:
                self.carrier[-1].primary = True
            return True
        
        # remove tmp file if no carrier found
        # print(f"Insurance carrier ID not found")
        os.remove(self.carrier_db + ".tmp")
        return False
    
    #---------------
    #   SERVICES
    #---------------
    def new_service(self, service_description, service_cost, fillin_id=True) -> int:
        """ 
            Add a row of new Service to the database.
            #### Parameters:
            - `service_description` description of the new service
            - `service_cost` cost of the new service (format: `$___`)
            
            #### Returns: 
            - a new and unique `service_id`
        """
        service_id = "0" if fillin_id else max(self.services, key=lambda x: x.id).id
        while any(service.id == service_id for service in self.services):
            service_id = str(int(service_id) + 1)
        
        n_service = InsuranceService(service_id, service_description, service_cost)
        # add service to db
        with open(self.service_db, 'a') as f:
            f.write(n_service.as_csv_entry() + "\n")
        
        # add service to local list
        self.services.append(n_service)
        
        return service_id
    
    def remove_service(self, service_id) -> bool:
        """ 
            Remove the row of where `service_id` is found in the database.
            #### Parameters:
            - `service_id` to find in database
            
            #### Returns:
            - `True` if row successfully removed. 
            - `False` otherwise.
        """
        if Path(self.service_db + ".tmp").is_file(): 
            os.remove(self.service_db + ".tmp")
        
        service_id = str(service_id)
        found_idx = None
        count = 0
        with open(self.service_db, 'r') as inp, open(self.service_db + ".tmp", 'w', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_DELIMITER)
            for row in csv.DictReader(inp, fieldnames=IB_DB_FIELDS['IS'], delimiter=IB_DB_DELIMITER):
                if row['Service ID'] != service_id:
                    writer.writerow(row)
                else:
                    found_idx = count
                count += 1
        
        if found_idx is not None:
            # print(f"found {found_idx} {'service' if found_idx == 1 else 'services'}")
            os.remove(self.service_db)
            os.rename(self.service_db + ".tmp", self.service_db)
            self.services = self.services[:found_idx] + self.services[found_idx+1:]
            return True
        
        # remove tmp file if no service found
        # print(f"Service ID not found")
        os.remove(self.service_db + ".tmp")
        return False
        
        
    def generate_invoice(self, patient_id) -> str:
        # TODO: format invoice
        # search for patient by id from database
        # retrieve: patient name and address
        #           services info
        pass
    
    #---------------
    #    OTHERS
    #---------------
    def print_all_services(self, just_id=False) -> None:
        if just_id:
            s = []
            for service in self.services:
                s.append(service.id)
            print(s)
        else:
            for service in self.services:
                print(service)
    
    def print_all_carriers(self, just_id=False) -> None:
        if just_id:
            s = []
            for carrier in self.carriers:
                s.append(carrier.id)
            print(s)
        else:
            for carrier in self.carriers:
                print(carrier)
        

def service_tests(bill):
    bill.print_all_services(True)
    if bill.remove_service(1): 
        print("\n<<< removed service with id=1")
        bill.print_all_services(True)

    print("\n>>> add new service: ear piecing with the cost of $1000 id =", bill.new_service("ear piercing", "$1000"))
    bill.print_all_services(True)
    print("\n>>> add new service: gym membership with the cost of $10 id =", bill.new_service("gym membership", "$10"))
    bill.print_all_services(True)
    
def carrier_tests(bill):
    bill.print_all_carriers(True)
    print("\n>>> add new carrier: PRIMARY Medical @111 1st st id =", bill.new_carrier('Medical', '111 1st st', True))
    bill.print_all_carriers(True)
    print("\n>>> add new carrier: PRIMARY Care @222 2nd st id =", bill.new_carrier('Care', '222 2nd st', True))
    
    bill.print_all_carriers(True)
    
    if bill.remove_carrier(0): 
        print("\n<<< removed carrier with id=0")
        bill.print_all_carriers(True)
    
    print("\n>>> add new carrier: non-primary SupCare @333 3rd st with id =", bill.new_carrier('SupCare', '333 3rd st', False))
    bill.print_all_carriers(True)
    
#
#
# IB Tests
#
#
bill = InsuranceBilling()

# service tests
# service_tests(bill)

# carrier tests
# carrier_tests(bill)