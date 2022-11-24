# NOTE: THIS FILE MIGHT Not be necessary

import PharmacyOrder as PO
import PharmacyOrderTracking as POT
import tkinter as tk



def CO_run_GUI(passed_user_id, passed_order_list, POT_var):
    CO_root = tk.Tk()
    CO_root.title("Complete Order")

    CO_root.geometry("400x350")

    def exit_entry():
        CO_root.destroy()
        POT.initialize(passed_user_id)
    
    exit_button = tk.Button(CO_root, text='Back', command = exit_entry)
    exit_button.grid(row = 0, column = 0, pady = 5)

    pharmacist_var = tk.StringVar()
    date_filled_var = tk.StringVar()

    def complete():
        POT_var.PO_complete_order(passed_user_id, passed_order_list[POT.PRESC_ID_LOC], str(pharmacist_var), str(date_filled_var))


    presc_ID_label = tk.Label(CO_root, text = "Prescription ID: " + passed_order_list[POT.PRESC_ID_LOC], font=('calibre',10, 'bold'))
    patient_name_label = tk.Label(CO_root, text = "Patient Name: " + passed_order_list[POT.PAT_NAME_LOC], font=('calibre',10, 'bold'))
    patient_ID_label = tk.Label(CO_root, text = "Patient ID: " + passed_order_list[POT.PAT_ID_LOC], font=('calibre',10, 'bold'))
    physician_name_label = tk.Label(CO_root, text = "Physician Name: " + passed_order_list[POT.PHYS_NAME_LOC], font=('calibre',10, 'bold'))
    presc_med_label = tk.Label(CO_root, text = "Prescribed Medication: " + passed_order_list[POT.PRESC_MED_LOC], font=('calibre',10, 'bold'))
    med_ID_label = tk.Label(CO_root, text = "Medication ID: " + passed_order_list[POT.MED_ID_LOC], font=('calibre',10, 'bold'))
    dosage_label = tk.Label(CO_root, text = "Dosage: " + passed_order_list[POT.DOSAGE_LOC], font=('calibre',10, 'bold'))
    freq_label = tk.Label(CO_root, text = "Frequency: " + passed_order_list[POT.FREQ_LOC], font=('calibre',10, 'bold'))
    date_ordered_label = tk.Label(CO_root, text = "Date Ordered: " + passed_order_list[POT.D_ORD_LOC], font=('calibre',10, 'bold'))
    date_filled_label = tk.Label(CO_root, text = "Date Filled (MM/DD/YYYY): ", font=('calibre',10, 'bold'))
    pharmacist_label =tk.Label(CO_root, text = "Pharmacist: ", font=('calibre',10, 'bold'))

    pharmacist_entry = tk.Entry(CO_root, textvariable=pharmacist_var, font=('calibre',10,'normal'))
    date_filled_entry = tk.Entry(CO_root, textvariable=date_filled_var, font=('calibre',10,'normal'))

    submit_button = tk.Button(CO_root, text="Complete", command = complete)

    # TODO: need to check if prescription is already filled. 

    presc_ID_label.grid(row = 1, column = 0, pady = 5)
    patient_name_label.grid(row = 2, column = 0)
    patient_ID_label.grid(row = 3, column = 0)
    physician_name_label.grid(row = 4, column = 0)
    presc_med_label.grid(row=5, column=0)
    med_ID_label.grid(row=6, column=0)
    dosage_label.grid(row=7, column=0)
    freq_label.grid(row=8, column=0)
    date_ordered_label.grid(row=9, column=0)
    date_filled_label.grid(row=10, column=0)
    date_filled_entry.grid(row=10, column=1)
    pharmacist_label.grid(row=11, column=0)
    pharmacist_entry.grid(row=11, column=1)
    # print("IN CompleteOrder.py")

    submit_button.grid(row = 12, column = 0)

    CO_root.mainloop()