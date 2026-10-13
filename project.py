from tkinter import *
from tkinter import messagebox
import pandas as pd
import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

mycode = mydb.cursor()

mycode.execute("CREATE DATABASE IF NOT EXISTS employees_db")

mycode.execute("USE employees_db")

mycode.execute("""
CREATE TABLE IF NOT EXISTS employees(Id INT PRIMARY KEY AUTO_INCREMENT,
Name VARCHAR(50),Age INT,Gender VARCHAR(30),City VARCHAR(30),
Department VARCHAR(30),Salary DECIMAL(10,2)
)""")

mydb.commit()

window = Tk()

window.title("User Data Collection")
window.geometry("550x600")

title = Label(window,text="User Data Collection Form")
title.pack(pady=20)

form_frame = Frame(window)
form_frame.pack(pady=10)


Label(form_frame,text="Name").grid(row=0, column=0, padx=10, pady=7)
name_entry = Entry(form_frame,width=30)
name_entry.grid(row=0,column=1,padx=10,pady=7)

Label(form_frame,text="Age").grid(row=1, column=0, padx=10, pady=7)
age_entry = Entry(form_frame,width=30)
age_entry.grid(row=1,column=1,padx=10,pady=7)

Label(form_frame,text="Gender").grid(row=2, column=0, padx=10, pady=7)
gender_entry = Entry(form_frame,width=30)
gender_entry.grid(row=2,column=1,padx=10,pady=7)

Label(form_frame,text="City").grid(row=3, column=0, padx=10, pady=7)
city_entry = Entry(form_frame,width=30)
city_entry.grid(row=3,column=1,padx=10,pady=7)

Label(form_frame,text="Department").grid(row=4, column=0, padx=10, pady=7)
department_entry = Entry(form_frame,width=30)
department_entry.grid(row=4,column=1,padx=10,pady=7)

Label(form_frame,text="Salary").grid(row=5, column=0, padx=10, pady=7)
salary_entry = Entry(form_frame,width=30)
salary_entry.grid(row=5,column=1,padx=10,pady=7)


def submit_data():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_entry.get().strip()
    city = city_entry.get().strip()
    department = department_entry.get().strip()
    salary = salary_entry.get().strip()

    if not name or not age or not gender or not city or not department or not salary:

        messagebox.showwarning(
            "Missing Information","Please fill in all fields"
        )
        return


    if not age.isdigit():
        messagebox.showerror(
            "Invalid Age","Age must be a number"
        )
        return

    age_val = int(age)

    if age_val <= 18:
        messagebox.showerror(
            "Invalid Age","Age must be greater than 18"
        )
        return

    try:
        salary_value = float(salary)

    except ValueError:

        messagebox.showerror(
            "Invalid Salary",
            "Salary must be a number."
        )
        return

    if salary_value <= 0:
        messagebox.showerror(
            "Invalid Salary",
            "Salary cannot be negative or zero ."
        )
        return

    
    data = {
            "Name": [name],
            "Age": [age],
            "Gender": [gender],
            "City": [city],
            "Department": [department],
            "Salary": [salary_value]
            }

    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    df["Age"] = df["Age"].astype("Int64")
    df["Salary"] = df["Salary"].astype(float)
    df["Name"] = df["Name"].str.title()
    df["Gender"] = df["Gender"].str.title()
    df["City"] = df["City"].str.title()
    df["Department"] = df["Department"].str.title()
    

    sql = """
    INSERT INTO employees
    (Name, Age, Gender, City, Department, Salary)
     VALUES (%s, %s, %s, %s, %s, %s)
    """

    for index,row in df.iterrows():

        values = (
            row["Name"],
            int(row["Age"]),
            row["Gender"],
            row["City"],
            row["Department"],
            float(row["Salary"])
        )

    mycode.execute(sql, values)

    mydb.commit()

    news = datetime.datetime.today()
    timestamp = news.strftime("%Y-%m-%d_%H-%M-%S")

    all_data = pd.read_sql("SELECT * FROM employees", mydb)

    file_name = "Employee_Report_" + timestamp + ".xlsx"

    all_data.to_excel(file_name,index=False,sheet_name="Cleaned Data1")
    messagebox.showinfo(
        "Success","Data cleaned and stored successfully!"
    )
    reset_data()

def reset_data():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)
    city_entry.delete(0, END)
    department_entry.delete(0, END)
    salary_entry.delete(0, END)


btn_frame = Frame(window)
btn_frame.pack(pady=25)

submit_btn = Button(btn_frame,text="Submit",command=submit_data,width=15,bg="light green")
submit_btn.grid(row=0,column=0,padx=5)

reset_btn = Button(btn_frame,text="Reset",command=reset_data,width=15,bg="cyan")
reset_btn.grid(row=0,column=1,padx=5)
window.mainloop()