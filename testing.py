import streamlit as st
st.set_page_config(page_title="Employee Management Tool", page_icon=":bar_chart:", layout="wide")
import numpy as np
from streamlit_option_menu import option_menu
import psycopg2
from datetime import datetime
import random
from psycopg2.extensions import AsIs
import hydralit_components as hc
import pickle
from pathlib import Path
import pandas as pd  # pip install pandas openpyxl
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from PIL import Image
import re

image = Image.open('logo.jpeg')
current_dateTime = datetime.now()

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.shaper.co.za/" target="_blank">Shaper Devs</a></p>
</div>
"""
def connection():
    conn = psycopg2.connect(database="ems_app",
        host="localhost",
        user="postgres",
        password="",
        port="5436")
    cursor = conn.cursor()
    return cursor, conn

# --- USER AUTHENTICATION ---


# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
credentials = {"usernames":{}}

for uname,name,pwd in zip(usernames,names,hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})
        
authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    
    st.image(image)
    menu_data = [
        {'label':"View/Edit/Delete Employee"},
        {'label':"Add Employees"},
        {'label':"Add/Edit/Delete Departments"},
        {'label':"Add/Edit Roles"},
        {'label':"Add/Edit Skill"},
        {'label':"Add/Edit Project"},
        {'label':"View And Approve Leave"},
        {'label':"Add Contact Details"},
        {'label':"Add Payment Details"},
    ]

    menu_id = hc.nav_bar(menu_definition=menu_data)

    choice = menu_id

    if choice=='View/Search Employee':
        try:
            conn, cur = connection()
            conn.execute("SELECT id, dept_name FROM departments")
            deptss = conn.fetchall()
            deptss =  pd.DataFrame(deptss, columns=['id','name'])
        
            COHORT = st.selectbox(
            "Select department",
            (deptss['name']),
            index=None,
            placeholder="Select department here...",
            )
            conn.close()
        except:
            st.write("Please make sure that you select a user")
            st.stop()
            
        try:
            conn, cur = connection()
            conn.execute("SELECT id, firstname, lastname , male, idnumber FROM employees")
            ddd = conn.fetchall()
            personal =  pd.DataFrame(ddd, columns=['id','firstname','lastname','male','idnumber'])
            personal['fullname'] = personal['firstname'] + " " + personal['lastname']
            conn.close()
        except:
            st.write("Please make sure that you select a user")
            st.stop()

        option = st.selectbox(
        "Search for employee",
        (personal['fullname']),
        index=None,
        placeholder="type employee name...",
        )
        tab1, tab2, tab3, tab4= st.tabs(["Personal Details", "Contact Details", "Educational Details","Dependants Details" ])

        with tab1:
                                
                if option:
                    st.header("Personal Details")
                    try:
                        st.session_state.dff = personal

                        edited_dff = st.data_editor(st.session_state.dff)
                        st.write(edited_dff['id'][0])
                        st.session_state.dff = edited_dff

                        id = edited_dff['id'][0]
                        fn = edited_dff['firstname'][0]
                        ln =edited_dff['lastname'][0]
                        male =edited_dff['male'][0]
                        idnumber = edited_dff['idnumber'].astype(np.int64)
                        conn.execute("UPDATE employees SET firstname=%s, lastname=%s, male=%s, idnumber=%s  where id = %s", (fn,ln,bool(male),int(idnumber), int(id)))
                        cur.commit()
                      
                        st.write('df at end:',ln)
                        if st.button("delete"):
                            conn.execute("DELETE FROM employees where id = %s",(int(id),))
                            cur.commit()
                        conn.close()
                        
                    except:
                        st.write(int(id))
                        st.stop()

        with tab2:
            st.header("Contact Details")
                                
            try:
                conn, cur = connection()
                conn.execute("SELECT id, physicaladdress, postaladdress , phonenumber, email, postalcode FROM employee_contacts where id=%s", (int(id),))
                ccc = conn.fetchall()
                contacts =  pd.DataFrame(ccc, columns=['id', 'physicaladdress', 'postaladdress' , 'phonenumber', 'email', 'postalcode'])
             
                st.session_state.dfff = contacts

                edited_dfff = st.data_editor(st.session_state.dfff)
                st.write(edited_dfff['id'][0])
                st.session_state.dfff = edited_dfff

                id = edited_dfff['id'][0]
                pa = edited_dfff['physicaladdress'][0]
                poa =edited_dfff['postaladdress'][0]
                phone =edited_dfff['phonenumber'][0]
                email = edited_dfff['email'][0]
                conn.execute("UPDATE employee_contacts SET physicaladdress=%s, postaladdress=%s,phonenumber=%s, email=%s  where id = 1", (pa,poa,int(phone),email))
                cur.commit()

                st.write('df at end:',ln)
                if st.button("deletion"):
                    conn.execute("DELETE FROM employee_contacts where id = %s", int(id))
                    cur.commit()
                conn.close()
                                                
            except:
                st.write("Please make sure that you select a user")
                st.stop()

        with tab3:
            st.header("Educational Details")
                                      

        with tab4:
            st.header("Dependants Details")

                            

        
    elif choice=='Add Employees':
                            
                
                #  st.button("Add"):
                with st.form("my_form"):

                    conn, cur = connection()
                    conn.execute("SELECT id, name FROM roleees")
                    roleesoption = conn.fetchall()
                    roleesoption =  pd.DataFrame(roleesoption, columns=['id','name'])
                    
                    conn, cur = connection()
                    conn.execute("SELECT id, dept_name FROM departments")
                    deptoption = conn.fetchall()
                    deptoption =  pd.DataFrame(deptoption, columns=['id','dept_name'])
                    
                    col1, col2, col3, col4,col5 = st.columns(5)

                    with col1:
                        st.header("Personal Info")
                        fn = st.text_input("Firstname:")
                        ln = st.text_input("Lastname:")
                        initials = st.text_input("Initials:")
                        gender = st.selectbox('Please Select Gender:',
                                              ('Male', 'Female')) 
                        if gender =='Male':
                            genderid = True
                        idnumber = st.text_input("ID Number:")
                    with col2:
                        st.header("Contact Details")
                        physicaladd = st.text_area("Postal Address")
                        postaladd = st.text_area("Postal Address:")
                        phone = st.text_input("Phone Number:")
                        email = st.text_input("Email:")
                        postalcode = st.text_input("Postal Code:")
                    with col3:
                        st.header("Qualification")
                        qualification  = st.text_input("Qualification")
                        level = st.text_input("Level:")
                        dateobtained = st.date_input("When did you Obtain this?")
                    with col4:
                        st.header("Dept/Role/Skill")
                        role = st.selectbox('Please Select Role Below:',
                                              (roleesoption['name']))
                        
                       
                        skill  = st.selectbox('Please Select Skill Below:',
                                              ('Email', 'Home phone', 'Mobile phone'))
                        if skill =='Email':
                            skillid = 1

                        department  = st.selectbox('Please Select Department Below:',
                                              (deptoption['dept_name']))
                    

                    with col5:
                        st.header("Dependants")
                        Dependant  = st.text_input("Dependant:")   
                        genderD  = st.selectbox('Please Select Gender Below:',
                                              ('Male', 'Female'))    
                        if genderD =='Male':
                            genderDid = True           
                        relationship  = st.selectbox('Please Select Relationship Below:',
                                              ('Email', 'Home phone', 'Mobile phone'))    
                        if relationship =='Email':
                            relationshipid = 1            
                        phonenumber  = st.text_input("Contact Number:")                    

                        # def validate_email(email):  
                        #     if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
                        #         return True  
                        #     return st.write("Please make sure email is valid")
    
                        # validate_email(email)

                # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        cc = 1
                        conn, cur = connection()
                        conn.execute("INSERT into employees(firstname, lastname, initials,male, idnumber, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s )", (fn,ln, initials,genderid, idnumber,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                        cur.commit()
                        # conn.close()

                        conn.execute("SELECT id from employees where firstname=%s AND lastname=%s", (fn,ln))
                        ccc = conn.fetchall()
                        employee =  pd.DataFrame(ccc, columns=['id'])
                        employeeid = employee['id'][0]

                        conn.execute("INSERT into employee_contacts(physicaladdress, postaladdress, phonenumber,email, postalcode, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s )", (physicaladd,postaladd, phone,email, postalcode,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                        cur.commit()

                        conn.execute("SELECT id from employee_contacts where physicaladdress=%s AND phonenumber=%s", (physicaladd,phone))
                        ccc = conn.fetchall()
                        employee_contacts =  pd.DataFrame(ccc, columns=['id'])
                        contactid = employee_contacts['id'][0]

                        conn.execute("INSERT into employees_employee_contacts_links(employee_id,employee_contact_id,employee_contact_order, employee_order) VALUES (%s, %s, %s, %s )", (int(employeeid),int(contactid), int(contactid),int(contactid)))
                        cur.commit()

                        conn.execute("INSERT into educations(qualification, level, dateobtained, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s )", (qualification,level, dateobtained,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                        cur.commit()

                        conn.execute("SELECT id from educations where qualification=%s AND dateobtained=%s", (qualification,dateobtained))
                        ccc = conn.fetchall()
                        education =  pd.DataFrame(ccc, columns=['id'])
                        educationid = education['id'][0]


                        conn.execute("INSERT into employees_educations_links(employee_id, education_id,education_order, employee_order) VALUES (%s, %s,%s, %s)", (int(employeeid),int(educationid), int(educationid),int(educationid)))
                        cur.commit()

                        conn.execute("INSERT into dependants(name, relationship, phonenumber, male, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s )", (Dependant,relationship, phonenumber,genderDid,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                        cur.commit()

                        conn.execute("SELECT id from dependants where name=%s AND phonenumber=%s", (Dependant,phonenumber))
                        ccc = conn.fetchall()
                        dependants =  pd.DataFrame(ccc, columns=['id'])
                        dependantsid = dependants['id'][0]


                        conn.execute("INSERT into employees_dependants_links(employee_id, dependant_id,dependant_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(dependantsid), int(dependantsid),int(dependantsid)))
                        cur.commit()

                        # conn.execute("INSERT into roleees(name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (name,description, phonenumber,genderDid,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                        # cur.commit()

                        conn.execute("SELECT id from roleees where name=%s ", (role,))
                        ccc = conn.fetchall()
                        roles =  pd.DataFrame(ccc, columns=['id'])
                        roleeeid = roles['id'][0]


                        conn.execute("INSERT into employees_rolees_links(employee_id, roleee_id,roleee_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(roleeeid), int(roleeeid),int(roleeeid)))
                        cur.commit()

                        conn.execute("SELECT id from departments where dept_name=%s ", (department,))
                        ccc = conn.fetchall()
                        depts =  pd.DataFrame(ccc, columns=['id'])
                        deptid = depts['id'][0]


                        conn.execute("INSERT into departments_employees_links(employee_id, department_id,department_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(deptid), int(deptid),int(deptid)))
                        cur.commit()
                  
            
    elif choice=='Add/Edit Departments':
            
            with st.form("my_form"):
                dept_name = st.text_input("Department Name:")
                description = st.text_input("Description:")
            # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    cc = 1
                    conn, cur = connection()
                    conn.execute("INSERT into departments(dept_name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (dept_name,description,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                    cur.commit()
                    conn.close()
                    
         
            conn, cur = connection()
            conn.execute("SELECT id, dept_name, description FROM departments")
            ddd = conn.fetchall()
            departmentdata =  pd.DataFrame(ddd, columns=['id','dept_name','description'])
            option = st.selectbox(
            "Search for employee",
            (departmentdata['dept_name']),
            index=None,
            placeholder="type employee name...",
            )
            if option:
                departmentdata = departmentdata[departmentdata["dept_name"]== option]
                st.header("Show Departments")
                try:
                        st.session_state.dfffff = departmentdata

                        departmentdata2 = st.data_editor(st.session_state.dfffff)
                        st.write(departmentdata2['dept_name'][0])
                        st.session_state.dfffff = departmentdata2

                        id = departmentdata2['id'][0]
                        dn = departmentdata2['dept_name'][0]
                        ddesc =departmentdata2['description'][0]

                        conn.execute("UPDATE departments SET dept_name=%s, description=%s  where id = %s", (dn,ddesc, int(id)))
                        cur.commit()
                      
                        st.write('df at end:',id)

                        if st.button("deletess"):
                            conn.execute("DELETE FROM departments where id = %s",(int(id),))
                            cur.commit()

                        conn.close()
                        
                except:
                        st.write(int(id))
                        st.stop()
        

    elif choice=='Add/Edit Roles':
            with st.form("my_form"):
                role = st.text_input("Role Name:")
                description = st.text_input("Description:")
            # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    cc = 1
                    conn, cur = connection()
                    conn.execute("INSERT into roleees(name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (role,description,current_dateTime,current_dateTime,current_dateTime,cc,cc))
                    cur.commit()
                    conn.close()

    elif choice=='Add Skill':
            with st.form("my_form"):
                fn = st.text_input("Team Name:")
                ln = st.text_input("Description:")

                # Every form must have a submit button.
                submitted = st.form_submit_button("submit")


    elif choice=='Add Project':
            with st.form("my_form"):
                fn = st.text_input("Team Name:")
                ln = st.text_input("Description:")

                # Every form must have a submit button.
                submitted = st.form_submit_button("submit")


    elif choice=='Add Tech Skill Rating':
            with st.form("my_form"):
                fn = st.text_input("Team Name:")
                ln = st.text_input("Description:")

                # Every form must have a submit button.
                submitted = st.form_submit_button("submit")

    elif choice=='Search':
            with st.form("my_form"):
                conn = psycopg2.connect(database="shaper",
                host="dpg-ckp2uroujous73d8htug-a.oregon-postgres.render.com",
                user="admin",
                password="NFLa5XvzRkU9ihAFxJ91WsX0zfy1jdcv",
                port="5432")
                cursor = conn.cursor()
                cursor.execute("SELECT firstname, lastname FROM learners" )
                xxx = cursor.fetchall()
                cursor.close()

                option = st.selectbox(
                "Search for Learner",
                (xxx),
                index=None,
                placeholder="Select learner...",
                )

                # Every form must have a submit button.
                submitted = st.form_submit_button("submit")
                if submitted:
                    firstname = option[:-1][0]
                    lastname = option[1:][0]
                    cursor = conn.cursor()
                    xx = cursor.execute("SELECT * FROM learners where firstname = %s and  lastname = %s", (firstname, lastname))
                        
                    st.write(xx)
    
st.markdown(footer,unsafe_allow_html=True)
