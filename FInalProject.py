from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pylab as plt
from PIL import Image, ImageTk

def show_add_win():
    main_win.withdraw()
    add_win.deiconify()

def close_add_win():
    add_win.withdraw()
    main_win.deiconify()

def show_view_win():
    main_win.withdraw()
    view_win.deiconify()
    vw_data.delete(1.0, END)
    
    con= None
    try:
        con=connect("Employee_data.db")
        cursor=con.cursor()
        sql="select * from employee"
        cursor.execute(sql)
        data=cursor.fetchall()
        info=""
        for d in data:
            info= info+ "empid: "+ str(d[0])+ " \n" + "name:"+ str(d[1]) + "\n" + "salary: "+ str(d[2]) + "\n"
        vw_data.insert(INSERT, info)

    except Exception as e:
        showerror("Issue", e)
    
    finally:
        if con is not None:
            con.close()
            print("connection is closed.")


def close_view_win():
    view_win.withdraw()
    main_win.deiconify()        

def show_update_win():
    main_win.withdraw()
    update_win.deiconify()


    empid = int(update_empid_entry.get())
    name = update_empname_entry.get()  
    salary = int(update_empsalary_entry.get())

    if not name or not salary:
        showerror("Error", "Name and salary fields are required")
        return

    con = None
    try:
        con = connect("Employee_data.db")
        cursor = con.cursor()
        sql = "update employee set name= ? , salary= ? where empid = ?"
        empid = update_empid_entry.get()
        if empid != "":
            name = update_empname_entry.get()  
            salary = int(update_empsalary_entry.get())
            cursor.execute(sql, (name, salary, empid))
            if cursor.rowcount == 1:
                con.commit()
                showinfo("Success", "Record updated")
            else:
                showwarning("Warning", "No record found with the given ID")
        
            update_empname_entry.delete(0, END)
            update_empid_entry.delete(0, END)
            update_empsalary_entry.delete(0, END)
            update_empid_entry.focus_set()
    except Exception as e:
            showerror("Incorrect", e)
    finally:
            if con is not None:
                con.close()
                print("connection is closed.")


def close_update_win():
    update_win.withdraw()
    main_win.deiconify()

def show_delete_win():
    main_win.withdraw()
    delete_win.deiconify()   

    con = None
    try:
        con = connect("Employee_data.db")
        cursor = con.cursor()
        empid = id_entry.get()
        if empid !="":
            cursor.execute("DELETE FROM employee WHERE empid = ?", (empid,))
            if cursor.rowcount == 0:
                showinfo("Error", "No record found with given ID")    
            else:
                showinfo("Success", "Record deleted")
                con.commit()
                id_entry.delete(0,END)
                
    except Exception as e:
        showerror("Error", str(e))
    finally:
        if con is not None:
            con.close() 
            print("connection is closed.")

def close_delete_win():
    delete_win.withdraw()
    main_win.deiconify()

def show_charts_win():
    main_win.withdraw()
    charts_win.deiconify()  
    
def plot_data():
    con= None
    try:
        con=connect("Employee_data.db")
        cursor=con.cursor()
        sql="select * from employee"
        cursor.execute(sql)
        data=cursor.fetchall()
        employees = []
        salaries = []
        for d in data:
            employees.append(d[1])
            salaries.append(d[2])

            
    
        # create a bar chart of the employee salaries
        plt.bar(employees, salaries)
        plt.title("Employee Salaries")
        plt.xlabel("Employee Name")
        plt.ylabel("Salary")
        
            # display the chart
        plt.show()
            
        
    except Error as e:
        print(e)
    finally:
        if con is not None:
            con.close()
    
    
def close_charts_win():
    charts_win.withdraw()
    main_win.deiconify()  


def save_data():
    con=None
    try:
        con=connect("Employee_data.db")
        cursor=con.cursor()
        sql="insert into employee values('%d', '%s', '%d')"
        empid=int(empid_entry.get())
        name=empname_entry.get()
        salary=int(empsalary_entry.get())
        cursor.execute(sql % (empid, name, salary))
        con.commit()
        showinfo("Success", "Record added")
        empname_entry.delete(0, END)
        empid_entry.delete(0, END)
        empsalary_entry.delete(0,END)
        empid_entry.focus()

    except Exception as e:    
        showerror("Incorrect", e)

    finally:
        if con is not None:
            con.close()    
            print("connection is closed.") 

        
main_win=Tk()
main_win.title("Employee Management System")
main_win.geometry("1500x700+0+0")

screen_width = main_win.winfo_screenwidth()
screen_height = main_win.winfo_screenheight()
#we create a transparent Frame widget called spacer_frame that has the same dimensions as the screen. 
# The bg parameter is set to an empty string to make it transparent.
# We position the spacer frame on top of the background label using the place() method, so that it covers the entire window.
#  Then we can add our content widgets on top of the spacer frame using pack() 
# or grid(), so that they are not blocked by the background label.


bg_image = Image.open("L24_Final/Bg_mainpage.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background label and position at the back of the widget stack
bg_label = Label(main_win, image=bg_photo, width=screen_width, height=screen_height)
bg_label.place(x=0, y=0)

# Add transparent spacer frame on top of the background label
spacer_frame = Frame(main_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="Employee Management System",
                font=("times new roman", 40, "bold",), bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)


f=("times new roman", 40, "bold")
y=30
x=25
mw_add=Button(main_win, text="Add Employee", font=f, width=15, command=show_add_win)
mw_view=Button(main_win, text="View Employee", font=f, width=15, command=show_view_win)
mw_update=Button(main_win, text="Update Employee", font=f, width=15, command=show_update_win)
mw_delete=Button(main_win,text="Delete Employee", font=f, width=15, command=show_delete_win)
mw_charts=Button(main_win, text="Charts", font=f, width=15, command=show_charts_win)


mw_add.pack(pady=y,padx=(600,0))
mw_view.pack(pady=y, padx=(600,0))
mw_update.pack(pady=y, padx=(600,0))
mw_delete.pack(pady=y, padx=(600,0))
mw_charts.pack(pady=y, padx=(600,0))

add_win=Toplevel(main_win)
add_win.title("Add Student")
add_win.geometry("1500x700+0+0")

screen_width = add_win.winfo_screenwidth()
screen_height = add_win.winfo_screenheight()

add_win_bg_image = Image.open("L24_Final/View_emp_bgimage.png")
add_win_bg_image = add_win_bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
add_win_bg_photo = ImageTk.PhotoImage(add_win_bg_image)

# Create background label and position at the back of the widget stack
add_win_bg_label = Label(add_win, image=add_win_bg_photo, width=screen_width, height=screen_height)
add_win_bg_label.place(x=0, y=0)
spacer_frame = Frame(add_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="Add Employeee Details",
                font=f, bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)


empid_label=Label(add_win,text="Enter Employee ID", font=f, bg="grey", fg="white", relief="solid", bd=5)
empid_entry=Entry(add_win,font=f,  bg="white", fg="Black", insertbackground="black")
empname_label=Label(add_win,text="Enter Employee name", font=f, bg="grey", fg="white", relief="solid", bd=5)
empname_entry=Entry(add_win,font=f, bg="white", fg="Black", insertborderwidth=6)
empsalary_label=Label(add_win,text="Enter Employee Salary", font=f, bg="grey", fg="white", relief="solid", bd=5)
empsalary_entry=Entry(add_win,font=f, bg="white", fg="Black", insertbackground="black")

addwin_save=Button(add_win,text="Save", font=f, width=15, command=save_data, bg="grey", fg="white", relief="solid", bd=5)
addwin_back=Button(add_win, text="Back", font=f, width=15, command=close_add_win, bg="grey", fg="white", relief="solid", bd=5)

empid_label.grid(row=0, column=0, pady=y, padx=(580,0))
empid_entry.grid(row=0, column=1, pady=y, padx=(5,0))
empname_label.grid(row=1, column=0, pady=y, padx=(580,0))
empname_entry.grid(row=1, column=1, pady=y, padx=(5,0))
empsalary_label.grid(row=2, column=0, pady=y, padx=(580,0)) 
empsalary_entry.grid(row=2, column=1, pady=y, padx=(5,0))
addwin_back.grid(row=3, column=0, pady=y, padx=(580,0)) 
addwin_save.grid(row=3, column=1, pady=y, padx=(5,0)) 
add_win.withdraw()

view_win=Toplevel(main_win)
view_win.title("View Employee")
view_win.geometry("1500x700+0+0")
screen_width = view_win.winfo_screenwidth()
screen_height = view_win.winfo_screenheight()

view_win_bg_image = Image.open("L24_Final/viewpage.png")
view_win_bg_image = view_win_bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
view_win_bg_photo = ImageTk.PhotoImage(view_win_bg_image)

# Create background label and position at the back of the widget stack
view_win_bg_label = Label(view_win, image=view_win_bg_photo, width=screen_width, height=screen_height)
view_win_bg_label.place(x=0, y=0)
spacer_frame = Frame(view_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="View Employeee Details",
                font=f, bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)

vw_data=ScrolledText(view_win, width=20, height=8, font=f, bg="grey", fg="black", relief="ridge", bd=8)
vw_back=Button(view_win, text="Back", font=f, command=close_view_win, bg="grey", fg="black")
vw_data.pack(pady=y, padx=(500,0))
vw_back.pack(pady=y, padx=(500,0))
view_win.withdraw()

update_win=Toplevel(main_win)
update_win.title("Update Employee")
update_win.geometry("1500x700+0+0")

screen_width = update_win.winfo_screenwidth()
screen_height = update_win.winfo_screenheight()

update_win_bg_image = Image.open("L24_Final/update.png")
update_win_bg_image = update_win_bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
update_win_bg_photo = ImageTk.PhotoImage(update_win_bg_image)

update_win_bg_label = Label(update_win, image=update_win_bg_photo, width=screen_width, height=screen_height)
update_win_bg_label.place(x=0, y=0)
spacer_frame = Frame(update_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="Update Employeee Details",
                font=f, bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)

update_empid_label=Label(update_win,text="Enter Employee ID", font=f, bg="grey", fg="white", relief="solid", bd=5)
update_empid_entry=Entry(update_win,font=f,  bg="white", fg="Black", insertbackground="black")
update_empname_label=Label(update_win,text="Enter Updated name", font=f, bg="grey", fg="white", relief="solid", bd=5)
update_empname_entry=Entry(update_win,font=f,  bg="white", fg="Black", insertbackground="black")
update_empsalary_label=Label(update_win,text="Enter Updated Salary", font=f, bg="grey", fg="white", relief="solid", bd=5)
update_empsalary_entry=Entry(update_win,font=f,  bg="white", fg="Black", insertbackground="black")

updatewin_save=Button(update_win,text="Save", font=f, width=15, command=show_update_win, relief="solid", bd=5)
updatewin_back=Button(update_win, text="Back", font=f, width=15, command=close_update_win, relief="solid", bd=5)
update_empid_label.grid(row=0, column=0, pady=35, padx=(620,0)) 
update_empid_entry.grid(row=0, column=1, pady=35, padx=(5,0)) 
update_empname_label.grid(row=1, column=0, pady=35, padx=(610,0)) 
update_empname_entry.grid(row=1, column=1, pady=35, padx=(5,0))
update_empsalary_label.grid(row=2, column=0, pady=35, padx=(580,0))
update_empsalary_entry.grid(row=2, column=1, pady=35, padx=(5,0)) 
updatewin_back.grid(row=3, column=0, pady=35, padx=(620,0)) 
updatewin_save.grid(row=3, column=1, pady=35, padx=(5,0))
update_win.withdraw()

delete_win=Toplevel(main_win)
delete_win.title("Delete Employee")
delete_win.geometry("1500x700+0+0")

screen_width = delete_win.winfo_screenwidth()
screen_height = delete_win.winfo_screenheight()

delete_win_bg_image = Image.open("L24_Final/delete.png")
delete_win_bg_image = delete_win_bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
delete_win_bg_photo = ImageTk.PhotoImage(delete_win_bg_image)

delete_win_bg_label = Label(delete_win, image=delete_win_bg_photo, width=screen_width, height=screen_height)
delete_win_bg_label.place(x=0, y=0)
spacer_frame = Frame(delete_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="Delete Employeee Details",
                font=f, bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)

id_Label=Label(delete_win,text="Enter Employee Id", font=f, bg="grey", fg="white", relief="solid", bd=5)
id_entry=Entry(delete_win, font=f,bg="white", fg="Black", insertbackground="black" )
delete_back=Button(delete_win,text="Back", width=15, font=f, command=close_delete_win)
delete_delbutton=Button(delete_win, text="Delete", width=15, font=f, command=show_delete_win)
id_Label.pack(pady=y, padx=(750,0))
id_entry.pack(pady=y, padx=(750,0))
delete_back.pack(pady=y, padx=(750,0))
delete_delbutton.pack(pady=y, padx=(750,0))
delete_win.withdraw()

charts_win=Toplevel(main_win)
charts_win.title("Plot Employee Data")
charts_win.geometry("1500x700+0+0")
screen_width = charts_win.winfo_screenwidth()
screen_height = charts_win.winfo_screenheight()

charts_win_bg_image = Image.open("L24_Final/graph.png")
charts_win_bg_image = charts_win_bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
charts_win_bg_photo = ImageTk.PhotoImage(charts_win_bg_image)

charts_win_bg_label = Label(charts_win, image=charts_win_bg_photo, width=screen_width, height=screen_height)
charts_win_bg_label.place(x=0, y=0)
spacer_frame = Frame(charts_win, width=screen_width, height=screen_height, bg="")
spacer_frame.place(x=0, y=0)

# Add content widgets on top of the spacer frame
labelTitle = Label(spacer_frame, text="Employee data chart",
                font=f, bg="grey", fg="white", bd=45, relief="ridge")
labelTitle.pack(side=TOP, fill=X, padx=20, pady=20)

plot_button =Button(charts_win, text="Plot Employee Data", font=f, command=plot_data)
plot_button.pack(padx=x, pady=y)

back_button = Button(charts_win, text="Back", font=f , command=close_charts_win)
back_button.pack(padx=x, pady=y)

charts_win.withdraw()

main_win.mainloop()
