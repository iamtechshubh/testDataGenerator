"""
Author: Shubham Pimple
"""
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from faker import Faker
import pandas as pd

fake = Faker()

def generate_data():
    try:
        num_entries = int(entry_num_entries.get())
        if num_entries <= 0:
            raise ValueError

        # data = {
        #     "Name": [fake.name() if var_name.get() else "" for _ in range(num_entries)],
        #     "Email": [fake.email() if var_email.get() else "" for _ in range(num_entries)],
        #     "Phone Number": [fake.phone_number() if var_phone.get() else "" for _ in range(num_entries)],
        #     "Address": [fake.address() if var_address.get() else "" for _ in range(num_entries)],
        #     "Date": [fake.date() if var_date.get() else "" for _ in range(num_entries)],
        # }

        data = {
            "Name": [fake.name() if var_name.get() else "" for _ in range(num_entries)]
        }

        # Splitting name into first and last names for email
        if var_email.get():
            emails = []
            for name in data["Name"]:
                if name:
                    fname, lname = name.split()[:2]  # Extract first and last name
                    email = f"{fname.lower()}.{lname.lower()}@example.com"
                else:
                    email = fake.email()  # If no name, generate random email
                emails.append(email)
            data["Email"] = emails

        # fname, lname = name.split()[:2]  # Extract first and last name
        # domain = fake.free_email_domain()  # Get a random email domain
        # email = f"{fname.lower()}.{lname.lower()}@{domain}"

        # Other fields
        data["Phone Number"] = [fake.phone_number() if var_phone.get() else "" for _ in range(num_entries)]
        data["Address"] = [fake.address() if var_address.get() else "" for _ in range(num_entries)]
        data["Date"] = [fake.date() if var_date.get() else "" for _ in range(num_entries)]

        df = pd.DataFrame(data)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, df.to_string(index=False))
        global generated_data
        generated_data = df
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

def save_to_csv():
    # try:
    #     if generated_data.empty:
    #         raise ValueError
    #     file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    #     if file_name:
    #         generated_data.to_csv(file_name, index=False)
    #         messagebox.showinfo("Success", "Data saved successfully!")
    # except (ValueError, AttributeError):
    #     messagebox.showerror("Error", "No data to save. Please generate data first.")
    global generated_data
    if generated_data.empty:
        messagebox.showwarning("Warning", "No data to save!")
        return

    # Ensure the 'output' directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, "generated_data.csv")
    generated_data.to_csv(file_path, index=False)
    messagebox.showinfo("Success", f"Data saved to {file_path}")

def clear_data():
    entry_num_entries.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    for var in [var_name, var_email, var_phone, var_address, var_date]:
        var.set(False)
    global generated_data
    generated_data = pd.DataFrame()
    messagebox.showinfo("Cleared", "All data has been cleared.")

root = tk.Tk()
root.title("Test Data Generator")
root.geometry("650x500")

frame_inputs = tk.Frame(root)
frame_inputs.grid(row=0, column=0, padx=10, pady=10)

frame_checkboxes = tk.Frame(root)
frame_checkboxes.grid(row=1, column=0, padx=10, pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.grid(row=2, column=0, padx=10, pady=10)

frame_output = tk.Frame(root)
frame_output.grid(row=3, column=0, padx=10, pady=10)

label_num_entries = tk.Label(frame_inputs, text="Enter number of entries:")
label_num_entries.grid(row=0, column=0, padx=5, pady=5)
entry_num_entries = tk.Entry(frame_inputs)
entry_num_entries.grid(row=0, column=1, padx=5, pady=5)

generate_button = tk.Button(frame_inputs, text="Generate Data", command=generate_data)
generate_button.grid(row=0, column=2, padx=5, pady=5)

var_name, var_email, var_phone, var_address, var_date = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
checkboxes = [
    ("Generate Names", var_name),
    ("Generate Emails", var_email),
    ("Generate Phone Numbers", var_phone),
    ("Generate Addresses", var_address),
    ("Generate Dates", var_date)
]
for i, (text, var) in enumerate(checkboxes):
    tk.Checkbutton(frame_checkboxes, text=text, variable=var).grid(row=i, column=0, sticky="w")

result_text = tk.Text(frame_output, height=12, width=80)
result_text.grid(row=0, column=0)

save_button = tk.Button(frame_buttons, text="Save to CSV", command=save_to_csv)
save_button.grid(row=0, column=0, padx=5, pady=5)
clear_button = tk.Button(frame_buttons, text="Clear Data", command=clear_data)
clear_button.grid(row=0, column=1, padx=5, pady=5)

generated_data = pd.DataFrame()
root.mainloop()
