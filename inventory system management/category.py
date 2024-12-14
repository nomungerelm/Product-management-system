from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from driver import connect_database

def delete_category(treeview):
    index = treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s', id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info', 'Record is deleted')
    except Exception as e:
        messagebox.showerror ('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def clear(id_entry, category_name_entry, description_text):
    id_entry.delete(0, END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)

def treeview_data(treeview):
    """
    Fetches data from the 'category_data' table in the database 
    and populates it into the given treeview widget.
    """
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return

    try:
        # Switch to the correct database
        cursor.execute('USE inventory_system')

        # Fetch all records from the table
        cursor.execute('SELECT * FROM category_data')
        category_records = cursor.fetchall()

        # Clear the Treeview
        treeview.delete(*treeview.get_children())

        # Insert new data into the Treeview
        for record in category_records:
            treeview.insert('', 'end', values=record)

        # Debugging: Print all rows in the Treeview
        print("Current data in Treeview:")
        for child in treeview.get_children():
            print(treeview.item(child, 'values'))

    except Exception as e:
        messagebox.showerror('Error', f"Error retrieving data: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def add_category(id, name, description, treeview):
    if id == '' or name == '' or description == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return  # Exit if connection fails

    try:   
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS category_data(id INT PRIMARY KEY, name VARCHAR(100), description TEXT)')

        # Corrected query for checking if ID already exists
        cursor.execute('SELECT * FROM category_data WHERE id=%s', (id,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Id already exists')
            return

        # Insert data into the table
        cursor.execute('INSERT INTO category_data VALUES(%s, %s, %s)', (id, name, description))
        connection.commit()
        messagebox.showinfo('Info', 'Data is inserted')

        # Refresh the Treeview
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

    
def category_form(window):
    global back_image
    category_frame = Frame(window, width=1000, height=565, bg='white')
    category_frame.place(x=260, y=80)

    heading_label = Label(category_frame, text='Manage Category Details', font=('times new roman', 16), bg='ivory4', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back_button.png')
    back_button = Button(category_frame, image=back_image, bd=0, cursor='hand2', bg='white', command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=30)

    details_frame = Frame(category_frame, bg='white')
    details_frame.place(x=250, y=60)

    id_label = Label(details_frame, text='Id', font=('times new roman', 14, 'normal'), bg='white')
    id_label.grid(row=0, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'normal'), bg='lightyellow')
    id_entry.grid(row=0, column=1)

    category_name_label = Label(details_frame, text='Category Name', font=('times new roman', 14, 'normal'), bg='white')
    category_name_label.grid(row=1, column=0, padx=20, sticky='w')
    category_name_entry = Entry(details_frame, font=('times new roman', 14, 'normal'), bg='lightyellow')
    category_name_entry.grid(row=1, column=1, pady=20)

    description_label = Label(details_frame, text='Description', font=('times new roman', 14, 'normal'), bg='white')
    description_label.grid(row=2, column=0, padx=20, sticky='nw')
    description_text = Text(details_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=2, column=1)


    button_frame = Frame(category_frame, bg='white')
    button_frame.place(x=280, y=280)

    style = ttk.Style()
    style.configure("TButton", foreground='white', background='#0F4D7D', font=('times new roman', 14))

    add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', 
                        command=lambda: add_category(id_entry.get(), category_name_entry.get(), description_text.get(1.0, END).strip(), treeview))
    add_button.grid(row=0, column=0, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :delete_category(treeview))
    delete_button.grid(row=0, column=1, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#0f4d7d', command=lambda :clear(id_entry, category_name_entry, description_text))
    clear_button.grid(row=0, column=2, padx=20)


    treeview_frame = Frame(category_frame, bg='yellow')
    treeview_frame.place(x=210, y=340, height=200, width=500)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(
        treeview_frame,
        columns=('id', 'name', 'description'),
        show='headings',
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )

    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text="ID")
    treeview.heading('name', text="Name")
    treeview.heading('description', text="Description")
    treeview.column('id', width=100)
    treeview.column('name', width=150)
    treeview.column('description', width=250)

    # Populate the Treeview initially
    treeview_data(treeview)
    return category_frame