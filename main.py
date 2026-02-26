import os
import json


class Product:
    inventory = {}

    def __init__(self, product_id, name, category, quantity, price, supplier):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        Product.inventory[self.product_id] = self

    @classmethod
    def add_product(cls, name, category, quantity, price, supplier):
        """Creates a new product with an auto-incremented ID and saves to JSON."""
        new_id = max(cls.inventory.keys(), default=0) + 1
        new_product = cls(new_id, name, category, quantity, price, supplier)
        cls.save_to_json()  # syncs with json
        return f"Success: Added {name} (ID: {new_id})"

    @classmethod
    def delete_product(cls, product_id):
        if product_id in cls.inventory:
            del cls.inventory[product_id]
            cls.save_to_json()   #syncs with json
            return "Product deleted successfully"
        else:
            return "Product not found"

    @classmethod
    def update_product(cls, product_id, quantity=None, price=None, supplier=None):
        """Updates product details and syncs with JSON."""
        if product_id in cls.inventory:
            product = cls.inventory[product_id]
            if quantity is not None: product.quantity = int(quantity)
            if price is not None: product.price = float(price)
            if supplier is not None: product.supplier = str(supplier)
            cls.save_to_json() # syncs with json
            return "Product updated successfully."
        return "Error: Product not found."

    @classmethod
    def save_to_json(cls, filename="inventory.json"):
        data = []
        for p in cls.inventory.values():
            data.append(p.__dict__) # Converts object attributes to a dictionary
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Inventory saved to {filename}"

    @classmethod
    def load_from_json(cls, filename="inventory.json"):
        """Reads JSON and recreates Product objects."""
        if not os.path.exists(filename):
            return "No saved data found."
        
        with open(filename, 'r') as f:
            data = json.load(f)
            cls.inventory = {} # Clear current memory
            for item in data:
                # This automatically calls __init__ and refills cls.inventory
                cls(**item) 
        return "Inventory loaded successfully."
    
class Order:
    _order_counter = 1 # Protected class variable

    def __init__(self, customer_info=None):
        self.order_id = Order._order_counter
        Order._order_counter += 1
        self.items = [] # List of tuples (product_name, quantity, subtotal)
        self.customer_info = customer_info
        self.total_price = 0.0

    def add_to_order(self, product_id, quantity):
        if product_id not in Product.inventory:
            return "Error: Product not found."
        
        prod = Product.inventory[product_id]
        if prod.quantity >= quantity:
            prod.quantity -= quantity
            subtotal = prod.price * quantity
            self.items.append((prod.name, quantity, subtotal))
            self.total_price += subtotal
            return f"Added {quantity}x {prod.name} to Order #{self.order_id}"
        return "Error: Insufficient stock."
    
# Sample usage
if __name__ == "__main__":
    # 1. Load existing data
    print(Product.load_from_json())

    # 2. Add a product if inventory is empty
    if not Product.inventory:
        print(Product.add_product("Gaming Mouse", "Peripherals", 100, 49.99, "Logitech"))

    # 3. Process an order
    my_order = Order(customer_info="Alice")
    print(my_order.add_to_order(product_id=1, quantity=2))
    
    print(f"Final Inventory Count: {Product.inventory[1].quantity}")    