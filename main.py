import tkinter as tk
from tkinter import messagebox
import csv
import os
import re 

# Constants for the client table and schema
CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'phone', 'email', 'position']
clients = []

# Initialize the client data from storage
def _initialize_clients_from_storage():
    if not os.path.exists(CLIENT_TABLE):
        with open(CLIENT_TABLE, mode='w') as f:
            pass

    with open(CLIENT_TABLE, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
        for row in reader:
            clients.append(row)

# Save the client data to storage
def _save_clients_to_storage():
    tmp_table_name = '{}.tmp'.format(CLIENT_TABLE)
    with open(tmp_table_name, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
        writer.writerows(clients)

    os.remove(CLIENT_TABLE)
    os.rename(tmp_table_name, CLIENT_TABLE)

# Create a new client
def create_client(client):
    if client not in clients:
        clients.append(client)
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client already is in the client's list")

# List all clients in a new window
def list_clients():
    list_window = tk.Toplevel()
    list_window.title("Clients List")

    tk.Label(list_window, text='uid | name | company | phone | email | position ').pack()
    tk.Label(list_window, text='*' * 80).pack()

    for idx, client in enumerate(clients):
        client_info = '{uid} | {name} | {company} | {phone} | {email} | {position}'.format(
            uid=idx,
            name=client['name'],
            company=client['company'],
            phone=client['phone'],
            email=client['email'],
            position=client['position']
        )
        tk.Label(list_window, text=client_info).pack()

# Update an existing client
def update_client(client_id, updated_client):
    if 0 <= client_id < len(clients):
        clients[client_id] = updated_client
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client is not in client's list")

# Delete an existing client
def delete_client(client_id):
    if 0 <= client_id < len(clients):
        clients.pop(client_id)
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client is not in client's list")

# Search for a client by name
def search_client(client_name):
    for client in clients:
        if client['name'] == client_name:
            messagebox.showinfo("Search Result", f"The client '{client_name}' is in the client's list")
            return True
    messagebox.showinfo("Search Result", f"The client '{client_name}' is not in our clients list")
    return False

# Main application class
class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Client Management")
        self.geometry("400x400")

        self.create_widgets()

    # Create the main widgets in the application
    def create_widgets(self):
        tk.Label(self, text="WELCOME TO MY STORE", font=('Helvetica', 16)).pack(pady=10)
        tk.Label(self, text="What would you like to do today?", font=('Helvetica', 14)).pack(pady=10)

        tk.Button(self, text="Create client", command=self.create_client).pack(pady=5)
        tk.Button(self, text="List clients", command=list_clients).pack(pady=5)
        tk.Button(self, text="Update client", command=self.update_client).pack(pady=5)
        tk.Button(self, text="Delete client", command=self.delete_client).pack(pady=5)
        tk.Button(self, text="Search client", command=self.search_client).pack(pady=5)

    # Open the form window to create a client
    def create_client(self):
        self._open_form_window("Create Client", self._create_client_callback)

    # Open the form window to update a client
    def update_client(self):
        client_id = self._get_client_id()
        if client_id is not None:
            self._open_form_window("Update Client", self._update_client_callback, client_id)

    # Delete a client
    def delete_client(self):
        client_id = self._get_client_id()
        if client_id is not None:
            delete_client(client_id)
            list_clients()

    # Open the search window to search for a client
    def search_client(self):
        self._open_search_window("Search Client", self._search_client_callback)

    # Callback function to create or update a client
    def _create_client_callback(self, form_window, client_id=None):
        client = {
            "name": self.name_var.get(),
            "company": self.company_var.get(),
            "phone": self.phone_var.get(),
            "email": self.email_var.get(),
            "position": self.position_var.get()
        }

        # Validate phone number (must start with + and have 10-15 digits)
        if not re.match(r'^\+\d{9,12}$', client["phone"]):
            messagebox.showerror("Invalid Phone", "Phone number must start with + and contain 10-15 digits.")
            return

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', client["email"]):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if client_id is None:
            create_client(client)
        else:
            update_client(client_id, client)
        form_window.destroy()
        list_clients()

    # Wrapper for the update callback to reuse the create callback
    def _update_client_callback(self, form_window, client_id):
        self._create_client_callback(form_window, client_id)

    # Open a form window for client data entry
    def _open_form_window(self, title, callback, client_id=None):
        form_window = tk.Toplevel(self)
        form_window.title(title)

        self.name_var = tk.StringVar()
        self.company_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.position_var = tk.StringVar()

        if client_id is not None:
            client = clients[client_id]
            self.name_var.set(client['name'])
            self.company_var.set(client['company'])
            self.phone_var.set(client['phone'])
            self.email_var.set(client['email'])
            self.position_var.set(client['position'])

        tk.Label(form_window, text="Name").pack()
        tk.Entry(form_window, textvariable=self.name_var).pack()

        tk.Label(form_window, text="Company").pack()
        tk.Entry(form_window, textvariable=self.company_var).pack()

        tk.Label(form_window, text="Phone").pack()
        tk.Entry(form_window, textvariable=self.phone_var).pack()

        tk.Label(form_window, text="Email").pack()
        tk.Entry(form_window, textvariable=self.email_var).pack()

        tk.Label(form_window, text="Position").pack()
        tk.Entry(form_window, textvariable=self.position_var).pack()

        tk.Button(form_window, text="Submit", command=lambda: callback(form_window, client_id)).pack()

    # Get the client ID from user input
    def _get_client_id(self):
        id_window = tk.Toplevel(self)
        id_window.title("Enter Client ID")

        self.id_var = tk.StringVar()

        id_label = tk.Label(id_window, text="Enter Client ID:")
        id_label.pack(pady=5)

        id_entry = tk.Entry(id_window, textvariable=self.id_var)
        id_entry.pack(pady=5)

        submit_button = tk.Button(id_window, text="Submit", command=id_window.destroy)
        submit_button.pack(pady=5)

        id_window.grab_set()
        self.wait_window(id_window)

        try:
            return int(self.id_var.get())
        except ValueError:
            messagebox.showerror("Invalid ID", "Please enter a numeric value.")
            return None

    # Open a search window for client name input
    def _open_search_window(self, title, callback):
        search_window = tk.Toplevel(self)
        search_window.title(title)

        self.search_var = tk.StringVar()

        tk.Label(search_window, text="Name").pack()
        tk.Entry(search_window, textvariable=self.search_var).pack()

        tk.Button(search_window, text="Submit", command=lambda: callback(search_window)).pack()

    # Callback function for searching a client
    def _search_client_callback(self, search_window):
        client_name = self.search_var.get()
        search_client(client_name)
        search_window.destroy()

if __name__ == "__main__":
    # Initialize and run the application
    _initialize_clients_from_storage()
    app = ClientApp()
    app.mainloop()
    _save_clients_to_storage()
