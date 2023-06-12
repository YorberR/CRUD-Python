import sys
import csv
import os

CLIENT_TABLE ='.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
clients = []

def _initialize_clients_from_storage():
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


def create_cliente(client):
    global clients

    if client not in clients:
        clients.append(client)
    else:
        print("Client already is in the client\'s list")


def list_clints():
    print('uid | name | company | email | position ')
    print('*'*50)

    for idx, client in enumerate(clients):
        print('{uid} | {name} | {company} | {email} | {position}'.format(
            uid = idx,
            name = client['name'],
            company = client['company'],
            email = client['email'],
            position = client['position']
        ))


def update_client(client_id, updated_client):
    global clients

    if len(clients) - 1 >= client_id:
        clients[client_id] = updated_client
    else:
        print("Client is not in client\'s list")


def delete_client(client_id):
    global clients

    for idx, dummy_client in enumerate(clients):
        if idx == client_id:
            del clients[idx]
            break


def search_client(client_name):

    for client in clients:
        if client['name'] != client_name:
            continue
        else:
            return True


def _add_comma():
    global clients

    clients += ","


def _print_welcom():
    print("WELCONE TO MY STORE")
    print("*" * 50)
    print("What world you like to do today?")
    print("[C]reate clint")
    print("[L]ist clients")
    print("[U]pdate client")
    print("[D]elete client")
    print("[S]earch client")


def _get_client_field(field_name):
    field = None

    while not field:
        field = input("What is the client {}?".format(field_name))

    return field


def _get_client_name():
    client_name = None

    while not client_name:
        client_name = input("What is the client name?")

        if client_name == 'exit':
            client_name = None
            break

        if not client_name:
            sys.exit()

    return client_name

if __name__ == "__main__":
    _initialize_clients_from_storage()
    _print_welcom()

    Command = input()
    Command = Command.upper()

    if Command == "C":
        client = {
            "name": _get_client_field('name'),
            "company": _get_client_field('company'),
            "email": _get_client_field('email'),
            "position": _get_client_field('position'),
        }
        create_cliente(client)
        list_clints()
    elif Command == "L":
        list_clints()
    elif Command == "D":
        client_id = int(input('What is the client?'))
        delete_client(client_id)
    elif Command == "U":
        client_id = _get_client_field('id')
        updated_client = input("What is the updated client name?")
        update_client(client_id, updated_client)
    elif Command == "S":
        client_name = _get_client_name()
        found = search_client(client_name)

        if found:
            print("The client is in the client\'s list")
        else:
            print("The client: {} is not in our clients list".format(client_name))
    else:
        print("Invalid command")

    _save_clients_to_storage()