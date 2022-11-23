from datetime import datetime
from pathlib import Path
import os
from InsuranceBilling import InsuranceBilling, PaymentStatus, IB_DB_DIR, USER_FILE
from ib_gui import ib_gui

def init_gui(uid: str or int):
    insurance_bill = InsuranceBilling(id=uid)
    app = ib_gui.MainGUI(bill=insurance_bill)
    app.run()


#
#
#   Test/Debug Section
#
#

uid = 30000000


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


def __clean_up__(opt=0):
    count = 0
    
    with open(USER_FILE, "r+", encoding = "utf-8") as file:
        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
        
        if opt != 0:
            file.write('\n')

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
    __clean_up__()
    if not Path(IB_DB_DIR).is_dir():
        os.mkdir(IB_DB_DIR)
    with open(USER_FILE, mode='a', newline='\n') as f:
        f.write('\n')
        f.write(",".join([str(uid), "TRI", "TRAN", "tree@test.com", "123456",
                        "1234567890", "123@4th Ave", "CS 532", "11/11/1111", "Male"]))
        f.write('\n')
    bill = InsuranceBilling(uid)
    # bill.new_carrier('Medical', '111 1st st', primary=True)
    # bill.new_carrier('Care', '222 2nd st', primary=True)
    # bill.new_carrier('SupCare', '333 3rd st', primary=False)
    # bill.commit_to_db()

    __service_tests__(bill)  # service tests
    bill.commit_to_db()
    __carrier_tests__(bill)  # carrier tests
    bill.commit_to_db()
    bill.generate_invoice(month=11)
    bill.generate_invoice(month=12)
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
        __clean_up__(1)
