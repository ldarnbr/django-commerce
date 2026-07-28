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

def checkout_basket(client):
    # Server side handles checks for stock, updating the db and serving the success/fail messages.
    server_response = client.post(f"{URL}/checkout/")

    if server_response.status_code == 200:
        print(f"{server_response.json()['message']}")
        return True
    else:
        print(f"{server_response.json()['error']}")
        return False

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
            successful_checkout = checkout_basket(client)
            if successful_checkout:
                return
            else:
                # This should only happen if the item is out of stock.
                # Allows the user to update their basket because of this.
                view_basket(client)

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

def view_orders(client):
    server_response = client.get(f"{URL}/view_orders/")

    if server_response.status_code == 200:
        orders = server_response.json()

        if len(orders) == 0:
            print("\nNo order history\n")
            return
        for order in orders:
            print(f"\nOrder ID: {order['order_id']}:")
            combined_total = 0.0

            for item in order['items']:
                print(f"{item['quantity']} x {item['name']} - {item['price']}/ea")
                combined_total += (float(item['price']) * int(item['quantity']))

            print(f"Order Total: £{combined_total:.2f}")
            print("\n -----------------------------------------------------------")
    else:
        error_message = server_response.json()['error']
        print("Error: ", error_message)

    return

def browse_products(client):
    while True:
        print("Product pages-----------------------------------")
        print("1) View All")
        print("2) Search Items")
        print("3) Sale")
        print("4) Home\n")

        command = input("Please select a command: \n")

        # Default endpoint just serves all available items.
        # If statement switches to show the relevant items based on URL.
        search_url = f"{URL}/shopping/"

        if command == '1':
            # The default behaviour of the application is to show all items.
            pass
        elif command == '2':
            user_search = input("Please input your search terms: ")
            search_url = f"{URL}/shopping/?search={user_search}"
        elif command == '3':
            search_url = f"{URL}/sale/"
        elif command == '4':
            return
        else:
            print("Error: command not found. Usage examples: | Enter <1> to see all items | Enter <3> to view items on sale |")
            continue

        server_response = client.get(search_url)
        if server_response.status_code == 200:
            items = server_response.json()
            if len(items) == 0:
                print("\nThere are no products available at the moment. Please check back later.\n")
                continue

            print("\n All items:")
            for item in items:
                # Don't show out of stock items.
                if int(item['stock_count']) <= 0:
                    print(f"ID: {item['id']} | {item['name']} - *Out of stock*")
                else:
                    if float(item['sale_discount']) > 0:
                        # Discount is stored as a decimal.
                        new_price = float(item['price']) * (1 - float(item['sale_discount']))
                        percentage_discount = int(float(item['sale_discount']) * 100)
                        print(f"ID: {item['id']} | {item['name']} - *SALE PRICE {percentage_discount}% OFF:* £{new_price:.2f}/ea ({item['stock_count']} in stock!)")
                    else:
                        print(f"ID: {item['id']} | {item['name']} - £{item['price']}/ea ({item['stock_count']} in stock!)")

            print("\n---------------------------------------------\n")
            inspect_item = input("Input an Item ID to view details before adding to cart. Press 'Enter' to return to browsing options.: ")

            if inspect_item:
                item_details_response = client.get(f"{URL}/items/{inspect_item}/")

                if item_details_response.status_code == 200:
                    item_details = item_details_response.json()
                    qty_in_stock = int(item_details['stock_count'])
                    normal_price = float(item_details['price'])
                    discount = float(item_details['sale_discount'])
                    final_price = normal_price - (discount * normal_price) if discount > 0 else normal_price

                    print(f"\n-----------------------------------------------------------")
                    print(f"Product Title: {item_details['name']}")
                    print(f"Product Description: {item_details['description']}")

                    if qty_in_stock <= 0:
                        print("*OUT OF STOCK*")
                        print("This item cannot be added to your basket.")
                    else:
                        print(f"Price: £{final_price:.2f}" + (f"({discount * 100}% Off!)" if discount > 0 else ""))
                        print(f"Quantity in stock: {item_details['stock_count']}")
                        print(f"-----------------------------------------------------------")

                        add_to_basket = input("Add this item to your basket? (y/n): ")
                        # Might as well support uppercase.
                        if add_to_basket.lower() == 'y':
                            item_id_json = {"item_id": int(inspect_item)}
                            add_to_basket_response = client.post(f"{URL}/shopping_basket/", json=item_id_json)
                            if add_to_basket_response.status_code == 200:
                                print(f"\n{add_to_basket_response.json()['message']}")
                            else:
                                error_message = add_to_basket_response.json()['error']
                                print("Error: ", error_message)
                else:
                    print(f"\nError: Could not find item with ID: {inspect_item}")
        else:
            print("Could not load products at this time, check back later.")


def main():
    # Creates a session to keep the user logged in
    client = requests.Session()

    # Flag keeps track of if a user is logged in to dynamically present login/logout buttons.
    logged_in = None

    print("\n")

    while True:
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
            browse_products(client)

        elif command == '4':
            if logged_in:
                print("\nOrder History----------------------")
                view_orders(client)

            # If the user isnt logged in, they can't view previous orders.
            else:
                print("\nError: command not found. Usage examples: | Enter <1> for login | Enter <exit> to close application |")

        elif command == 'exit':
            print("\nExit Message------------------------")
            break
        else:
            print("\nError: command not found. Usage examples: | Enter <1> for login | Enter <exit> to close application |")

if __name__ == '__main__':
    main()