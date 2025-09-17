#E-CART BY *JAIKRRISH *NITIN PRANAV *SRINITHI *MADHAN...
import tkinter as tk
from tkinter import messagebox, simpledialog

# Product Data
PRODUCTS = {
    "Home Accessories": {
        "Sofa": 30000.0,
        "Bed": 5000.0,
        "Blanket": 500.0
    },
    "Electronics": {
        "Laptop": 80000.0,
        "Mobile": 16000.0,
        "TV": 27000.0
    },
    "Groceries": {
        "Vegetables": 100.0,
        "Fruits": 150.0,
        "Grains": 200.0
    }
}

# Global variables
cart = {}
root = None
cart_listbox = None
total_label = None
address_entry = None
shipping_method = None

# Cart Functions
def addToCart(category, product, quantity=1):
    if category in PRODUCTS and product in PRODUCTS[category]:
        cart[product] = cart.get(product, 0) + quantity
    else:
        messagebox.showerror("Error", "Product not available")

def removeFromCart(product):
    if product in cart:
        del cart[product]
    else:
        messagebox.showerror("Error", "Product not in cart")

def calculateTotal():
    total = 0
    for product, quantity in cart.items():
        for category in PRODUCTS:
            if product in PRODUCTS[category]:
                total += PRODUCTS[category][product] * quantity
    return total

def saveOrderSummary(total, filename="orderSummary.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Order Summary:\n")
        for product, quantity in cart.items():
            for category in PRODUCTS:
                if product in PRODUCTS[category]:
                    price = PRODUCTS[category][product] * quantity
                    file.write(f"{product} - Quantity: {quantity} - Price: ₹{price:.2f}\n")
        file.write(f"\nTotal: ₹{total:.2f}\n")

    # Display the contents of the file in a popup message box
    with open(filename, "r", encoding="utf-8") as file:
        summary = file.read()
        messagebox.showinfo("Order Summary", summary)

def shippingCost(method):
    if method == "Standard":
        return 5.0
    elif method == "Express":
        return 10.0
    else:
        messagebox.showerror("Error", "Invalid shipping method")
        return 0.0

# GUI Setup Functions
def productList():
    frame = tk.Frame(root)
    frame.pack(pady=10)
    tk.Label(frame, text="Available Products").pack()
    
    for category, products in PRODUCTS.items():
        cat_frame = tk.LabelFrame(frame, text=category)
        cat_frame.pack(pady=5)
        
        for product, price in products.items():
            product_frame = tk.Frame(cat_frame)
            product_frame.pack(anchor="w")
            tk.Label(product_frame, text=f"{product} - ₹{price}").pack(side="left")
            tk.Button(product_frame, text="Add to Cart", command=lambda c=category, p=product: addToCart_and_update(c, p)).pack(side="right")

def cartOverview():
    global cart_listbox
    cart_frame = tk.Frame(root)
    cart_frame.pack(pady=10)
    tk.Label(cart_frame, text="Shopping Cart").pack()
    cart_listbox = tk.Listbox(cart_frame, width=50)
    cart_listbox.pack()
    
    for text, cmd in [("Edit Quantity", editQuantity), ("Remove Item", removeItem), ("Checkout", checkout)]:
        tk.Button(cart_frame, text=text, command=cmd).pack(pady=2)

def totalSection():
    global total_label
    total_label = tk.Label(root, text="Total: ₹0.00")
    total_label.pack(pady=10)

# Cart Update Functions
def addToCart_and_update(category, product):
    addToCart(category, product)
    updateCart()

def updateCart():
    cart_listbox.delete(0, tk.END)
    total = calculateTotal()
    for product, quantity in cart.items():
        for category in PRODUCTS:
            if product in PRODUCTS[category]:
                price = PRODUCTS[category][product] * quantity
                cart_listbox.insert(tk.END, f"{product} - Quantity: {quantity} - Price: ₹{price:.2f}")
    total_label.config(text=f"Total: ₹{total:.2f}")

def editQuantity():
    product_name = selectedProduct()
    if not product_name: return
    new_quantity = simpledialog.askinteger("Edit Quantity", f"Enter new quantity for {product_name}:")
    if new_quantity and new_quantity > 0:
        cart[product_name] = new_quantity
        updateCart()
    else:
        messagebox.showinfo("Info", "Invalid quantity. Please enter a positive number.")

def removeItem():
    product_name = selectedProduct()
    if product_name:
        removeFromCart(product_name)
    updateCart()

def selectedProduct():
    selected = cart_listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "Select an item to edit.")
        return None
    return cart_listbox.get(selected[0]).split(" - ")[0]

# Checkout Functions
def checkout():
    checkout_window = tk.Toplevel(root)
    checkout_window.title("Checkout")
    tk.Label(checkout_window, text="Order Summary", font=("Arial", 12, "bold")).pack(pady=5)
    
    for product, quantity in cart.items():
        for category in PRODUCTS:
            if product in PRODUCTS[category]:
                price = PRODUCTS[category][product] * quantity
                tk.Label(checkout_window, text=f"{product} - Quantity: {quantity} - Price: ₹{price:.2f}").pack()

    subtotal = calculateTotal()
    global total_with_discount
    total_with_discount = subtotal
    total_label_checkout = tk.Label(checkout_window, text=f"Total: ₹{subtotal:.2f}")
    total_label_checkout.pack(pady=10)

    shippingPayment(checkout_window)
    tk.Button(checkout_window, text="Place Order", command=placeOrder).pack(pady=20)

def shippingPayment(checkout_window):
    global address_entry, shipping_method
    tk.Label(checkout_window, text="Shipping Address", font=("Times New Roman", 12, "bold")).pack(pady=10)
    tk.Label(checkout_window, text="Address:").pack()
    address_entry = tk.Entry(checkout_window, width=40)
    address_entry.pack()
    tk.Label(checkout_window, text="Shipping Method:").pack()
    shipping_method = tk.StringVar(value="Standard")
    for method, display_text in [("Standard", "Standard(+₹5.0)"), ("Express", "Express(+₹10.0)")]:
        tk.Radiobutton(checkout_window, text=display_text, variable=shipping_method, value=method).pack()

def placeOrder():
    if not cart:
        messagebox.showerror("Error", "Your cart is empty! Please add at least one product to the cart before placing an order.")
        return  # Exit if the cart is empty

    if not address_entry.get() or not total_with_discount:
        messagebox.showerror("Error", "Please enter a shipping address and ensure total is calculated.")
        return
    
    shipping_cost = shippingCost(shipping_method.get())
    if shipping_cost == 0.0:
        return  # Don't proceed if shipping method is invalid
    
    final_total = total_with_discount + shipping_cost
    saveOrderSummary(final_total)
    
    # Reset address and shipping method after placing the order
    address_entry.delete(0, tk.END)
    shipping_method.set("Standard")

    messagebox.showinfo("Order Confirmation", "Order placed successfully!")

# Main Application Function
def main():
    global root
    root = tk.Tk()
    root.title("Shopping Cart")

    methodOfPayment = simpledialog.askstring("Payment", "Do you want to use Cash on Delivery? (yes/no)").strip().lower()

    if methodOfPayment == "yes":
        productList()
        cartOverview()
        totalSection()
        root.mainloop()
    elif methodOfPayment == "no":
        messagebox.showinfo("Order Cancelled", "Order cannot be placed without cash on delivery.")
    else:
        messagebox.showerror("Invalid Input", "Invalid payment option. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
