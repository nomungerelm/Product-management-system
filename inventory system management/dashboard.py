from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

import pymysql

# Placeholder imports for forms
from driver import driver_form
from category import category_form
from product import product_form

current_frame = None

def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)

def create_card(parent, icon, x, y):
    frame = Frame(parent, bg='ivory4', bd=0, relief=SOLID, padx=10, pady=20)
    frame.place(x=x, y=y, width=200, height=200)

    # Icon in the card
    icon_label = Label(frame, image=icon, bg='ivory4')
    icon_label.pack(expand=True)

    

# GUI Setup
window = Tk()
window.title('Dashboard')
window.geometry('1270x668+0+0')
window.resizable(0, 0)
window.config(bg='ivory3')

# Header
bg_image = PhotoImage(file='inventory.png')
titleLabel = Label(window, image=bg_image, compound=LEFT, text='Product Management System',
                    font=('times new roman', 40), anchor='c', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)


# Left frame
leftFrame = Frame(window, bg='ivory3')
leftFrame.place(x=50, y=150, width=200, height=555)

logoImage = PhotoImage(file='logo.png')
imageLabel = Label(leftFrame, image=logoImage, bg='ivory3')
imageLabel.pack(pady=10)

menuLabel = Label(leftFrame, text='Selection', font=('times new roman', 20), bg='ivory4', fg='white')
menuLabel.pack(fill=X)

# Menu Buttons with rounded corners
def rounded_button(parent, image, text, command):
    button = Button(parent, image=image, compound=LEFT, text=text, font=('times new roman', 20), anchor='w',
                    command=command, relief=FLAT, bg='ivory3', padx=10, pady=10)
    button.pack(fill=X, pady=5)
    return button

driver_icon = PhotoImage(file='driver.png')
driver_button = rounded_button(leftFrame, driver_icon, '  Driver', lambda: show_form(driver_form))

categories_icon = PhotoImage(file='categories.png')
categories_button = rounded_button(leftFrame, categories_icon, '  Categories', lambda: show_form(category_form))

product_icon = PhotoImage(file='product.png')
product_button = rounded_button(leftFrame, product_icon, '  Product', lambda: show_form(product_form))


# Statistics Cards (Vertical Layout with Icons Only)
try:
    total_dri_icon = PhotoImage(file='total_dri.png')
    create_card(window, total_dri_icon, 420, 280)

    total_cat_icon = PhotoImage(file='total_cat.png')
    create_card(window, total_cat_icon, 630, 280)

    total_prod_icon = PhotoImage(file='total_prod.png')
    create_card(window, total_prod_icon, 840, 280)

except Exception as e:
    print("Error loading images:", e)

# Run the main loop
window.mainloop()
