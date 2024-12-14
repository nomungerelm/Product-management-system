from tkinter import *
from tkinter import ttk
from driver import connect_database
from tkinter import messagebox

def show_all(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)

def search_product(search_combobox, search_entry, treeview):
    if search_combobox.get()=='Search By':
        messagebox.showwarning('Warning', 'Select an option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning', 'Enter the value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 
        cursor.execute('use inventory_system')
        cursor.execute(f"SELECT * FROM product_data WHERE {search_combobox.get()} = %s", (search_entry.get(),))

        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror('Error', 'No records found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END, values=record)

def clear_fields(category_combobox, name_entry, price_entry, quantity_entry, status_combobox, treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select Status')

def delete_product(treeview, category_combobox, name_entry, price_entry, quantity_entry, status_combobox):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return

    dict = treeview.item(index)
    content = dict['values']

    ans = messagebox.askyesno('Confirm', 'Do you want to delete?')
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 
        try:
            cursor.execute('USE inventory_system')
            cursor.execute('DELETE FROM product_data WHERE category=%s AND name=%s', (content[0], content[1]))
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info', 'Record is deleted')
            clear_fields(category_combobox, name_entry, price_entry, quantity_entry, status_combobox, treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def update_product(category, name, price, quantity, status, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    
    dict = treeview.item(index)
    content = dict['values']
    
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT * FROM product_data WHERE category=%s AND name=%s', (category, name))
    current_data = cursor.fetchone()
    
    if current_data:
        current_data = list(current_data)  # Convert tuple to list
        current_data[2] = str(current_data[2])  # Ensure price is a string (if needed)
        current_data = tuple(current_data)

    # Convert price and quantity
    try:
        price = float(price)
        quantity = int(float(quantity))  # Ensure it's an integer
    except ValueError:
        messagebox.showerror('Error', 'Invalid price or quantity')
        return

    # New data to update
    new_data = (category, name, price, quantity, status)
    
    # Check if there are changes
    if current_data == new_data:
        messagebox.showinfo('Info', 'No changes detected')
        return
    
    cursor.execute(
        'UPDATE product_data SET category=%s, name=%s, price=%s, quantity=%s, status=%s WHERE category=%s AND name=%s',
        (category, name, price, quantity, status, category, name)
    )
    connection.commit()
    
    messagebox.showinfo('Info', 'Data is updated')
    treeview_data(treeview)  # Assuming this function refreshes the treeview


def select_data(event, treeview, category_combobox, name_entry, price_entry, quantity_entry, status_combobox):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    
    category_combobox.set(content[0])
    name_entry.insert(0, content[1])
    price_entry.insert(0, content[2])
    quantity_entry.insert(0, content[2])
    status_combobox.set(content[4])
    

def treeview_data(treeview):
    
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return

    try:
        # Switch to the correct database
        cursor.execute('USE inventory_system')

        # Fetch all records from the table
        cursor.execute('SELECT * FROM product_data')
        records = cursor.fetchall()

        # Clear the Treeview
        treeview.delete(*treeview.get_children())

        # Insert new data into the Treeview
        for record in records:
            treeview.insert('',END, values=record)

        # Debugging: Print all rows in the Treeview
    except Exception as e:
        messagebox.showerror('Error', f"Error retrieving data: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def fetch_category(category_combobox):
    # Connect to the database
    category_option=[]
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 
    # Use the appropriate database
    cursor.execute('USE inventory_system')

    # Fetch category names
    cursor.execute('SELECT name FROM category_data')
    names = [row[0] for row in cursor.fetchall()]
    if len(names)>0:
        category_combobox.set('Select')
    for name in names:
        category_option.append(name)
    category_combobox.config(values=category_option)


def add_product(category, name, price, quantity, status, treeview):
    # Validation for category
    if category == 'Empty':
        messagebox.showerror('Error', 'Please select a valid category')
        return
    elif category=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 
        # Use the appropriate database
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2), quantity INT, status VARCHAR(50))')
        cursor.execute('SELECT * from product_data WHERE category=%s AND name=%s', (category,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error', 'Product already exists')
            return
        
        cursor.execute('INSERT INTO product_data (category, name, price, quantity, status) VALUES (%s, %s, %s, %s, %s)', (category, name, price, quantity, status))
        connection.commit()
        messagebox.showinfo('Success', 'Data is added succesfully')
        treeview_data(treeview)




def product_form(window):
    global back_image
    # Frame for product form
    product_frame = Frame(window, width=1000, height=565, bg='white')
    product_frame.place(x=260, y=80)

    back_image = PhotoImage(file='back_button.png')
    # Back Button
    back_button = Button(product_frame, image=back_image, bd=0, cursor='hand2', bg='white', command=lambda:product_frame.place_forget())
    back_button.place(x=10, y=0)

    # Details Frame
    left_frame = Frame(product_frame, bg='white', bd=2, relief=RIDGE)
    left_frame.place(x=20, y=40)


    # Heading Label
    heading_label = Label(left_frame, text='Manage Product Details', font=('times new roman', 16), bg='ivory4', fg='white')
    heading_label.grid(row=0, columnspan=2, sticky='we')

    category_label = Label(left_frame, text='Category', font=('times new roman', 14), bg='white')
    category_label.grid(row=1, column=0, padx=20, sticky='w')
    category_combobox=ttk.Combobox(left_frame, font=('times new roman', 14), width=18, state='read')
    category_combobox.grid(row=1, column=1, pady=20)
    category_combobox.set('Empty')
    
    name_label = Label(left_frame, text='Product Name', font=('times new roman', 14), bg='white')
    name_label.grid(row=2, column=0, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    name_entry.grid(row=2, column=1, pady=20)
    
    price_label = Label(left_frame, text='Price', font=('times new roman', 14), bg='white')
    price_label.grid(row=3, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    price_entry.grid(row=3, column=1, pady=20)
    
    quantity_label = Label(left_frame, text='Quantity', font=('times new roman', 14), bg='white')
    quantity_label.grid(row=4, column=0, padx=20, sticky='w')
    quantity_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    quantity_entry.grid(row=4, column=1, pady=20)

    status_label = Label(left_frame, text='Status', font=('times new roman', 14), bg='white')
    status_label.grid(row=5, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('times new roman', 14), width=18, state='readonly')
    status_combobox.grid(row=5, column=1, pady=20)
    status_combobox.set('Select Status')

    button_frame=Frame(left_frame, bg='white')
    button_frame.grid(row=6, columnspan=2, pady=(30,10))
    
    add_button=Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :add_product(category_combobox.get(), name_entry.get(), price_entry.get(), quantity_entry.get(), status_combobox.get(), treeview))
    add_button.grid(row=0, column=0, padx=10)

    update_button=Button(button_frame, text='Update', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :update_product(category_combobox.get(), name_entry.get(), price_entry.get(), quantity_entry.get(), status_combobox.get(), treeview) )
    update_button.grid(row=0, column=1, padx=10)

    delete_button=Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :delete_product(treeview, category_combobox, name_entry, price_entry, quantity_entry, status_combobox))
    delete_button.grid(row=0, column=2, padx=10)

    clear_button=Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :clear_fields(category_combobox, name_entry, price_entry, quantity_entry, status_combobox, treeview))
    clear_button.grid(row=0, column=3, padx=10)

    search_frame=LabelFrame(product_frame, text='Search Products', font=('times new roman', 14))
    search_frame.place(x=480,y=30)
    search_combobox=ttk.Combobox(search_frame, values=('Category', 'Name', 'Status'), state='readonly', width=16, font=('times new roman', 14))
    search_combobox.grid(row=0, column=0, padx=10)
    search_combobox.set('Search By')

    search_entry = Entry(search_frame, font=('times new roman', 14), bg='lightyellow', width=16)
    search_entry.grid(row=0, column=1)

    search_button=Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :search_product(search_combobox,search_entry, treeview))
    search_button.grid(row=0, column=2, padx=(10,0),pady=10)
    show_button=Button(search_frame, text='Show all', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :show_all(treeview, search_combobox, search_entry))
    show_button.grid(row=0, column=3, padx=10)
    
    treeview_frame=Frame(product_frame)
    treeview_frame.place(x=480, y=125, width=570, height=430)
    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(
        treeview_frame,
        columns=('category', 'name', 'price', 'quantity','status'),
        show='headings',
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )

    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('category', text='Category')
    treeview.heading('name', text='Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    fetch_category(category_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>', lambda event:select_data(event, treeview, category_combobox, name_entry, price_entry, quantity_entry, status_combobox))

    return product_frame