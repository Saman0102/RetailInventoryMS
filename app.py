from main import Product, Order
def main_menu():
    print(Product.load_from_json())

    while True:
        print("\n--- Inventory Management System ---")
        print("1. View Inventory")
        print("2. Add New Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Create New Order")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ")

        if choice == '1':
            if not Product.inventory:
                print("\nInventory is currently empty.")
            for p in Product.inventory.values():
                print(f"ID: {p.product_id} | Name: {p.name} | Stock: {p.quantity} | Price: ${p.price}")

        elif choice == '2':
            name = input("Enter product name: ")
            cat = input("Enter category: ")
            qty = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            supp = input("Enter supplier: ")
            print(Product.add_product(name, cat, qty, price, supp))

        elif choice == '3':
            p_id = int(input("Enter Product ID to update: "))
            print("Leave blank to keep current value.")
            u_qty = input("New quantity: ")
            u_price = input("New price: ")
            
            qty = int(u_qty) if u_qty else None
            prc = float(u_price) if u_price else None
            
            print(Product.update_product(p_id, quantity=qty, price=prc))

        elif choice == '4':
            p_id = int(input("Enter Product ID to delete: "))
            confirm = input(f"Are you sure you want to delete ID {p_id}? (y/n): ")
            if confirm.lower() == 'y':
                print(Product.delete_product(p_id))

        elif choice == '5':
            customer = input("Enter customer name: ")
            new_order = Order(customer_info=customer)
            p_id = int(input("Enter Product ID to purchase: "))
            qty = int(input("Enter quantity: "))
            print(new_order.add_to_order(p_id, qty))

        elif choice == '6':
            print("Saving data and exiting... Goodbye!")
            Product.save_to_json()
            break

        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main_menu()