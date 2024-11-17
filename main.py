import tkinter as tk
from tkinter import messagebox
import csv
import os

CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
clients = []

def _initialize_clients_from_storage():
    if not os.path.exists(CLIENT_TABLE):
        with open(CLIENT_TABLE, mode='w') as f:
            pass

    with open(CLIENT_TABLE, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
        for row in reader:
            clients.append(row)

def _save_clients_to_storage():
    tmp_table_name = '{}.tmp'.format(CLIENT_TABLE)
    with open(tmp_table_name, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
        writer.writerows(clients)

    os.remove(CLIENT_TABLE)
    os.rename(tmp_table_name, CLIENT_TABLE)

def create_client(client):
    if client not in clients:
        clients.append(client)
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client already is in the client's list")

def list_clients():
    list_window = tk.Toplevel()
    list_window.title("Clients List")

    tk.Label(list_window, text='uid | name | company | email | position ').pack()
    tk.Label(list_window, text='*' * 50).pack()

    for idx, client in enumerate(clients):
        client_info = '{uid} | {name} | {company} | {email} | {position}'.format(
            uid=idx,
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']
        )
        tk.Label(list_window, text=client_info).pack()

def update_client(client_id, updated_client):
    if 0 <= client_id < len(clients):
        clients[client_id] = updated_client
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client is not in client's list")

def delete_client(client_id):
    if 0 <= client_id < len(clients):
        clients.pop(client_id)
        _save_clients_to_storage()
    else:
        messagebox.showerror("Error", "Client is not in client's list")

def search_client(client_name):
    for client in clients:
        if client['name'] == client_name:
            messagebox.showinfo("Search Result", f"The client '{client_name}' is in the client's list")
            return True
    messagebox.showinfo("Search Result", f"The client '{client_name}' is not in our clients list")
    return False

class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Client Management")
        self.geometry("400x400")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="WELCOME TO MY STORE", font=('Helvetica', 16)).pack(pady=10)
        tk.Label(self, text="What would you like to do today?", font=('Helvetica', 14)).pack(pady=10)

        tk.Button(self, text="Create client", command=self.create_client).pack(pady=5)
        tk.Button(self, text="List clients", command=list_clients).pack(pady=5)
        tk.Button(self, text="Update client", command=self.update_client).pack(pady=5)
        tk.Button(self, text="Delete client", command=self.delete_client).pack(pady=5)
        tk.Button(self, text="Search client", command=self.search_client).pack(pady=5)

    def create_client(self):
        self._open_form_window("Create Client", self._create_client_callback)

    def update_client(self):
        client_id = self._get_client_id()
        if client_id is not None:
            self._open_form_window("Update Client", self._update_client_callback, client_id)

    def delete_client(self):
        client_id = self._get_client_id()
        if client_id is not None:
            delete_client(client_id)
            list_clients()

    def search_client(self):
        client_name = self._get_client_name()
        if client_name:
            search_client(client_name)

    def _create_client_callback(self, form_window, client_id=None):
        client = {
            "name": self.name_var.get(),
            "company": self.company_var.get(),
            "email": self.email_var.get(),
            "position": self.position_var.get()
        }
        if client_id is None:
            create_client(client)
        else:
            update_client(client_id, client)
        form_window.destroy()
        list_clients()

    def _update_client_callback(self, form_window, client_id):
        self._create_client_callback(form_window, client_id)

    def _open_form_window(self, title, callback, client_id=None):
        form_window = tk.Toplevel(self)
        form_window.title(title)

        self.name_var = tk.StringVar()
        self.company_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.position_var = tk.StringVar()

        tk.Label(form_window, text="Name").pack()
        tk.Entry(form_window, textvariable=self.name_var).pack()

        tk.Label(form_window, text="Company").pack()
        tk.Entry(form_window, textvariable=self.company_var).pack()

        tk.Label(form_window, text="Email").pack()
        tk.Entry(form_window, textvariable=self.email_var).pack()

        tk.Label(form_window, text="Position").pack()
        tk.Entry(form_window, textvariable=self.position_var).pack()

        tk.Button(form_window, text="Submit", command=lambda: callback(form_window, client_id)).pack()

    def _get_client_id(self):
        try:
            return int(input("What is the client id? "))
        except ValueError:
            messagebox.showerror("Invalid ID", "Please enter a numeric value.")
            return None

    def _get_client_name(self):
        client_name = input("What is the client name? (type 'exit' to quit): ")
        if client_name.lower() == 'exit':
            sys.exit()
        return client_name

if __name__ == "__main__":
    _initialize_clients_from_storage()
    app = ClientApp()
    app.mainloop()
    _save_clients_to_storage()

