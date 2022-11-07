from enum import Enum
from pathlib import Path
import os
import csv
from datetime import datetime


# IB_DB key format:
#   IC: Insurance Carrier
#   IS: Insurance Service
# IB_DB value format:
#   [0: database file name, 1: field names]
IB_DB_DIR = "IB_DB"
IB_DB = {
    "IC": [f"{IB_DB_DIR}/InsuranceCarrier.csv", ['Insurance carrier ID', 'Insurance carrier name', 'Insurance carrier address', 'Insurance carrier status']],
    "IS": [None, ['Service ID', 'Service description', 'Service cost', 'Service date']],
}
IB_DB_DELIMITER = "~"

# check for database existence, if not create an empty file
if not Path(IB_DB['IC'][0]).is_file():
    open(IB_DB['IC'][0], "a").close()

#
#
#   Insurance Billing Classes
#
#
class CarrierStatus(Enum):
    # Payments status of an Insurance carrier  
    ONTIME = 0
    LATE = 1
    DIFFICULT = 2
    
    def __eq__(self, other) -> bool:
        return str(self.value) == (other if other.__class__ == str else str(other))
    
class InsuranceCarrier:
    def __init__(self, id, name, address) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.status = CarrierStatus.ONTIME

class InsuranceService:
    def __init__(self, id, description, cost, date=None) -> None:
        self.id = id
        self.description = description
        self.cost = cost
        self.date = datetime.now() if date is None else date
        
    def __str__(self) -> str:
        return f"'Service ID': {self.id}, 'Service description': {self.description}, 'Service cost': {self.cost}, 'Service date': {self.date}"

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
            #TODO: generate new id for new insurance billing
            self.id = "//"
        
        # service database file
        # currently db file name is in this format:
        #       id{self.id:07}_services.csv
        #          __________  <- front padding so that string len is 7
        self.service_db = IB_DB_DIR + f"/id{self.id:07}" + "_services.csv"
        if not Path(self.service_db).is_file():
            open(self.service_db, "a").close()
        
        # service list
        self.services = list()
        with open(self.service_db, 'r') as inp:
            for service in csv.DictReader(inp, fieldnames=IB_DB['IS'][1], delimiter=IB_DB_DELIMITER):
                self.services.append(InsuranceService(service['Service ID'], service['Service description'], service['Service cost'], service['Service date']))
        
        # TODO: retrieve carrier list from db
        self.carriers = list[InsuranceCarrier]
        
    def new_carrier(self, carrier_id, carrier_name, carrier_address, primary=False) -> None:
        new_carrier = InsuranceCarrier(carrier_id, carrier_name, carrier_address)
        # TODO: add carrier to db
        # self.carriers.insert(new_carrier, 0 if primary else len(self.carriers))
    
    def new_service(self, service_description, service_cost) -> int:
        """ 
            Add a row of new service to the database.
            #### Parameters:
            - `service_description` description of the new service
            - `service_cost` cost of the new service (format: `$___`)
            
            #### Returns: 
            - `service_id`
        """
        service_id = max(self.services, key=lambda x: x.id).id
        while any(service.id == service_id for service in self.services):
            service_id = str(int(service_id) + 1)
        
        # TODO: add service to db
        
        # add service to local list
        self.services.append(InsuranceService(service_id, service_description, service_cost))
        
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
        found = 0
        with open(self.service_db, 'r') as inp, open(self.service_db + ".tmp", 'w', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=IB_DB['IS'][1], delimiter=IB_DB_DELIMITER)
            for row in csv.DictReader(inp, fieldnames=IB_DB['IS'][1], delimiter=IB_DB_DELIMITER):
                if row['Service ID'] != service_id:
                    writer.writerow(row)
                else:
                    found += 1
                
        if found > 0:
            # print(f"found {found} {'service' if found == 1 else 'services'}")
            os.remove(self.service_db)
            os.rename(self.service_db + ".tmp", self.service_db)
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
    
    def print_all_services(self) -> None:
        for service in self.services:
            print(service)
        


#
#
# IB Tests
#
#
bill = InsuranceBilling(1)


# service tests
bill.print_all_services()
bill.remove_service(2)
print("\n<<< removed service with id=2")
bill.print_all_services()

print("\n>>> add new service: ear piecing with the cost of $1000")
bill.new_service("ear piercing", "$1000")
bill.print_all_services()

# carrier tests
