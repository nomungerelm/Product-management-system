from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql

def connect_database():
    try:
            connection=pymysql.connect(host='localhost', user='root', password='bilig616')
            cursor=connection.cursor()
    except:
        messagebox.showerror('Error','Database connectivity issue try again')
        return None, None
    return cursor, connection

def create_database_table():
    cursor,connection=connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system ')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS driver_data(driverId INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), gender VARCHAR(50), contact VARCHAR(30), work_shift VARCHAR(50), salary VARCHAR(50) )')


def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_system')
    try:
        # Fetch data from the database
        cursor.execute('SELECT * FROM driver_data')
        driver_records = cursor.fetchall()

        # Clear the existing Treeview data
        driver_treeview.delete(*driver_treeview.get_children())

        # Insert new data into the Treeview
        for record in driver_records:
            driver_treeview.insert('', 'end', values=record)

        # Debugging: Print all rows in the Treeview
        print("Current data in Treeview:")
        for child in driver_treeview.get_children():
            print(driver_treeview.item(child, 'values'))

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


        
def select_data(event, driverId_entry, name_entry, email_entry, gender_combobox, contact_entry, work_shift_combobox, salary_entry):
    selected_row = driver_treeview.focus()
    row = driver_treeview.item(selected_row, 'values')
    
    if not row:
        print("No data found for the selected row.")
        return  # Exit the function if row is empty
    
    driverId_entry.delete(0, END)
    driverId_entry.insert(0, row[0])
    
    name_entry.delete(0, END)
    name_entry.insert(0, row[1])
    
    email_entry.delete(0, END)
    email_entry.insert(0, row[2])
    
    gender_combobox.set(row[3])
    
    contact_entry.delete(0, END)
    contact_entry.insert(0, row[4])
    
    work_shift_combobox.set(row[5])
    
    salary_entry.delete(0, END)
    salary_entry.insert(0, row[6])

    driver_treeview.selection_remove(driver_treeview.selection())
        
def update_driver(driverId, name, email, gender, contact, work_shift, salary):
    selected_row = driver_treeview.focus()
    if not selected_row:
        print("No row selected.")
        return
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
                return  # Exit if connection fails
        try:
            cursor.execute('use inventory_system')
            cursor.execute('SELECT * from driver_data WHERE driverId=%s', (driverId,))
            current_data=cursor.fetchone()
            current_data=current_data[1:]
            
            new_data=(name, email, gender, contact, work_shift, salary)
            
            if current_data==new_data:
                messagebox.showinfo('Information','No changes')
                return
        
            cursor.execute('UPDATE driver_data SET name=%s,email=%s, gender=%s, contact=%s, work_shift=%s, salary=%s WHERE driverId=%s', (name, email, gender, contact, work_shift, salary, driverId))
            connection.commit()
            messagebox.showinfo('Success', 'Data is updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        finally:
            # Ensure the database connection is closed
                cursor.close()
                connection.close()

#recieve call
def delete_driver(driverId_entry, driver_treeview):
    selected_row = driver_treeview.focus()
    if not selected_row:
        messagebox.showwarning('Warning', 'No row selected.')
        return
    
    # Get the Driver ID from the selected row
    driverId = driverId_entry.get()
    if not driverId:
        messagebox.showerror('Error', 'Driver ID is required.')
        return

    # Confirm deletion
    result = messagebox.askyesno('Confirm', 'Do you want to delete this record?')
    if not result:
        return
    
    # Database connection
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Database connection failed.')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM driver_data WHERE driverId = %s', (driverId,))
        connection.commit()

        # Refresh the Treeview data
        treeview_data()

        messagebox.showinfo('Success', 'Record has been deleted.')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to delete record: {e}')
    finally:
        cursor.close()
        connection.close()

def search_driver(search_option, value):
    if search_option=='Search By':
        messagebox.showerror('Error', 'No option is selected')
    elif value=='':
        messagebox.showerror('Error', 'Enter the value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return 
        try:
            cursor.execute('use inventory_system')
            cursor.execute(f'SELECT * FROM driver_data WHERE {search_option} LIKE %s', f'%{value}%')
            records=cursor.fetchall()
            driver_treeview.delete(*driver_treeview.get_children())
            for record in records:
                driver_treeview.insert('', END, value=record)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete record: {e}')
        finally:
            cursor.close()
            connection.close()

def add_driver(driverId, name, email, gender, contact, work_shift, salary):
    if (driverId == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or work_shift == 'Select Work Shift' or salary == ''):
        messagebox.showerror('Error', 'All fields are required')
        return  # Prevent further execution if there's an error
    else:
            # Connect to the database
            cursor, connection = connect_database()
            if not cursor or not connection:
                return  # Exit if connection fails
            cursor.execute('use inventory_system')
            try:
                cursor.execute('SELECT driverId from driver_data WHERE driverId=%s', (driverId, ))
                if cursor.fetchone():
                        messagebox.showerror('Error','Id already exists')
                        return
            # Insert data into the database
                cursor.execute('INSERT INTO driver_data VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (driverId, name, email, gender, contact, work_shift, salary))
                connection.commit()
                treeview_data()
            # Inform the user of successful insertion
                messagebox.showinfo('Success', 'Driver added successfully')
            except Exception as e:
                messagebox.showerror('Error', f'An error occurred: {str(e)}')
            finally:
            # Ensure the database connection is closed
                cursor.close()
                connection.close()

def clear_fields(driverId_entry, name_entry, email_entry, gender_combobox, contact_entry, work_shift_combobox, salary_entry, check):
        driverId_entry.delete(0,END)
        name_entry.delete(0,END)
        email_entry.delete(0,END)
        gender_combobox.delete(0,END)
        contact_entry.delete(0,END)
        work_shift_combobox.delete(0,END)
        salary_entry.delete(0,END)
        if check:
            driver_treeview.selection_remove(driver_treeview.selection())

def show_all(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')
    
#Functional
def driver_form(window):
    global back_image, driver_treeview
    driver_frame = Frame(window, width=1000, height=565 ,bg='white')
    driver_frame.place (x=260, y=80)
    heading_label = Label(driver_frame, text='Manage Drivers Information', font=( 'times new roman', 16),bg='ivory4', fg='white')
    heading_label.place(x=0, y=0, relwidth=1) 
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(driver_frame,image=back_image, bd=0,cursor='hand2',bg='white',command=lambda: driver_frame.place_forget())
    back_button.place(x=10,y=30)
    
    #combobox songolt hiideg
    top_frame=Frame(driver_frame, bg='white')
    top_frame.place(x=0, y=60, relwidth=1,height=235)

    search_frame=Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=('driverId', 'Name', 'Email'),font=('times new roman',12),state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=20) #2talaas 20 
    search_entry=Entry(search_frame,font=('times new roman',12),bg='lightyellow')
    search_entry.grid(row=0,column=1)
    search_button=Button(search_frame, text='SEARCH', font=('times new roman', 12),width=10,cursor='hand2', command=lambda :search_driver(search_combobox.get(), search_entry.get()) )
    search_button.grid(row=0, column=2, padx=20)

    show_button=Button(search_frame, text='SHOW', font=('times new roman', 12), width=10, cursor='hand2', command=lambda :show_all(search_entry, search_combobox))
    show_button.grid(row=0, column=3)
    
    #scrollbar before treeview
    horizontal_scrollbar=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scrollbar=Scrollbar(top_frame,orient=VERTICAL)
    
    driver_treeview=ttk.Treeview(top_frame, columns=('driverId', 'name', 'email','gender', 'contact','work_shift','salary'),show='headings',yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    vertical_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scrollbar.config(command=driver_treeview.xview)
    vertical_scrollbar.config(command=driver_treeview.yview)
    driver_treeview.pack(pady=(10,0))
    
    driver_treeview.heading('driverId', text='Driver Id')
    driver_treeview.heading('name', text='Name')
    driver_treeview.heading('email', text='Email')
    driver_treeview.heading('gender', text='Gender')
    driver_treeview.heading('contact', text='Contact')
    driver_treeview.heading('work_shift', text='Work Shift')
    driver_treeview.heading('salary', text='Salary')
    
    driver_treeview.column('driverId',width=60)
    driver_treeview.column('name',width=140)
    driver_treeview.column('email',width=180)
    driver_treeview.column('gender',width=80)
    driver_treeview.column('contact',width=100)
    driver_treeview.column('work_shift',width=100)
    driver_treeview.column('salary',width=140)
    
    treeview_data()
    
    detail_frame=Frame(driver_frame, bg='white')
    detail_frame.place(x=20,y=300)

    driverId_label=Label(detail_frame,text='Driver Id',font=('times new roman', 12),bg='white')
    driverId_label.grid(row=0, column=0, padx=20,pady=10)
    driverId_entry=Entry(detail_frame, font=('times new roman', 12),bg='lightyellow')
    driverId_entry.grid(row=0, column=1,padx=20, pady=10)

    name_label=Label(detail_frame,text='Name',font=('times new roman', 12),bg='white')
    name_label.grid(row=0, column=2, padx=20,pady=10)
    name_entry=Entry(detail_frame, font=('times new roman', 12),bg='lightyellow')
    name_entry.grid(row=0, column=3,padx=20, pady=10)


    email_label=Label(detail_frame,text='Email',font=('times new roman', 12),bg='white')
    email_label.grid(row=0, column=4, padx=20,pady=10)
    email_entry=Entry(detail_frame, font=('times new roman', 12),bg='lightyellow')
    email_entry.grid(row=0, column=5,padx=20, pady=10)

    gender_label=Label(detail_frame,text='Gender',font=('times new roman', 12),bg='white')
    gender_label.grid(row=1, column=0, padx=20,pady=10)
    gender_combobox=ttk.Combobox(detail_frame, values=('Male', 'Female'), font=('times new roman', 12),width=18, state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)


    contact_label=Label(detail_frame,text='Contact',font=('times new roman', 12),bg='white')
    contact_label.grid(row=1, column=2, padx=20,pady=10, sticky='w')
    contact_entry=Entry(detail_frame, font=('times new roman', 12),bg='lightyellow')
    contact_entry.grid(row=1, column=3,padx=20, pady=10)

    work_shift_label=Label(detail_frame,text='Work Shift',font=('times new roman', 12),bg='white')
    work_shift_label.grid(row=1, column=4, padx=20,pady=10, sticky='w')
    work_shift_combobox=ttk.Combobox(detail_frame, values=('Morning', 'Evening', 'Night'), font=('times new roman', 12),width=18, state='readonly')
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=1, column=5)

    salary_label=Label(detail_frame,text='Salary',font=('times new roman', 12),bg='white')
    salary_label.grid(row=2, column=0, padx=20,pady=10, sticky='w')
    salary_entry=Entry(detail_frame, font=('times new roman', 12),bg='lightyellow')
    salary_entry.grid(row=2, column=1,padx=20, pady=10)

    button_frame=Frame(driver_frame, bg='white')
    button_frame.place(x=200, y=530)
#button calling function
    add_button=Button(button_frame, text='Add', font=('times new roman', 12),width=10,cursor='hand2', command=lambda :add_driver(driverId_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), contact_entry.get(), work_shift_combobox.get(), salary_entry.get()) )
    add_button.grid(row=0, column=0, padx=20)
    
    update_button=Button(button_frame, text='Update', font=('times new roman', 12),width=10,cursor='hand2', command=lambda :update_driver(driverId_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), contact_entry.get(), work_shift_combobox.get(), salary_entry.get()) )
    update_button.grid(row=0, column=1, padx=20)

    delete_button=Button(button_frame, text='Delete', font=('times new roman', 12),width=10,cursor='hand2' ,command=lambda :delete_driver(driverId_entry, driver_treeview))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button=Button(button_frame, text='Clear', font=('times new roman', 12),width=10,cursor='hand2', command=lambda :clear_fields(driverId_entry, name_entry, email_entry, gender_combobox, contact_entry, work_shift_combobox, salary_entry, True)) 
    clear_button.grid(row=0, column=3, padx=20)
    
    driver_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, driverId_entry, name_entry, email_entry, gender_combobox, contact_entry, work_shift_combobox, salary_entry))

    create_database_table()
    return driver_frame