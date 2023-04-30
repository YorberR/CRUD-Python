import sys

clients = [
    {
        "name":"Pablo",
        "company": "Google",
        "email": "pablo@email.com",
        "position": "Software engineer"
    },
    {
        "name":"Ricardo",
        "company": "Meta",
        "email": "ricardo@email.com",
        "position": "Data engineer"
    }
]


def create_cliente(client):
    global clients

    if client not in clients:
        clients.append(client)
    else:
        print("Client already is in the client\'s list")


def list_clints():
    for idx, client in enumerate(clients):
        print('{uid} | {name} | {company} | {email} | {position}'.format(
            uid = idx,
            name = client['name'],
            company = client['company'],
            email = client['email'],
            position = client['position']
        ))


def update_client(cliente_name, updated_client_name):
    global clients

    if cliente_name in clients:
        clients = clients.replace(client_name + ",", updated_client_name + ",")
    else:
        print("Client is not in client\'s list")


def delete_client(client_name):
    global clients

    if client_name in clients:
        clients = clients.replace(client_name + ",", "")
    else:
        print("Client is not in client\'s list")


def search_client(client_name):
    client_list = clients.split(",")

    for client in client_list:
        if client != client_name:
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
        client_name = _get_client_name()
        delete_client(client_name)
    elif Command == "U":
        client_name = _get_client_name()
        updated_client_name = input("What is the updated client name")
        update_client(client_name, updated_client_name)
    elif Command == "S":
        client_name = _get_client_name()
        found = search_client(client_name)

        if found:
            print("The client is in the client\'s list")
        else:
            print("The client: {} is not in our clients list".format(client_name))
    else:
        print("Invalid command")

    print(clients)