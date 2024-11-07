from setuptools import Command
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
def _add_comma():
    global clients
    clients += ","
def _print_welcom():
    print("WELCONE TO MY STORE")
    print("*" * 50)
    print("What world you like to do today?")
    print("[C]reate clint")
    print("[D]elete client")
if __name__ == "__main__":
    _print_welcom()
    Command = input()
    if Command == "c":
        client_name = input("What is the client name?")
        create_cliente(client_name)
        list_clints()
    elif Command == "d":
        pass
    else:
        print("Invalid command")
    print(clients)