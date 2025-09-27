import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

DATA_FILE = "data.csv"
LOG_FILE = "retrieval_log.csv"
VALID_USERS = {"omkar", "akshay", "prajakta", "amar", "shrikant", "sander", "mathijs", "dirk", "rohit", "kedar"}
RESET_USERS = {"omkar", "akshay"}

# Load data
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return [{k.strip(): v.strip() for k, v in row.items()} for row in reader]

# Save data
def save_data(data):
    with open(DATA_FILE, "w", newline="") as f:
        fieldnames = ["CID", "Type", "Offer", "Used", "User_ID"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Log retrieval
def log_retrieval(user, cid, type_val, offer_val):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, user, cid, type_val, offer_val])

# Verify username
def verify_user():
    user = username_var.get().strip().lower()
    if user in VALID_USERS:
        status_label.config(text=f"Welcome, {user}", fg="white")
        retrieve_button.config(state="normal")
        if user in RESET_USERS:
            reset_button.config(state="normal")
        else:
            reset_button.config(state="disabled")
    else:
        status_label.config(text="Invalid username", fg="yellow")
        retrieve_button.config(state="disabled")
        reset_button.config(state="disabled")

# Update dropdowns
def update_dropdowns():
    types = sorted(set(row["Type"] for row in data if not row["Used"]))
    offers = sorted(set(row["Offer"] for row in data if not row["Used"]))
    type_dropdown['values'] = types
    offer_dropdown['values'] = offers

# Retrieve CID
def retrieve_cid():
    user = username_var.get().strip().lower()
    selected_type = type_var.get()
    selected_offer = offer_var.get()

    for row in data:
        if row["Type"] == selected_type and row["Offer"] == selected_offer and not row["Used"]:
            row["Used"] = "Yes"
            row["User_ID"] = user
            save_data(data)
            log_retrieval(user, row["CID"], selected_type, selected_offer)
            cid_output_var.set(row["CID"])
            status_label.config(text=f"Retrieved CID: {row['CID']}", fg="white")
            update_dropdowns()
            return

    cid_output_var.set("")
    status_label.config(text="No available CID for selected filters", fg="yellow")

# Reset data
def reset_data():
    for row in data:
        row["Used"] = ""
        row["User_ID"] = ""
    save_data(data)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    update_dropdowns()
    cid_output_var.set("")
    status_label.config(text="Data and log reset successfully", fg="white")

# Copy CID to clipboard
def copy_cid():
    cid = cid_output_var.get()
    if cid:
        root.clipboard_clear()
        root.clipboard_append(cid)
        status_label.config(text=f"CID {cid} copied to clipboard", fg="lightgreen")

# GUI setup
data = load_data()
root = tk.Tk()
root.title("VIT Data Retriever")
root.geometry("520x540")
root.configure(bg="#e60000")  # Vodafone red

# Container frame
container = tk.Frame(root, bg="white", bd=2, relief="groove")
container.pack(pady=20, padx=20, fill="both", expand=True)

# Heading
tk.Label(container, text="VIT Data Retriever", bg="white", fg="#e60000", font=("Arial", 18, "bold")).pack(pady=10)

# Username entry
tk.Label(container, text="Enter Username:", bg="white", fg="#ff6a00", font=("Arial", 12)).pack()
username_var = tk.StringVar()
username_entry = tk.Entry(container, textvariable=username_var, font=("Arial", 12), bg="white", fg="black", bd=2, relief="groove")
username_entry.pack(pady=5)

verify_button = tk.Button(container, text="Verify", command=verify_user,
                          bg="#e60000", fg="white", font=("Arial", 12, "bold"),
                          activebackground="#ff6a00", activeforeground="white", bd=0)
verify_button.pack(pady=5)

# Dropdowns
type_var = tk.StringVar()
offer_var = tk.StringVar()

tk.Label(container, text="Select Type:", bg="white", fg="#ff6a00", font=("Arial", 12)).pack()
type_dropdown = ttk.Combobox(container, textvariable=type_var, font=("Arial", 12))
type_dropdown.pack(pady=5)

tk.Label(container, text="Select Offer:", bg="white", fg="#ff6a00", font=("Arial", 12)).pack()
offer_dropdown = ttk.Combobox(container, textvariable=offer_var, font=("Arial", 12))
offer_dropdown.pack(pady=5)

# Retrieve button
retrieve_button = tk.Button(container, text="Retrieve CID", command=retrieve_cid,
                            bg="#e60000", fg="white", font=("Arial", 12, "bold"),
                            activebackground="#ff6a00", activeforeground="white", bd=0)
retrieve_button.pack(pady=10)
retrieve_button.config(state="disabled")

# CID output + copy
cid_output_var = tk.StringVar()
tk.Label(container, text="Retrieved CID:", bg="white", fg="#ff6a00", font=("Arial", 12)).pack()
cid_output_entry = tk.Entry(container, textvariable=cid_output_var, font=("Arial", 12),
                            state="readonly", justify="center", bg="white", fg="black",
                            relief="groove", bd=2)
cid_output_entry.pack(pady=5)

copy_button = tk.Button(container, text="Copy CID", command=copy_cid,
                        bg="#ff6a00", fg="white", font=("Arial", 12, "bold"),
                        activebackground="#e60000", activeforeground="white", bd=0)
copy_button.pack(pady=5)

# Reset button
reset_button = tk.Button(container, text="Reset All", command=reset_data,
                         bg="#ff6a00", fg="white", font=("Arial", 12, "bold"),
                         activebackground="#e60000", activeforeground="white", bd=0)
reset_button.pack(pady=5)
reset_button.config(state="disabled")

# Status label
status_label = tk.Label(container, text="", bg="white", fg="black", font=("Arial", 10, "italic"))
status_label.pack(pady=10)

update_dropdowns()
root.mainloop()