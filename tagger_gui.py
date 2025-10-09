import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

DATA_FILE = "data.csv"
LOG_FILE = "retrieval_log.csv"
VALID_USERS = {"omkar", "akshay", "prajakta", "amar", "shrikant", "sander", "mathijs", "dirk", "rohit", "kedar"}
RESET_USERS = {"omkar", "akshay", "shrikant"}


# Load data
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{k.strip(): v.strip() for k, v in row.items()} for row in reader]


# Save data
def save_data(data):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Customer ID", "Type", "Offer", "IMSI", "SIM", "MSISDN", "BILL CYCLE", "Used", "User_ID"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Log retrieval
def log_retrieval(user, cid, type_val, offer_val):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, user, cid, type_val, offer_val])


# Verify username
def verify_user():
    user = username_var.get().strip().lower()
    if user in VALID_USERS:
        status_label.config(text=f"Welcome, {user}", fg="#0078D7")
        retrieve_button.config(state="normal")
        reset_button.config(state="normal" if user in RESET_USERS else "disabled")
    else:
        status_label.config(text="Invalid username", fg="#D83B01")
        retrieve_button.config(state="disabled")
        reset_button.config(state="disabled")


# Update dropdowns
def update_dropdowns():
    types = sorted(set(row["Type"] for row in data if not row["Used"]))
    offers = sorted(set(row["Offer"] for row in data if not row["Used"]))
    cycles = sorted(set(row["BILL CYCLE"] for row in data if not row["Used"]))
    type_dropdown['values'] = types
    offer_dropdown['values'] = offers
    cycle_dropdown['values'] = cycles


# Retrieve full details
def retrieve_cid():
    user = username_var.get().strip().lower()
    selected_type = type_var.get()
    selected_offer = offer_var.get()
    selected_cycle = cycle_var.get()

    for row in data:
        if (row["Type"] == selected_type and
                row["Offer"] == selected_offer and
                row["BILL CYCLE"] == selected_cycle and
                not row["Used"]):
            row["Used"] = "Yes"
            row["User_ID"] = user
            save_data(data)
            log_retrieval(user, row["Customer ID"], selected_type, selected_offer)

            # Display full details
            details_output.delete("1.0", tk.END)
            details_output.insert(tk.END, f"Customer ID: {row['Customer ID']}\n")
            details_output.insert(tk.END, f"Type: {row['Type']}\n")
            details_output.insert(tk.END, f"Offer: {row['Offer']}\n")
            details_output.insert(tk.END, f"IMSI: {row['IMSI']}\n")
            details_output.insert(tk.END, f"SIM: {row['SIM']}\n")
            details_output.insert(tk.END, f"MSISDN: {row['MSISDN']}\n")
            details_output.insert(tk.END, f"Bill Cycle: {row['BILL CYCLE']}\n")

            status_label.config(text="Customer ID retrieved successfully", fg="#0078D7")
            update_dropdowns()
            return

    details_output.delete("1.0", tk.END)
    status_label.config(text="No available Customer ID for selected filters", fg="#D83B01")


# Reset data
def reset_data():
    for row in data:
        row["Used"] = ""
        row["User_ID"] = ""
    save_data(data)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    update_dropdowns()
    details_output.delete("1.0", tk.END)
    status_label.config(text="Data and log reset successfully", fg="#0078D7")


# Copy full details to clipboard
def copy_cid():
    text = details_output.get("1.0", tk.END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        status_label.config(text="Details copied to clipboard", fg="#107C10")


# GUI setup
data = load_data()
root = tk.Tk()
root.title("VIT Data Retriever")
root.state("zoomed")
root.configure(bg="#e60000")  # Vodafone red

# Container
container = tk.Frame(root, bg="white", bd=1, relief="solid")
container.pack(padx=40, pady=20, fill="both", expand=True)

# Heading
tk.Label(container, text="VIT Data Retriever", bg="white", fg="#e60000", font=("Segoe UI", 20, "bold"),
         anchor="w").pack(pady=(10, 20), anchor="w")

# Username section
user_frame = tk.Frame(container, bg="white")
user_frame.pack(anchor="w", pady=5)
tk.Label(user_frame, text="Username:", bg="white", fg="#333", font=("Segoe UI", 11)).pack(side="left", padx=5)
username_var = tk.StringVar()
username_entry = tk.Entry(user_frame, textvariable=username_var, font=("Segoe UI", 11), bg="white", fg="#333", bd=2,
                          relief="groove", width=20)
username_entry.pack(side="left", padx=5)
verify_button = tk.Button(user_frame, text="Verify", command=verify_user,
                          bg="#e60000", fg="white", font=("Segoe UI", 11, "bold"),
                          activebackground="#ff6a00", activeforeground="white", bd=0, relief="flat")
verify_button.pack(side="left", padx=10)

# Filter section
filter_frame = tk.Frame(container, bg="white")
filter_frame.pack(anchor="w", pady=10)

tk.Label(filter_frame, text="Type:", bg="white", fg="#333", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=5,
                                                                                        sticky="w")
type_var = tk.StringVar()
type_dropdown = ttk.Combobox(filter_frame, textvariable=type_var, font=("Segoe UI", 11), width=30)
type_dropdown.grid(row=0, column=1, padx=5, pady=5)

tk.Label(filter_frame, text="Offer:", bg="white", fg="#333", font=("Segoe UI", 11)).grid(row=1, column=0, padx=5,
                                                                                         pady=5, sticky="w")
offer_var = tk.StringVar()
offer_dropdown = ttk.Combobox(filter_frame, textvariable=offer_var, font=("Segoe UI", 11), width=30)
offer_dropdown.grid(row=1, column=1, padx=5, pady=5)

tk.Label(filter_frame, text="Bill Cycle:", bg="white", fg="#333", font=("Segoe UI", 11)).grid(row=2, column=0, padx=5,
                                                                                              pady=5, sticky="w")
cycle_var = tk.StringVar()
cycle_dropdown = ttk.Combobox(filter_frame, textvariable=cycle_var, font=("Segoe UI", 11), width=30)
cycle_dropdown.grid(row=2, column=1, padx=5, pady=5)

# Retrieve button
retrieve_button = tk.Button(container, text="Retrieve Customer ID", command=retrieve_cid,
                            bg="#ff6a00", fg="white", font=("Segoe UI", 11, "bold"),
                            activebackground="#e60000", activeforeground="white", bd=0, relief="flat")
retrieve_button.pack(anchor="w", pady=10)
retrieve_button.config(state="disabled")

# Output section
tk.Label(container, text="Retrieved Details:", bg="white", fg="#333", font=("Segoe UI", 11)).pack(anchor="w",
                                                                                                  pady=(10, 0))
details_output = tk.Text(container, font=("Segoe UI", 11), height=8, width=80, bg="white", fg="#333", relief="groove",
                         bd=2)
details_output.pack(anchor="w", pady=5)

copy_button = tk.Button(container, text="Copy Details", command=copy_cid,
                        bg="#ff6a00", fg="white", font=("Segoe UI", 11, "bold"),
                        activebackground="#e60000", activeforeground="white", bd=0, relief="flat")
copy_button.pack(anchor="w", pady=5)

# Reset button
reset_button = tk.Button(container, text="Reset All", command=reset_data,
                         bg="#e60000", fg="white", font=("Segoe UI", 11, "bold"),
                         activebackground="#b30000", activeforeground="white", bd=0, relief="flat")
reset_button.pack(anchor="w", pady=5)
reset_button.config(state="disabled")

# Status label
status_label = tk.Label(container, text="", bg="white", fg="#333", font=("Segoe UI", 10, "italic"))
status_label.pack(anchor="w", pady=10)

# Finalize dropdowns and launch
update_dropdowns()
root.mainloop()
