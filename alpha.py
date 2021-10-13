from tkinter import * 
from tkinter import messagebox 
from ttkthemes import themed_tk as tk
from tkinter import ttk
import re, pymysql 
from datetime import datetime
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

df1=pd.read_excel('DATASET.xlsx',header=None).iloc[8:-1,:]
x=list(df1.iloc[0])
df1=df1.iloc[1:]
df1.to_excel('NEW_DATASET.xlsx',index=False,header=x)
df=pd.read_excel('NEW_DATASET.xlsx')

def adjustWindow(window): 
    w = 600  # width for the window size 
    h = 600  # height for the window size 
    ws = screen.winfo_screenwidth()  # width of the screen 
    hs = screen.winfo_screenheight()  # height of the screen 
    x = (ws/2) - (w/2)  # calculate x and y coordinates for the Tk window 
    y = (hs/2) - (h/2) 
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))  # set the dimensions of the screen and where it is placed 
    window.resizable(False, False)    # disabling the resize option for the window 

def register(): 
    global screen1, fullname, email, password, repassword, gender, tnc, company_id, company_name, company_city # making all entry field variable global 
    fullname, email, password, repassword, tnc, company_id, company_name, company_city = StringVar(),StringVar(),StringVar(),StringVar(),IntVar(),StringVar(),StringVar(),StringVar() 
    screen1 = Toplevel(screen)                
    screen1.title("Registeration") 
    adjustWindow(screen1) # configuring the window 
    image2,submit_button,proceed_button= PhotoImage(file="register_final_1.png"),PhotoImage(file="submit_button_3.png"),PhotoImage(file="proceed_to_login_3.png")
    label_for_image= Label(screen1, image=image2)
    label_for_image.pack()#lace(x=0, y=0, relwidth=1, relheight=1)
    label_text,labelx,labely = ["Full Name ","E-mail ID ","Password ","Re-Password ","Company Info : "],[.343,.342,.3428,.360,.3],[.305,.385,.465,.545,.645]
    for t,x,y in zip(label_text,labelx,labely):
        Label(screen1, text= t,font=("Roboto lt", 9, 'italic'), bg='black', fg='white').place(relx=x, rely=y, anchor="center")
    ttk.Entry(screen1, textvar=fullname , width='39').place(relx=.5, rely=.34, anchor="center")
    ttk.Entry(screen1, textvar=email , width='39').place(relx=.5, rely=.42, anchor="center")
    ttk.Entry(screen1, textvar=password, show="*" , width='39').place(relx=.5, rely=.50, anchor="center")
    ttk.Entry(screen1, textvar=repassword, show="*" , width='39').place(relx=.5, rely=.58, anchor="center")
    id_list,name_list,city_list = ['ID'], ['Name'],['City']
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor()   
    select_query = "SELECT * FROM company;"                                
    cursor.execute(select_query) # executing the queries 
    company_info = cursor.fetchall()
    for i in range(len(company_info)):
        id_list.append(company_info[i][0])
        name_list.append(company_info[i][1])
        city_list.append(company_info[i][2])
    connection.commit() # commiting the connection then closing it. 
    connection.close() 
    droplist = ttk.OptionMenu(screen1, company_id, *id_list) 
    droplist.config(width=2) 
    company_id.set('ID') 
    droplist.place(relx=.465, rely=.65, anchor="center")
    droplist = ttk.OptionMenu(screen1, company_name, *name_list) 
    droplist.config(width=6) 
    company_name.set('Name')
    droplist.place(relx=.6, rely=.65, anchor="center")
    droplist = ttk.OptionMenu(screen1, company_city, *city_list) 
    droplist.config(width=5) 
    company_city.set('City')
    droplist.place(relx=.75, rely=.65, anchor="center")
    ttk.Checkbutton(screen1, text="I accept all terms and conditions ", variable=tnc).place(relx=.5, rely=.735, anchor="center")
    Button(screen1, image = submit_button , border = 0,command=register_user).place(relx=.5, rely=.85, anchor="center")
    Button(screen1, image = proceed_button , border = 0, command=screen1.destroy).place(relx=.5, rely=.90, anchor="center")
    screen1.mainloop()

def register_user(): 
    
    if fullname.get() and email.get() and password.get() and repassword.get()  and company_id.get() and company_name.get() and company_city.get(): # checking for all empty values in entry field 
        if company_id.get() == "--ID--" or company_name.get() == "--Name--" or company_city.get() == "--City--":
            Label(screen1, text="⚠  Please Select Company ID / Name / City", fg="white", font=("Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
            return
        else: 
            if tnc.get(): # checking for acceptance of agreement 
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()): # validating the email 
                    if password.get() == repassword.get(): # checking both password match or not 
                        if all(x.isalpha() or x.isspace() for x in fullname.get()) and (len(fullname.get()) > 0):
                            
                            # if u enter in this block everything is fine just enter the values in database 
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                            cursor = connection.cursor() 
                            select_query =  "SELECT * FROM company where COMPANY_ID = '" + company_id.get() + "' AND COMPANY_NAME = '" + company_name.get() + "'  AND COMPANY_CITY = '" + company_city.get() + "';" # queries for retrieving values 
                            cursor.execute(select_query) # executing the queries 
                            company_info = cursor.fetchall() 
                            connection.commit() # commiting the connection then closing it. 
                            connection.close()
                            if company_info:
                                print(company_info)
                                connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                                cursor = connection.cursor() 
                                insert_query = "INSERT INTO company_users (fullname, email, password, company_id, company_name, company_city) VALUES('"+ fullname.get() + "', '"+ email.get() + "', '"+ password.get() + "', '"+ company_id.get() + "', '"+ company_name.get() + "', '"+ company_city.get() + "' );" # queries for inserting values 
                                cursor.execute(insert_query) # executing the queries 
                                connection.commit() # commiting the connection then closing it. 
                                connection.close() # closing the connection of the database 
                                Label(screen1, text="Registration Success ! You May Proceed To Login ", bg="white", font=("Roboto", 11), width='3000', anchor=W, fg='green').place(x=0, y=570) # printing successful registration message                
                            else:
                                Label(screen1, text="⚠  Please Select Valid Company ID / Name / City", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
                                return 
                        else:
                            Label(screen1, text="⚠  Name cannot contain Digits or Special Characters . Spaces are allowed." , fg="red", font=("Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                    else: 
                        Label(screen1, text="⚠  Password does not match", fg="red", font=( 
                            "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
                        return 
                else: 
                    Label(screen1, text="⚠  Please enter valid email id", fg="red", font=( 
                        "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
                    return 
            else: 
                Label(screen1, text="⚠  Please accept the agreement", fg="red", 
                      font=("Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
                return 
    else: 
        Label(screen1, text="⚠  Please fill all the details ", fg="red",font=("Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570) 
        return 

def login_verify(): 
    global userID 
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor() 
    select_query =  "SELECT * FROM company_users where email = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';" # queries for retrieving values 
    cursor.execute(select_query) # executing the queries 
    user_info = cursor.fetchall() 
    connection.commit() # commiting the connection then closing it. 
    connection.close() # closing the connection of the database                     
    if user_info: 
        messagebox.showinfo("Congratulation", "Login Succesfull") # displaying message for successful login 
        userID = user_info[0][0] 
        welcome_page(user_info) # opening welcome window 
    else: 
        messagebox.showerror("Error", "Invalid Username or Password")

def welcome_page(user_info): 
    global screen2 
    screen2 = Toplevel(screen) 
    screen2.title("Welcome") 
    adjustWindow(screen2) # configuring the window 
    image1, lookup,new_order,new_agent,new_customer,new_company,balance_button,cumulative_button,back,insights_button, = PhotoImage(file="bg_1.png"), PhotoImage(file="lookup.png"), PhotoImage(file="new_order.png"),PhotoImage(file="new_agent.png"),PhotoImage(file="new_customer.png"),PhotoImage(file="new_company.png"),PhotoImage(file="balance.png"),PhotoImage(file="cumulative_report.png"),PhotoImage(file="back.png"),PhotoImage(file="insights.png") 
    label_for_image= Label(screen2, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)      
    Label(screen2, text="Welcome " + user_info[0][1], width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen2, text="Search ",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.085)
    Button(screen2, image = lookup , border = 0, command = search_order).place(relx=.5, rely=.16, anchor="center") 
    Label(screen2, text="Add New Data To Database ",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.2)
    Button(screen2, image = new_order , border = 0, command= update_order).place(relx=.5, rely=.275, anchor="center") 
    Button(screen2, image = new_agent , border = 0, command= update_agent).place(relx=.5, rely=.320, anchor="center") 
    Button(screen2, image = new_customer , border = 0, command= update_customer).place(relx=.5, rely=.365, anchor="center")
    Button(screen2, image = new_company , border = 0, command= update_company).place(relx=.5, rely=.410, anchor="center")
    Label(screen2, text="Report ",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.455)
    Button(screen2, image = balance_button , border = 0, command = balance_report).place(relx=.5, rely=.530, anchor="center")
    Button(screen2, image = cumulative_button , border = 0,command = cumulative_data).place(relx=.5, rely=.575, anchor="center") 
    Label(screen2, text="Insights ",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.615)
    Button(screen2, image = insights_button , border = 0,command=insight_options).place(relx=.5, rely=.685, anchor="center")
    Button(screen2, image = back, border = 0, command=screen2.destroy).place(relx=.5, rely=.95, anchor="center") 
    screen2.mainloop()

def search_order():
    global screen3 ,order_year,order_month,order_day,order_code,customer_code 
    order_code = StringVar()
    customer_code = StringVar()
    screen3 = Toplevel(screen) 
    screen3.title("Search Order") 
    adjustWindow(screen3) # configuring the window 
    back,search_button,image1 = PhotoImage(file="back.png"),PhotoImage(file="search.png"),PhotoImage(file="bg_1.png")
    label_for_image= Label(screen3, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen3, text="Search Order ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    order_year,order_month,order_day = StringVar(),StringVar(),StringVar() 
    rx,ry,t,v = [1950,1,1],[2021,13,32],[.4,.5,.6],[order_year,order_month,order_day]
    for (i,j,k,l) in zip(rx,ry,t,v):
        choices = list(range(i,j)) 
        ttk.Combobox(screen3 , width=5, values = choices ,textvariable = l  ).place(relx=k, rely=.135, anchor="center") 
    order_year.set("2000") 
    order_month.set("01") 
    order_day.set("01") 
    label_text,rx1,ry1=[],[],[]
    Label(screen3, text="Order Number ", font=("Roboto lt", 10 , 'italic'), bg='black', fg='white').place(relx=.1, rely=.09, anchor="center")
    ttk.Entry(screen3, textvar=order_code , width='15').place(relx=.115, rely=.130, anchor="center")
    Label(screen3, text="Order Date ", font=("Roboto lt", 10 , 'italic'), bg='black', fg='white').place(relx=.51, rely=.09, anchor="center")
    Label(screen3, text="Customer Code ", font=("Roboto lt", 10 , 'italic'), bg='black', fg='white').place(relx=.895, rely=.09, anchor="center")
    ttk.Entry(screen3, textvar=customer_code , width='15').place(relx=.89, rely=.130, anchor="center")
    Button(screen3, image = search_button, border = 0, command = fetch_order).place(relx=.5, rely=.2, anchor="center")
    Label(screen3, text="Search Result",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.275,anchor='w')
    Label(screen3, text="Order Number : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.35,anchor='center')
    Label(screen3, text="Advance Amount : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.42,anchor='center')
    Label(screen3, text="Order ID : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.49,anchor='center')
    Label(screen3, text="Order Date : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.56,anchor='center')
    Label(screen3, text="Customer Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.63,anchor='center')
    Label(screen3, text="Agent Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.70,anchor='center')
    Label(screen3, text="Order Description : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.77,anchor='center')
    Button(screen3, image = back, border = 0, command=screen3.destroy).place(relx=.5, rely=.95, anchor="center")
    screen3.mainloop()  

def fetch_order():
    global screen3 ,order_year,order_month,order_day,order_code,customer_code 
    orderDateObj = datetime.strptime(order_year.get() + "-" + order_month.get() + "-" + order_day.get(), '%Y-%m-%d')
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor() 
    select_query =  "SELECT * FROM orders where ORD_NUM = '" + order_code.get() + "' OR ORD_DATE = '" + orderDateObj.strftime("%Y-%m-%d") + "' OR CUST_CODE = '" + customer_code.get() + "';" # queries for retrieving values 
    cursor.execute(select_query) # executing the queries 
    order_info = cursor.fetchall() 
    connection.commit() # commiting the connection then closing it. 
    connection.close() # closing the connection of the database                     
    if order_info:
        Label(screen3, text=order_info[0][0],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.35,anchor='e')
        Label(screen3, text=order_info[0][1],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.42,anchor='e')
        Label(screen3, text=order_info[0][2],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.49,anchor='e')
        Label(screen3, text=order_info[0][3],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.56,anchor='e')
        Label(screen3, text=order_info[0][4],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.63,anchor='e')
        Label(screen3, text=order_info[0][5],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.70,anchor='e')
        Label(screen3, text=order_info[0][6],width='10', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=E).place(relx=.8, rely=.77,anchor='e')
        Label(screen3, text=" Record Found ", width='100', height="1", font=("Ariel", 20,), fg='green', bg='white').place(relx=.5, rely=.85,anchor='center')
        
    else: 
        Label(screen3, text="Order Number : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.35,anchor='center')
        Label(screen3, text="Advance Amount : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.42,anchor='center')
        Label(screen3, text="Order ID : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.49,anchor='center')
        Label(screen3, text="Order Date : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.56,anchor='center')
        Label(screen3, text="Customer Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.63,anchor='center')
        Label(screen3, text="Agent Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.70,anchor='center')
        Label(screen3, text="Order Description : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.77,anchor='center')
        Label(screen3, text=" Record Not Found ", width='100', height="1", font=("Ariel", 20,), fg='red', bg='black').place(relx=.5, rely=.85,anchor='center')
    
def update_order():
    global screen4_1, ord_no , adv_amt , ord_amt , cust_code , agt_code , ord_des , order_year_1 ,order_month_1 , order_day_1
    ord_no , adv_amt , ord_amt , order_year_1 , order_month_1 , order_day_1 , cust_code , agt_code , ord_des = StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    screen4_1 = Toplevel(screen) 
    screen4_1.title("Update Order") 
    adjustWindow(screen4_1) # configuring the window 
    back = PhotoImage(file="back.png")
    add_button = PhotoImage(file="add.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen4_1, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen4_1, text="Add New Order ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen4_1, text="Order Number : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.25,anchor='center')
    ttk.Entry(screen4_1, textvar= ord_no , width='40').place(relx=.66, rely=.25, anchor="center")
    Label(screen4_1, text="Order Amount : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.32,anchor='center')
    ttk.Entry(screen4_1, textvar= ord_amt , width='40').place(relx=.66, rely=.32, anchor="center")
    Label(screen4_1, text="Advanced Amount : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.39,anchor='center')
    ttk.Entry(screen4_1, textvar= adv_amt , width='40').place(relx=.66, rely=.39, anchor="center")
    Label(screen4_1, text="Order Date : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.46,anchor='center')
    choices = list(range(1950,2051)) 
    ttk.Combobox(screen4_1 , width=5, values = choices ,textvariable = order_year_1  ).place(relx=.55, rely=.46, anchor="center") 
    choices = list(range(1,13)) 
    ttk.Combobox(screen4_1 , width=5, values = choices ,textvariable = order_month_1  ).place(relx=.65, rely=.46, anchor="center") 
    choices = list(range(1,32)) 
    ttk.Combobox(screen4_1 , width=5, values = choices ,textvariable = order_day_1  ).place(relx=.75, rely=.46, anchor="center") 
    order_year_1.set("2020") 
    order_month_1.set("1") 
    order_day_1.set("1")
    Label(screen4_1, text="Customer Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.53,anchor='center')
    ttk.Entry(screen4_1, textvar= cust_code , width='40').place(relx=.66, rely=.53, anchor="center")
    Label(screen4_1, text="Agent Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.60,anchor='center')
    ttk.Entry(screen4_1, textvar= agt_code , width='40').place(relx=.66, rely=.60, anchor="center")
    Label(screen4_1, text="Order Description : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.67,anchor='center')
    ttk.Entry(screen4_1, textvar= ord_des , width='40').place(relx=.66, rely=.67, anchor="center")
    Button(screen4_1, image = add_button, border = 0, command = update_order_db).place(relx=.5, rely=.8, anchor="center")
    Button(screen4_1, image = back, border = 0, command=screen4_1.destroy).place(relx=.5, rely=.9, anchor="center")
    Label(screen4_1, text=" Status", fg="white", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
    screen4_1.mainloop()   

def update_order_db():
    if ord_no.get() and adv_amt.get() and ord_amt.get() and cust_code.get() and agt_code.get() and ord_des.get() and order_year_1.get() and order_month_1.get() and order_day_1.get():
        orderDateObj_1 = datetime.strptime(order_year_1.get() + "-" + order_month_1.get() + "-" + order_day_1.get(), '%Y-%m-%d') 
        if len(ord_no.get()) == 6 and ord_no.get().isdigit(): 
            pass
        else:
            Label(screen4_1, text="⚠  Order number should have 6 digits ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
            return
        if ord_amt.get() and ord_amt.get().isdigit():
            if adv_amt.get() and adv_amt.get().isdigit():
                if order_year_1.get() and order_month_1.get() and order_day_1.get():
                    if len(cust_code.get()) == 6 and cust_code.get().isalnum():
                        connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                        cursor = connection.cursor() 
                        select_query =  "SELECT * FROM customer where CUST_CODE = '" + cust_code.get() + "';" # queries for retrieving values 
                        cursor.execute(select_query) # executing the queries 
                        cust_code_info = cursor.fetchall() 
                        connection.commit() # commiting the connection then closing it. 
                        connection.close()
                        if cust_code_info:
                            pass
                        else:
                            Label(screen4_1, text="⚠  Customer Code not found in the Database, Enter Valid Customer Code", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                        if len(agt_code.get()) == 4 and agt_code.get().isalnum():
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                            cursor = connection.cursor() 
                            select_query =  "SELECT * FROM agents where AGENT_CODE = '" + agt_code.get() + "';" # queries for retrieving values 
                            cursor.execute(select_query) # executing the queries 
                            agent_code_info = cursor.fetchall() 
                            connection.commit() # commiting the connection then closing it. 
                            connection.close()
                            if agent_code_info:
                                pass
                            else:
                                Label(screen4_1, text="⚠  Agent Code not found in the Database, Enter Valid Agent Code", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                return
                            if all(x.isalpha() or x.isspace() for x in ord_des.get()) and (len(ord_des.get()) > 0):
                                connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                                cursor = connection.cursor() 
                                insert_query = "INSERT INTO orders (ORD_NUM, ORD_AMOUNT, ADVANCE_AMOUNT, ORD_DATE, CUST_CODE, AGENT_CODE, ORD_DESCRIPTION) VALUES('"+ ord_no.get() + "', '"+ ord_amt.get() + "', '"+ adv_amt.get() + "', '" + orderDateObj_1.strftime("%Y-%m-%d") + "', '"+ cust_code.get() +  "', '" + agt_code.get() + "', '"+ ord_des.get() +"' );" 
                                cursor.execute(insert_query)
                                connection.commit() # commiting the connection then closing it. 
                                connection.close() # closing the connection of the database 
                                Label(screen4_1, text="New Order Added Successfully ", bg="white", font=("Roboto", 11), width='3000', anchor=W, fg='green').place(x=0, y=570) # printing successful registration message                 
                            else:
                                Label(screen4_1, text="⚠  Order Description should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                return
                        else:
                            Label(screen4_1, text="⚠  Agent Code should have 4 alphanumeric characters ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                    else:
                        Label(screen4_1, text="⚠  Custumer Code should have 6 alphanumeric characters ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                        return
                else:
                    Label(screen4_1, text="⚠  Please Enter Order Date ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                    return
            else:
                Label(screen4_1, text="⚠  Advanced Amount should have numbers only ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                return
        else:
            Label(screen4_1, text="⚠  Order Amount should have numbers only", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
            return
    else:
        Label(screen4_1, text="⚠  Please Fill All The Details ", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
        return

def update_agent():
    global screen4_2 , agt_code_1 , agt_name , work_area , commission , agt_phone
    agt_code_1 , agt_name , work_area , commission , agt_phone = StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    screen4_2 = Toplevel(screen) 
    screen4_2.title("Update Agent") 
    adjustWindow(screen4_2) # configuring the window 
    back = PhotoImage(file="back.png")
    add_button = PhotoImage(file="add.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen4_2, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen4_2, text="Add New Agent ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen4_2, text="Agent Code : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.35,anchor='center')
    ttk.Entry(screen4_2, textvar= agt_code_1 , width='40').place(relx=.66, rely=.35, anchor="center")
    Label(screen4_2, text="Agent Name : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.42,anchor='center')
    ttk.Entry(screen4_2, textvar= agt_name , width='40').place(relx=.66, rely=.42, anchor="center")
    Label(screen4_2, text="Working Area : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.49,anchor='center')
    ttk.Entry(screen4_2, textvar= work_area , width='40').place(relx=.66, rely=.49, anchor="center")
    Label(screen4_2, text="Commission : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.56,anchor='center')
    ttk.Entry(screen4_2, textvar= commission , width='40').place(relx=.66, rely=.56, anchor="center")
    Label(screen4_2, text="Phone number : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.63,anchor='center')
    ttk.Entry(screen4_2, textvar= agt_phone , width='40').place(relx=.66, rely=.63, anchor="center")
    Button(screen4_2, image = add_button, border = 0, command = update_agent_db).place(relx=.5, rely=.8, anchor="center")
    Button(screen4_2, image = back, border = 0, command=screen4_2.destroy).place(relx=.5, rely=.9, anchor="center")
    Label(screen4_2, text=" Status", fg="white", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
    screen4_2.mainloop()

def update_agent_db():
    if agt_code_1.get() and agt_name.get() and work_area.get() and commission.get() and agt_phone.get():
        if len(agt_code_1.get()) == 4 and agt_code_1.get().isalnum():
            if all(x.isalpha() or x.isspace() for x in agt_name.get()) and (len(agt_name.get()) > 0):
                if all(x.isalpha() or x.isspace() for x in work_area.get()) and (len(work_area.get()) > 0):
                    if commission.get().isdigit():
                        if int(commission.get()) > 0 and int(commission.get()) < 99:
                            comm = '0.'+ commission.get()
                            pass
                        else:
                            Label(screen4_2, text="⚠ Commission Percentage should be in the range of 0 - 99", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                        if len(agt_phone.get()) == 10 and agt_phone.get().isdigit():
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                            cursor = connection.cursor() 
                            insert_query = "INSERT INTO agents (AGENT_CODE, AGENT_NAME, WORKING_AREA, COMMISSION, PHONE_NO) VALUES('"+ agt_code_1.get() + "', '"+ agt_name.get() + "', '"+ work_area.get() + "', '" + comm +  "', '" + agt_phone.get() + "' );" # fullname.get() + "', '"+ email.get() + "', '"+ password.get() + "', '"+ company_id.get() + "', '"+ company_name.get() + "', '"+ company_city.get() + "' );" # queries for inserting values 
                            cursor.execute(insert_query) # executing the queries 
                            connection.commit() # commiting the connection then closing it. 
                            connection.close() # closing the connection of the database 
                            Label(screen4_2, text="New Agent Added Successfully ", bg="white", font=("Roboto", 11), width='3000', anchor=W, fg='green').place(x=0, y=570) # printing successful registration message                 
                            
                            pass
                        else:
                            Label(screen4_2, text="⚠ Agent Phone Number should have 10 Numbers", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                    else:
                        Label(screen4_2, text="⚠ Commission should have numbers only", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                        return
                else:
                    Label(screen4_2, text="⚠ Name of the area cannot have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                    return
            else:
                Label(screen4_2, text="⚠ Name of the agent cannot have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                return
        else:
            Label(screen4_2, text="⚠  Agent Code should have 4 alphanumeric characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
            return
    else:
        Label(screen4_2, text="⚠ Please Fill All The Details", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
        return
                
def update_customer():
    global screen4_3 , cust_code_2, cust_name, cust_city, cust_work_area, cust_country, grade, opn_amt, rec_amt, pay_amt, out_amt, cust_phone , agt_code_2
    cust_code_2, cust_name, cust_city, cust_work_area, cust_country, grade, opn_amt, rec_amt, pay_amt, out_amt, cust_phone , agt_code_2 = StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    screen4_3 = Toplevel(screen) 
    screen4_3.title("Update Customer") 
    adjustWindow(screen4_3) # configuring the window 
    back = PhotoImage(file="back.png")
    add_button = PhotoImage(file="add.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen4_3, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen4_3, text="Add New Customer ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen4_3, text="Customer Code : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.15,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_code_2 , width='40').place(relx=.7, rely=.15, anchor="center")
    Label(screen4_3, text="Customer Name : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.20,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_name , width='40').place(relx=.7, rely=.20, anchor="center")
    Label(screen4_3, text="Customer City : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.25,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_city , width='40').place(relx=.7, rely=.25, anchor="center")
    Label(screen4_3, text="Working Area : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.30,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_work_area , width='40').place(relx=.7, rely=.30, anchor="center")
    Label(screen4_3, text="Customer Country : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.35,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_country , width='40').place(relx=.7, rely=.35, anchor="center")
    Label(screen4_3, text="Grade : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.40,anchor='center')
    ttk.Entry(screen4_3, textvar= grade , width='40').place(relx=.7, rely=.40, anchor="center")
    Label(screen4_3, text="Opening Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.45,anchor='center')
    ttk.Entry(screen4_3, textvar= opn_amt , width='40').place(relx=.7, rely=.45, anchor="center")
    Label(screen4_3, text="Recieved Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.50,anchor='center')
    ttk.Entry(screen4_3, textvar= rec_amt , width='40').place(relx=.7, rely=.50, anchor="center")
    Label(screen4_3, text="Payment Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.55,anchor='center')
    ttk.Entry(screen4_3, textvar= pay_amt , width='40').place(relx=.7, rely=.55, anchor="center")
    Label(screen4_3, text="Outstanding Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.60,anchor='center')
    ttk.Entry(screen4_3, textvar= out_amt , width='40').place(relx=.7, rely=.60, anchor="center")
    Label(screen4_3, text="Phone Number : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.65,anchor='center')
    ttk.Entry(screen4_3, textvar= cust_phone , width='40').place(relx=.7, rely=.65, anchor="center")
    Label(screen4_3, text="Agent Code : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.70,anchor='center')
    ttk.Entry(screen4_3, textvar= agt_code_2 , width='40').place(relx=.7, rely=.70, anchor="center")
    Button(screen4_3, image = add_button, border = 0, command = update_customer_db).place(relx=.5, rely=.8, anchor="center")
    Button(screen4_3, image = back, border = 0, command=screen4_3.destroy).place(relx=.5, rely=.9, anchor="center")
    Label(screen4_3, text=" Status ", fg="white", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
    screen4_3.mainloop()

def update_customer_db():
    if cust_code_2 and cust_name and cust_city and cust_work_area and cust_country and grade and opn_amt and rec_amt and pay_amt and out_amt and cust_phone and agt_code_2:
        if len(cust_code_2.get()) == 6 and cust_code_2.get().isalnum():
            if all(x.isalpha() or x.isspace() for x in cust_name.get()) and (len(cust_name.get()) > 0):
                if all(x.isalpha() or x.isspace() for x in cust_city.get()) and (len(cust_city.get()) > 0):
                    if all(x.isalpha() or x.isspace() for x in cust_work_area.get()) and (len(cust_work_area.get()) > 0):
                        if all(x.isalpha() or x.isspace() for x in cust_country.get()) and (len(cust_country.get()) > 0):
                            if grade.get().isdigit():
                                if int(grade.get()) > 0 and int(grade.get()) < 4:
                                    pass
                                else:
                                    Label(screen4_3, text="⚠ Commission should be in the range of 1 - 3", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                    return
                                if opn_amt.get().isdigit():
                                    if rec_amt.get().isdigit():
                                        if pay_amt.get().isdigit():
                                            if out_amt.get().isdigit():
                                                if len(cust_phone.get()) == 10 and cust_phone.get().isdigit():
                                                    if len(agt_code_2.get()) == 4 and agt_code_2.get().isalnum():
                                                        connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                                                        cursor = connection.cursor() 
                                                        select_query =  "SELECT * FROM agents where AGENT_CODE = '" + agt_code_2.get() + "';" # queries for retrieving values 
                                                        cursor.execute(select_query) # executing the queries 
                                                        agent_code_info = cursor.fetchall() 
                                                        connection.commit() # commiting the connection then closing it. 
                                                        connection.close()
                                                        if agent_code_info:
                                                            pass
                                                        else:
                                                            Label(screen4_3, text="⚠  Agent Code not found in the Database, Enter Valid Agent Code", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                                            return
                                                        connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                                                        cursor = connection.cursor()
                                                        insert_query = "INSERT INTO customer (CUST_CODE, CUST_NAME, CUST_CITY, WORKING_AREA, CUST_COUNTRY, GRADE, OPENING_AMT, RECEIVE_AMT, PAYMENT_AMT, OUTSTANDING_AMT, PHONE_NO, AGENT_CODE) VALUES('" + cust_code_2.get() + "', '"+  cust_name.get() + "', '"+  cust_city.get() + "', '"+  cust_work_area.get() + "', '"+  cust_country.get() + "', '"+  grade.get() + "', '"+  opn_amt.get() + "', '"+  rec_amt.get() + "', '"+  pay_amt.get() + "', '"+  out_amt.get() + "', '"+  cust_phone.get() + "', '"+  agt_code_2.get()+ "' );"                                
                                                        cursor.execute(insert_query) # executing the queries 
                                                        connection.commit() # commiting the connection then closing it. 
                                                        connection.close() # closing the connection of the database 
                                                        Label(screen4_3, text="New Customer Added Successfully ", bg="white", font=("Roboto", 11), width='3000', anchor=W, fg='green').place(x=0, y=570) # printing successful registration message                 
                                                    else:
                                                        Label(screen4_3, text="⚠ Agent Code should have 4 alphanumeric characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                                        return
                                                else:
                                                    Label(screen4_3, text="⚠ Customer Phone Number should have 10 numbers", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                                    return
                                            else:
                                                Label(screen4_3, text="⚠ Outstanding Amount should not have alphabets or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                                return
                                        else:
                                            Label(screen4_3, text="⚠ Payment Amount should not have alphabets or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                            return
                                    else:
                                        Label(screen4_3, text="⚠ Recieved Amount should not have alphabets or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                        return
                                else:
                                    Label(screen4_3, text="⚠ Opening Amount should not have alphabets or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                    return
                            else:
                                Label(screen4_3, text="⚠ Grade should not have alphabets or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                                return
                        else:
                            Label(screen4_3, text="⚠ Country Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                            return
                    else:
                        Label(screen4_3, text="⚠ Work Area Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                        return
                else:
                    Label(screen4_3, text="⚠ City Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                    return
            else:
                Label(screen4_3, text="⚠ Customer Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                return
        else:
            Label(screen4_3, text="⚠ Customer Code should have 6 alphanumeric characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
            return
    else:
        Label(screen4_3, text="⚠ Please fill all the details", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
        return

def update_company():
    global screen4_4 , company_id_1 , company_name_1 , company_city_1
    company_id_1 , company_name_1 , company_city_1 = StringVar(),StringVar(),StringVar()
    screen4_4 = Toplevel(screen) 
    screen4_4.title("Update Company") 
    adjustWindow(screen4_4) # configuring the window 
    back = PhotoImage(file="back.png")
    add_button = PhotoImage(file="add.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen4_4, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen4_4, text="Add New Company ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen4_4, text="Company ID : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.35,anchor='center')
    ttk.Entry(screen4_4, textvar= company_id_1 , width='40').place(relx=.66, rely=.35, anchor="center")
    Label(screen4_4, text="Company Name : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.42,anchor='center')
    ttk.Entry(screen4_4, textvar= company_name_1 , width='40').place(relx=.66, rely=.42, anchor="center")
    Label(screen4_4, text="City : ",width='50', font=("Roboto lt", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.49,anchor='center')
    ttk.Entry(screen4_4, textvar= company_city_1 , width='40').place(relx=.66, rely=.49, anchor="center")
    Button(screen4_4, image = add_button, border = 0, command = update_company_db).place(relx=.5, rely=.8, anchor="center")
    Button(screen4_4, image = back, border = 0, command=screen4_4.destroy).place(relx=.5, rely=.9, anchor="center")
    Label(screen4_4, text=" Status", fg="white", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
    screen4_4.mainloop()

def update_company_db():
    if company_id_1.get() and company_name_1.get() and company_city_1.get():
        if company_id_1.get().isdigit() and int(company_id_1.get())>0 and int(company_id_1.get())<99:
            if all(x.isalpha() or x.isspace() for x in company_name_1.get()) and (len(company_name_1.get()) > 0):
                if all(x.isalpha() or x.isspace() for x in company_city_1.get()) and (len(company_city_1.get()) > 0):
                    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO company (COMPANY_ID, COMPANY_NAME, COMPANY_CITY) VALUES('" + company_id_1.get() + "', '"+  company_name_1.get() + "', '"+  company_city_1.get() + "' );"                                
                    cursor.execute(insert_query) # executing the queries 
                    connection.commit() # commiting the connection then closing it. 
                    connection.close() # closing the connection of the database 
                    Label(screen4_4, text="New Company Added Successfully ", bg="white", font=("Roboto", 11), width='3000', anchor=W, fg='green').place(x=0, y=570)
                    pass
                else:
                    Label(screen4_4, text=" ⚠  Company Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                    return
            else:
                Label(screen4_4, text=" ⚠  City Name should not have numbers or special characters", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
                return
        else:
            Label(screen4_4, text=" ⚠  Company ID should numbers in range 1-99", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
            return
    else:
        Label(screen4_4, text=" ⚠ Please Fill All The Details", fg="red", font=( "Roboto", 11), width='3000', anchor=W, bg='black').place(x=0, y=570)
        return

def balance_report():
    global screen5_1
    bal = []
    screen5_1 = Toplevel(screen) 
    screen5_1.title("Balance Amount Report") 
    adjustWindow(screen5_1) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen5_1, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen5_1, text="Balance Amount Report ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor()   
    select_query = "SELECT * ,(ORD_AMOUNT-ADVANCE_AMOUNT) AS BALANCE_AMT FROM orders LEFT JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE ORDER BY `BALANCE_AMT` DESC ;"                                
    cursor.execute(select_query) # executing the queries 
    bal = cursor.fetchall()
    alpha = [0,13,5,8]
    k = 0
    new_li = [[0 for x in range(4)] for y in range(len(bal))]
    for i in range(len(bal)):
        for j in alpha:
            new_li[i][k] = bal[i][j]
            k+=1
            if k == 4:
                k=k-4
    connection.commit() # commiting the connection then closing it. 
    connection.close() # closing the connection of the database 
    tv = ttk.Treeview(screen5_1, columns=(1,2,3,4), show = "headings", height = '20')
    tv.place(relx=.5, rely=.5, anchor="center")
    verscrlbar = ttk.Scrollbar(screen5_1,  
                           orient ="vertical",  
                           command = tv.yview) 
    verscrlbar.place(relx=.9, rely=.175, height=425)
    tv.configure(yscrollcommand = verscrlbar.set) 
    tv.column(1, width=130, minwidth=130, stretch=NO)
    tv.column(2, width=130, minwidth=130, stretch=NO)
    tv.column(3, width=80, minwidth=80)
    tv.column(4, width=150, minwidth=150, stretch=NO)
    tv.heading(1,text="Order Number",anchor = W)
    tv.heading(2, text="Balance Amount",anchor = W)
    tv.heading(3, text="Agent Code",anchor = W)
    tv.heading(4, text="Agent Name",anchor = W)
    for item in new_li:
        tv.insert('', 'end', values = item)
    Button(screen5_1, image = back, border = 0, command=screen5_1.destroy).place(relx=.5, rely=.95, anchor="center")
    screen5_1.mainloop()

def cumulative_data():
    global screen5_2 
    country_names = []
    screen5_2 = Toplevel(screen) 
    screen5_2.title("Cumulative Data Report") 
    adjustWindow(screen5_2) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(screen5_2, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen5_2, text="Cumulative Data Report ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Label(screen5_2, text="Cumulative Data of All Customers",width='500', font=("Roboto lt", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.2,anchor='w')
    Label(screen5_2, text="Payment Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.3,anchor='center')
    Label(screen5_2, text="Outstanding Amount : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.4,anchor='center')
    Label(screen5_2, text="Country with Maximum number of Customers",width='500', font=("Roboto ", 10 , 'italic'), bg='black', fg='white',anchor=W).place(relx=0, rely=.5,anchor='w')
    Label(screen5_2, text="Country Name : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.6,anchor='center')
    Label(screen5_2, text="Number of Customers : ",width='50', font=("Roboto ", 13 , 'italic'), bg='black', fg='white',anchor=W).place(relx=.5, rely=.7,anchor='center')
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor() 
    select_query =  "SELECT SUM(`PAYMENT_AMT`) FROM `customer` "# queries for retrieving values 
    cursor.execute(select_query) # executing the queries 
    cum_payment_amt = cursor.fetchall()
    select_query =  "SELECT SUM(`OUTSTANDING_AMT`) FROM `customer` "# queries for retrieving values 
    cursor.execute(select_query)
    cum_outstanding_amt = cursor.fetchall()
    select_query =  "SELECT `CUST_COUNTRY` FROM `customer`"
    cursor.execute(select_query)
    c_name = cursor.fetchall()
    connection.commit() # commiting the connection then closing it. 
    connection.close()
    Label(screen5_2, text= cum_payment_amt[0][0],width='20', font=("Roboto ", 13 , 'italic'),fg='black', bg='white',anchor=E).place(relx=.9, rely=.3,anchor='e')
    Label(screen5_2, text= cum_outstanding_amt[0][0] ,width='20', font=("Roboto ", 13 , 'italic'), fg='black', bg='white',anchor=E).place(relx=.9, rely=.4,anchor='e')
    for i in range(len(c_name)):
        country_names.append(c_name[i][0])
    c=Counter(country_names).most_common(1)
    Label(screen5_2, text= c[0][0],width='20', font=("Roboto ", 13 , 'italic'), fg='black', bg='white',anchor=E).place(relx=.9, rely=.6,anchor='e')
    Label(screen5_2, text= c[0][1] ,width='20', font=("Roboto ", 13 , 'italic'),fg='black', bg='white',anchor=E).place(relx=.9, rely=.7,anchor='e')
    Button(screen5_2, image = back, border = 0, command=screen5_2.destroy).place(relx=.5, rely=.95, anchor="center")
    screen5_2.mainloop()

def insight_options():
    global insight_menu
    insight_menu = Toplevel(screen) 
    insight_menu.title("Insights Options") 
    adjustWindow(insight_menu) # configuring the window 
    back,show = PhotoImage(file="back.png"),PhotoImage(file="show.png")
    i1,i2,i3,i4,i5,i6,i7 = PhotoImage(file="i_1.png"),PhotoImage(file="i_2.png"),PhotoImage(file="i_3.png"),PhotoImage(file="i_4.png"),PhotoImage(file="i_5.png"),PhotoImage(file="i_6.png"),PhotoImage(file="i_7.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_menu, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_menu, text="Insights", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    Button(insight_menu, image = i1, border = 0 ,command=insight_1).place(relx=.5, rely=.2, anchor="center")
    Button(insight_menu, image = i2, border = 0 ,command=insight_2).place(relx=.5, rely=.3, anchor="center")
    Button(insight_menu, image = i3, border = 0 ,command=insight_3).place(relx=.5, rely=.4, anchor="center")
    Button(insight_menu, image = i4, border = 0 ,command=insight_4).place(relx=.5, rely=.5, anchor="center")
    Button(insight_menu, image = i5, border = 0 ,command=insight_5).place(relx=.5, rely=.6, anchor="center")
    Button(insight_menu, image = i6, border = 0 ,command=insight_6).place(relx=.5, rely=.7, anchor="center")
    Button(insight_menu, image = i7, border = 0 ,command=insight_7).place(relx=.5, rely=.8, anchor="center")
    Button(insight_menu, image = back, border = 0, command=insight_menu.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_menu.mainloop()

def insight_1():
    global insight_1_screen
    insight_1_screen = Toplevel(screen) 
    insight_1_screen.title("Total Property Area Sold vs Leased ") 
    adjustWindow(insight_1_screen) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_1_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_1_screen, text="Total Property Area Sold vs Leased ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    owned= df[(df['Tenure']=='Owned') & (df['UoM']=='SQ-M')]
    sumo=list(owned.groupby(['Year'])['Area'].sum())
    leased= df[(df['Tenure']=='Leased') & (df['UoM']=='SQ-M')]
    suml=list(leased.groupby(['Year'])['Area'].sum())
    years=sorted(df['Year'].unique())
    figure1 = plt.Figure(figsize=(7,5), dpi=85)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_1_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    df1 = pd.DataFrame({'Sold': sumo,'Leased': suml}, index=years)
    df1.plot(kind='bar', ax=ax1,title='Total Property Area Sold vs Total Property Area Leased (in SQ-M only)')#,autopct='%1.2f%%',startangle=0,subplots=True,legend=False)
    toolbarFrame = Frame(master=insight_1_screen)
    toolbarFrame.place(relx=.25,rely=.85)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update()
    Button(insight_1_screen, image = back, border = 0, command=insight_1_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_1_screen.mainloop()

def insight_2():
    global insight_2_screen,countryselect
    insight_2_screen = Toplevel(screen) 
    insight_2_screen.title("Year With Maximum Leased Area ") 
    adjustWindow(insight_2_screen) # configuring the window 
    back,show2 = PhotoImage(file="back.png"),PhotoImage(file="show_2.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_2_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_2_screen, text="Year With Maximum Leased Area ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    countryselect=StringVar()
    country = ['Country','CA','WS']
    droplist = ttk.OptionMenu(insight_2_screen, countryselect, *country) 
    droplist.config(width=12) 
    countryselect.set('CA') 
    droplist.place(relx=.3, rely=.1, anchor="center")
    Button(insight_2_screen, image = show2, border = 0, command=insight_2_countryselect).place(relx=.7, rely=.1, anchor="center")
    Button(insight_2_screen, image = back, border = 0, command=insight_2_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_2_screen.mainloop()

def insight_2_countryselect():
    leased_sqm = df[(df['Tenure']=='Leased') & (df['Country'] == countryselect.get())& (df['Year'] != 2020)& (df['UoM']=='SQ-M')]
    leased_ha = df[(df['Tenure']=='Leased') & (df['Country'] == countryselect.get())& (df['Year'] != 2020) & (df['UoM']=='HA')]
    leased_sqm_sum=list(leased_sqm.groupby(['Year'])['Area'].sum())
    leased_ha_sum=list(leased_ha.groupby(['Year'])['Area'].sum())
    for i in range(len(leased_ha_sum)):
        leased_sqm_sum[i] = leased_sqm_sum[i]+ (leased_ha_sum[i]*10000)
    years=sorted(leased_sqm['Year'].unique()) 
    figure1 = plt.Figure(figsize=(7,5), dpi=80)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_2_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    yearselect = 'CA'
    df1 = pd.DataFrame({'Total Leased Area ': leased_sqm_sum}, index=years)
    df1.plot(kind='pie', ax=ax1,autopct='%1.2f%%',startangle=0,subplots=True,legend=False,title='Total Leased Area in '+countryselect.get()+' (represented in SQ-M)')
    toolbarFrame = Frame(master=insight_2_screen)
    toolbarFrame.place(relx=.25,rely=.85)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update()

def insight_3():
    global insight_3_screen
    insight_3_screen = Toplevel(screen) 
    insight_3_screen.title("Codes of Agents with OWNED Deals across the years") 
    adjustWindow(insight_3_screen) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_3_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_3_screen, text="Agents with OWNED Deals across the years", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    agent,count,code,temp=[],[],[],[]
    df_temp = df[(df['Tenure']=='Owned')]
    a = Counter(df_temp['Agent']).most_common(50)
    for i in a:
        agent.append(i[0])
        count.append(i[1])    
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor() 
    for i in agent:
        select_query =  "SELECT * FROM agents where AGENT_NAME = '" + i + "';" # queries for retrieving values 
        cursor.execute(select_query) # executing the queries 
        info = cursor.fetchall()
        if info:
            temp.append(info[0][0])
            i=i+' ( '+info[0][0]+')'
            code.append(i)
    while(len(count)!=len(code)):
        count.pop()
    connection.commit() # commiting the connection then closing it. 
    connection.close()
    df1 = pd.DataFrame({'Agent Code': temp,'OWNED Deals': count})
    figure1 = plt.Figure(figsize=(8,6.5), dpi=70)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1,insight_3_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.475,anchor='center')
    df1 = df1[['Agent Code','OWNED Deals']].groupby('Agent Code').sum()
    df1.plot(title='Codes of Agents with OWNED Deals across the years 2017-2020',kind='bar', ax=ax1,subplots=True, legend = True)#,autopct='%1.2f%%',startangle=0)
    toolbarFrame = Frame(master=insight_3_screen)
    toolbarFrame.place(relx=.25,rely=.86)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update() 
    Button(insight_3_screen, image = back, border = 0, command=insight_3_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_3_screen.mainloop()

def insight_4():
    global insight_4_screen
    insight_4_screen = Toplevel(screen) 
    insight_4_screen.title("Agent with maximum leased deals in Chilliwack ") 
    adjustWindow(insight_4_screen) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_4_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_4_screen, text="Maximum leased deals in Chilliwack", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    agents,count = [],[]
    chill = df[(df['City']=='Chilliwack') & (df['Tenure']=='Leased')]
    chill_agents = Counter(chill['Agent']).most_common(50)
    for i in range(len(chill_agents)):
        agents.append(chill_agents[i][0])
        count.append(chill_agents[i][1])
    figure1 = plt.Figure(figsize=(7,5), dpi=85)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_4_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    df1 = pd.DataFrame({'No of Leased Deals in Chilliwack ': count}, index=agents)
    df1.plot(kind='bar', ax=ax1,title='Agent with maximum leased deals in Chilliwack')#,autopct='%1.2f%%',startangle=0,subplots=True)
    toolbarFrame = Frame(master=insight_4_screen)
    toolbarFrame.place(relx=.25,rely=.85)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update() 
    Button(insight_4_screen, image = back, border = 0, command=insight_4_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_4_screen.mainloop()

def insight_5():
    global insight_5_screen,yearselect
    yearselect=StringVar()
    year = ['Year','2017','2018','2019']
    insight_5_screen = Toplevel(screen) 
    insight_5_screen.title("Agent Performance Comparison ") 
    adjustWindow(insight_5_screen) # configuring the window 
    back,show = PhotoImage(file="back.png"),PhotoImage(file="show.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_5_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_5_screen, text="Agent Performance Comparison ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    droplist = ttk.OptionMenu(insight_5_screen, yearselect, *year) 
    droplist.config(width=12) 
    yearselect.set('2017') 
    droplist.place(relx=.3, rely=.1, anchor="center")
    Button(insight_5_screen, image = show, border = 0, command=insight_5_yearselect).place(relx=.7, rely=.1, anchor="center")
    Button(insight_5_screen, image = back, border = 0, command=insight_5_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_5_screen.mainloop()
    
def insight_5_yearselect():
    agent1,area1,agent2,area2=[],[],[],[]
    x1 = df[(df['Tenure']=='Owned') & (df['Year'] == int(yearselect.get())) ]
    y1 = df[(df['Tenure']=='Leased') & (df['Year'] == int(yearselect.get())) ]
    for a,row in x1.iterrows():
        if row['UoM'] == 'HA':
            row['Area'] = row['Area']*10000
        area1.append(row['Area'])
        agent1.append(row['Agent'])
    for a,row in y1.iterrows():
        if row['UoM'] == 'HA':
            row['Area'] = row['Area']*10000
        area2.append(row['Area'])
        agent2.append(row['Agent'])
    x2 = pd.DataFrame({'Agent': agent1,'Area': area1})
    y2 = pd.DataFrame({'Agent': agent2,'Area': area2})
    x3=list(x2.groupby(['Agent'])['Area'].sum())
    y3=list(y2.groupby(['Agent'])['Area'].sum())
    if yearselect.get()=='2019':
        y3.insert(-3,0)
    agent=sorted(x2['Agent'].unique())
    figure1 = plt.Figure(figsize=(8,5), dpi=70)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_5_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    df1 = pd.DataFrame({'Owned Area': x3,'Leased Area':y3}, index=agent)
    df1.plot(kind='bar',ax=ax1,title='Performance of Agents in Year '+yearselect.get())#,legend=False)
    toolbarFrame = Frame(master=insight_5_screen)
    toolbarFrame.place(relx=.25,rely=.82)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update() 

def insight_6():
    global insight_6_screen
    insight_6_screen = Toplevel(screen) 
    insight_6_screen.title("Total area sold in July") 
    adjustWindow(insight_6_screen) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_6_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_6_screen, text="Total area sold in July ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    x = df[(df['Month']=='JUL') & (df['Tenure']=='Owned') & (df['UoM']=='SQ-M')]
    y = df[(df['Month']=='JUL') & (df['Tenure']=='Owned') & (df['UoM']=='HA')]
    sumsqm=list(x.groupby(['Year'])['Area'].sum())
    sumha=list(y.groupby(['Year'])['Area'].sum())
    years = sorted(x['Year'].unique())
    for i in range(len(sumha)):
        sumsqm[i] = sumsqm[i]+ (sumha[i]*10000)
    figure1 = plt.Figure(figsize=(7,5), dpi=85)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_6_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    df1 = pd.DataFrame({'Total Area (represented in SQ-M)': sumsqm}, index=years)
    df1.plot(kind='bar', ax=ax1, title='Total Area Sold in the month of July across the Years (represented in SQ-M)')#,autopct='%1.2f%%',startangle=0)
    toolbarFrame = Frame(master=insight_6_screen)
    toolbarFrame.place(relx=.25,rely=.86)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update() 
    Button(insight_6_screen, image = back, border = 0, command=insight_6_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_6_screen.mainloop()

def insight_7():
    global insight_7_screen
    insight_7_screen = Toplevel(screen) 
    insight_7_screen.title("Time Series Analysis ") 
    adjustWindow(insight_7_screen) # configuring the window 
    back = PhotoImage(file="back.png")
    image1= PhotoImage(file="bg_1.png")
    label_for_image= Label(insight_7_screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(insight_7_screen, text="Time Series Analysis ", width='500', height="1", font=("Ariel", 20,), fg='white', bg='#43315E', anchor =W).pack()
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="sales") # database connection 
    cursor = connection.cursor() 
    select_query =  "SELECT ORD_AMOUNT,ORD_DATE FROM orders ORDER BY orders.ORD_DATE ASC ;" # queries for retrieving values 
    cursor.execute(select_query) # executing the queries 
    info = cursor.fetchall()
    amt,dt = [],[] 
    for i in info:
        amt.append(float(i[0]))
        dt.append(i[1])
    connection.commit() # commiting the connection then closing it. 
    connection.close()
    figure1 = plt.Figure(figsize=(12,5), dpi=60)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, insight_7_screen)
    bar1.draw()
    bar1.get_tk_widget().place(relx=.5,rely=.5,anchor='center')
    df7 = pd.DataFrame({'Order Amount ': amt}, index=dt)
    df7.plot(ax=ax1 , title='Time series analysis of all orders in  year ' + str(info[0][1].year)+'-'+ str(info[-1][1].year))#,autopct='%1.2f%%',startangle=0,subplots=True)
    toolbarFrame = Frame(master=insight_7_screen)
    toolbarFrame.place(relx=.25,rely=.755)
    toolbar = NavigationToolbar2Tk(bar1, toolbarFrame)
    toolbar.update() 
    Button(insight_7_screen, image = back, border = 0, command=insight_7_screen.destroy).place(relx=.5, rely=.95, anchor="center")
    insight_7_screen.mainloop()

def main_screen(): 
    global screen, username_verify, password_verify 
    screen = tk.ThemedTk()
    screen.get_themes()                 
    screen.set_theme("arc")# initializing the tkinter window 
    username_verify, password_verify = StringVar(),StringVar() 
    screen.title("Login")  # mentioning title of the window 
    adjustWindow(screen)  # configuring the window 
    image1, login_button, register_button = PhotoImage(file="login_final_1.png"),PhotoImage(file="login_button_3.png"),PhotoImage(file="register_button_3.png")
    label_for_image= Label(screen, image=image1)
    label_for_image.place(x=0, y=0, relwidth=1, relheight=1)
    Label(screen, text="E-mail ID ", font=("Roboto lt", 8 , 'italic'), bg='black', fg='white').place(relx=.337, rely=.35, anchor="center")
    Label(screen, text="Password ", font=("Roboto lt", 8, 'italic'), bg='black', fg='white').place(relx=.3425, rely=.45, anchor="center")
    ttk.Entry(screen, textvar=username_verify , width='39').place(relx=.5, rely=.39, anchor="center")
    ttk.Entry(screen, textvar=password_verify, show="*" , width='39').place(relx=.5, rely=.49, anchor="center")
    Button(screen, image = login_button , border = 0, command=login_verify).place(relx=.5, rely=.63, anchor="center") 
    Button(screen, image = register_button , border = 0, command=register).place(relx=.5, rely=.73, anchor="center")
    screen.mainloop() 

main_screen() 