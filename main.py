clients = "pablo,ricardo,"

def create_cliente(client_name):
    global clients

    if client_name not in clients:
        clients += client_name
        _add_comma()
    else:
        print("Client already is in the clients list")


def list_clints():
    global clients

    print(clients)


def update_client(cliente_name, updated_client_name):
    global clients
    if cliente_name in clients:
        clients = clients.replace(client_name + ",", updated_client_name + ",")
    else:
        print("Client is not in clients list")
def delete_client(client_name):
    global clients
    if client_name in clients:
        clients = clients.replace(client_name + ",", "")
    else:
        print("Client is not in clients list")
def _add_comma():
    global clients

    clients += ","


def _print_welcom():
    print("WELCONE TO MY STORE")
    print("*" * 50)
    print("What world you like to do today?")
    print("[C]reate clint")
    print("[U]pdate client")
    print("[D]elete client")

def _get_client_name():
    return input("What is the client name?")

if __name__ == "__main__":
    _print_welcom()

    Command = input()
    Command = Command.upper()

    if Command == "C":
        client_name = _get_client_name()
        create_cliente(client_name)
        list_clints()
    elif Command == "D":
        client_name = _get_client_name()
        delete_client(client_name)
    elif Command == 'U':
        client_name = _get_client_name()
        updated_client_name = input("What is the updated client name")
        update_client(client_name, updated_client_name)
    else:
        print("Invalid command")

