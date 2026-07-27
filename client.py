import requests

URL = 'http://127.0.0.1:8000/api'

def login(client):
    # Prompt the user for login info.
    username = input("Enter your username: \n")
    password = input("Enter your password: \n")

    # Package the credentials in a dictionary.
    credentials = {
        "username": username,
        "password": password
    }

    # Post the credentials and capture the response from the server.
    server_response = client.post(f"{URL}/login/", json=credentials)

    # Convert the JSON to a python dictionary to read the response message.
    if server_response.status_code == 200:
        response_message = server_response.json()['message']
        print(response_message)
        return username
    else:
        error_message = server_response.json()['error']
        print("Error: ", error_message)
        return None

def logout(client):
    client.post(f"{URL}/logout/")
    client.cookies.clear()
    print("Logged out successfully.")
    return None

def register(client):
    # Prompt the user for login info.
    username = input("Create a unique username: \n")
    password = input("Create a password \n")

    # Package the credentials in a dictionary.
    credentials = {
        "username": username,
        "password": password
    }

    # Post the credentials and capture the response from the server.
    server_response = client.post(f"{URL}/register/", json=credentials)

    # Convert the JSON to a python dictionary to read the response message.
    if server_response.status_code == 200:
        response_message = server_response.json()['message']
        print(response_message)
        return username
    else:
        error_message = server_response.json()['error']
        print("Error: ", error_message)
        return None

def view_basket(client):

    server_response = client.get(f"{URL}/shopping_basket/")

    if server_response.status_code == 200:
        items = server_response.json()
        if (len(items) == 0):
            # Return to main menu if the basket is empty, nothing to checkout.
            print("Your shopping basket is empty.\n")
            return

        basket_total = 0.0
        for item in items:
            print(f"ID: {item['item_id']} | {item['quantity']} x {item['name']} - {item['price']}/ea")
            basket_total += (float(item['price']) * int(item['quantity']))

        print(f"\nCombined Total: £{basket_total:.2f}\n")

        print("Options:")
        print("1) Checkout")
        print("2) Remove an item")
        print("3) Return to Main Menu")

        command = input(": ")

        if command == '1':
            print("Checkout not yet available")

        # Item quantities can be reduced one at a time by inputting the ID.
        # Function has recursion to prompt the customer for another action until they're finished.
        elif command == '2':
            item_to_reduce = input("\nEnter the ID of the item you would like to remove: ")
            deleted_item = {"item_id": item_to_reduce}

            server_response = client.delete(f"{URL}/shopping_basket/", json=deleted_item)
            if server_response.status_code == 200:
                print(f"{server_response.json()['message']}")
                view_basket(client)
            else:
                print(f"Error: {server_response.json()['error']}")
        
        elif command == '3':
            return
        else:
            print("Error: Invalid command, please input a number from the presented options.")
            view_basket(client)

    else:
        error_message = server_response.json()['error']
        print("Error: ", error_message)

def main():
    # Creates a session to keep the user logged in
    client = requests.Session()

    # Flag keeps track of if a user is logged in to dynamically present login/logout buttons.
    logged_in = None

    while True:
        print("\n")
        if logged_in:
            print("1) Logout")
            print("2) Check Basket")
            print("3) Browse Products")
            print("4) View Order History")
            print("exit) Close Application\n")
        else:
            print("1) Login")
            print("2) Register")
            print("3) Browse Products")
            print("exit) Close Application\n")

        command = input("Please select a command: \n")

        # This command is either login or logout depending on if a user is logged in or not.
        # Only logged in users can see their basket and make purchases.
        if command == '1':
            if logged_in:
                print("\nLogout Screen -------------------\n")
                logged_in = logout(client)
            else:
                print("\nLogin Screen --------------------\n")
                logged_in = login(client)

        # This command is either register or check basket depending on if a user is logged in or not.
        elif command == '2':
            if logged_in:
                print("\nBasket Screen -----------------\n")
                view_basket(client)
            else:
                print("\nRegister Screen ------------------\n")
                logged_in = register(client)
   
        elif command == '3':
            print("\nShopping Screen----------------------")
            # Needs to have sale filter functionality as well as search.
        elif command == 'exit':
            print("\nExit Message------------------------")
            break
        else:
            print("\nError: command not found. Usage examples: | Enter <1> for login | Enter <exit> to close application |")

if __name__ == '__main__':
    main()