import sys
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
    else:
        print("Client already is in the client's list")

def list_clients():
    print('uid | name | company | email | position ')
    print('*'*50)

    for idx, client in enumerate(clients):
        print('{uid} | {name} | {company} | {email} | {position}'.format(
            uid=idx,
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']
        ))

def update_client(client_id, updated_client):
    if 0 <= client_id < len(clients):
        clients[client_id] = updated_client
    else:
        print("Client is not in client's list")

def delete_client(client_id):
    if 0 <= client_id < len(clients):
        clients.pop(client_id)
    else:
        print("Client is not in client's list")

def search_client(client_name):
    for client in clients:
        if client['name'] == client_name:
            return True
    return False

def _print_welcome():
    print("WELCOME TO MY STORE")
    print("*" * 50)
    print("What would you like to do today?")
    print("[C]reate client")
    print("[L]ist clients")
    print("[U]pdate client")
    print("[D]elete client")
    print("[S]earch client")

def _get_client_field(field_name):
    field = None
    while not field:
        field = input(f"What is the client {field_name}? ")
    return field

def _get_client_id():
    client_id = None
    while client_id is None:
        try:
            client_id = int(input("What is the client id? "))
        except ValueError:
            print("Invalid ID. Please enter a numeric value.")
    return client_id

def _get_client_name():
    client_name = input("What is the client name? (type 'exit' to quit): ")
    if client_name.lower() == 'exit':
        sys.exit()
    return client_name

def main():
    _initialize_clients_from_storage()
    _print_welcome()

    command = input().upper()

    if command == "C":
        client = {
            "name": _get_client_field('name'),
            "company": _get_client_field('company'),
            "email": _get_client_field('email'),
            "position": _get_client_field('position'),
        }
        create_client(client)
        list_clients()
    elif command == "L":
        list_clients()
    elif command == "D":
        client_id = _get_client_id()
        delete_client(client_id)
        list_clients()
    elif command == "U":
        client_id = _get_client_id()
        updated_client = {
            "name": _get_client_field('name'),
            "company": _get_client_field('company'),
            "email": _get_client_field('email'),
            "position": _get_client_field('position'),
        }
        update_client(client_id, updated_client)
        list_clients()
    elif command == "S":
        client_name = _get_client_name()
        if search_client(client_name):
            print(f"The client '{client_name}' is in the client's list")
        else:
            print(f"The client '{client_name}' is not in our clients list")
    else:
        print("Invalid command")

    _save_clients_to_storage()

if __name__ == "__main__":
    main()
