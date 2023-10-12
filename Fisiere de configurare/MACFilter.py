import tkinter as tk
from tkinter import filedialog
import csv
import re
from datetime import datetime

def filter_mac_addresses():
    randomized_listbox.delete(0, tk.END)
    non_randomized_listbox.delete(0, tk.END)
    randomized_listbox_2.delete(0, tk.END)
    non_randomized_listbox_2.delete(0, tk.END)
    comparison_listbox.delete(0, tk.END)
    randomized_counter = 0
    non_randomized_counter = 0
    randomized_counter_2 = 0
    non_randomized_counter_2 = 0

    non_randomized_set_1 = set()
    non_randomized_set_2 = set()
    non_randomized_counter_dict = {}

    # Select the first CSV file
    file_path_1 = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path_1:
        return

    # Filter MAC addresses from the first CSV file
    with open(file_path_1, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            mac_address = row[4]
            timestamp_str = row[0]
            is_randomized = check_mac_address_randomized(mac_address)
            if is_randomized:
                randomized_listbox.insert(tk.END, f"{mac_address} ({timestamp_to_datetime(timestamp_str)})")
                randomized_counter += 1
            else:
                non_randomized_listbox.insert(tk.END, f"{mac_address} ({timestamp_to_datetime(timestamp_str)})")
                non_randomized_counter += 1
                non_randomized_set_1.add(mac_address)
                if mac_address in non_randomized_counter_dict:
                    non_randomized_counter_dict[mac_address] += 1
                else:
                    non_randomized_counter_dict[mac_address] = 1

    # Select the second CSV file
    file_path_2 = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path_2:
        return

    # Filter MAC addresses from the second CSV file
    with open(file_path_2, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            mac_address = row[4]
            timestamp_str = row[0] 
            is_randomized = check_mac_address_randomized(mac_address)
            if is_randomized:
                randomized_listbox_2.insert(tk.END, f"{mac_address} ({timestamp_to_datetime(timestamp_str)})")
                randomized_counter_2 += 1
            else:
                non_randomized_listbox_2.insert(tk.END, f"{mac_address} ({timestamp_to_datetime(timestamp_str)})")
                non_randomized_counter_2 += 1
                non_randomized_set_2.add(mac_address)
                if mac_address in non_randomized_counter_dict:
                    non_randomized_counter_dict[mac_address] += 1
                else:
                    non_randomized_counter_dict[mac_address] = 1

    # Find common elements in non-randomized addresses from both CSV files
    common_addresses = non_randomized_set_1.intersection(non_randomized_set_2)

    # Add common addresses to the comparison listbox
    for address in common_addresses:
        count = non_randomized_counter_dict[address]
        comparison_listbox.insert(tk.END, f"{address} (Count: {count})")

    # Update the counter label with the count of common addresses
    common_counter = len(common_addresses)
    common_counter_label.config(text=f"Common Non-Randomized Addresses ({common_counter})")

    randomized_label.config(text=f"Randomized Addresses (File 1) ({randomized_counter})")
    non_randomized_label.config(text=f"Non-Randomized Addresses (File 1) ({non_randomized_counter})")
    randomized_label_2.config(text=f"Randomized Addresses (File 2) ({randomized_counter_2})")
    non_randomized_label_2.config(text=f"Non-Randomized Addresses (File 2) ({non_randomized_counter_2})")

def check_mac_address_randomized(mac_address):
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address):
        return False

    first_octet = int(mac_address.split(':')[0], 16)
    if (first_octet & 2) == 0:
        return False

    for octet in mac_address.split(':')[1:]:
        if int(octet, 16) != 0:
            return True

    return False

def timestamp_to_datetime(timestamp_str):
    try:
        timestamp = datetime.utcfromtimestamp(int(timestamp_str))
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp_str

# Create the main window
window = tk.Tk()
window.title("Filtered MAC Addresses")

# Create a label for randomized addresses from the first CSV file
randomized_label = tk.Label(window, text="Randomized Addresses (File 1)")
randomized_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

# Create a listbox for randomized addresses from the first CSV file
randomized_listbox = tk.Listbox(window, width=50)
randomized_listbox.grid(row=1, column=0, padx=10, pady=5)

# Create a label for randomized addresses from the second CSV file
randomized_label_2 = tk.Label(window, text="Randomized Addresses (File 2)")
randomized_label_2.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

# Create a listbox for randomized addresses from the second CSV file
randomized_listbox_2 = tk.Listbox(window, width=50)
randomized_listbox_2.grid(row=1, column=1, padx=10, pady=5)

# Create a label for non-randomized addresses from the first CSV file
non_randomized_label = tk.Label(window, text="Non-Randomized Addresses (File 1)")
non_randomized_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

# Create a listbox for non-randomized addresses from the first CSV file
non_randomized_listbox = tk.Listbox(window, width=50)
non_randomized_listbox.grid(row=3, column=0, padx=10, pady=5)

# Create a label for non-randomized addresses from the second CSV file
non_randomized_label_2 = tk.Label(window, text="Non-Randomized Addresses (File 2)")
non_randomized_label_2.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

# Create a listbox for non-randomized addresses from the second CSV file
non_randomized_listbox_2 = tk.Listbox(window, width=50)
non_randomized_listbox_2.grid(row=3, column=1, padx=10, pady=5)

# Create a label for the comparison listbox
comparison_label = tk.Label(window, text="Common Non-Randomized Addresses")
comparison_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Create a listbox for comparing non-randomized addresses
comparison_listbox = tk.Listbox(window, width=50)
comparison_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Create a label for the common non-randomized addresses count
common_counter_label = tk.Label(window, text="")
common_counter_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Create a button to select and filter MAC addresses
select_button = tk.Button(window, text="Select CSV Files", command=filter_mac_addresses)
select_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Start the GUI event loop
window.mainloop()
