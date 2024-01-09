import streamlit as st

st.set_page_config(page_title="Employee Management Tool", page_icon=":bar_chart:", layout="wide")
import json
import pickle
import random
import re
from datetime import datetime
from pathlib import Path

import hydralit_components as hc
import numpy as np
import pandas as pd  # pip install pandas openpyxl
import psycopg2
import requests
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from PIL import Image
from psycopg2.extensions import AsIs
from streamlit_option_menu import option_menu

image = Image.open('logo.jpeg')
st.image(image)
current_dateTime = datetime.now()
menu_data = [
        {'label':"Manage Learner"},
        {'label':"Manage Team Leader"},
        {'label':"Manage Projects"},
        {'label':"Manage Cohorts"},
        # {'label':"Add/Edit Skill"},
        # {'label':"Add/Edit Project"},
        # {'label':"View And Approve Leave"},
        # {'label':"Add Contact Details"},
        # {'label':"Add Payment Details"},
    ]

menu_id = hc.nav_bar(menu_definition=menu_data)

choice = menu_id
sn = []
sln = []
sid = []

if choice=='Manage Learner':
    try:
        COHORT = st.selectbox(
                    "Select Cohort",
                    (['Data Science','UX/UI Design','Web Development']),
                    index=None,
                    placeholder="Select cohort here...",
                    )
        URLCOHORT = "http://localhost:1337/api/applicants?filters[$and][0][Program][$contains]="+str(COHORT)
        d = requests.get(URLCOHORT)
        dd = d.json()
        z = 0

        for i in range(20):
            sn.append(dd['data'][z]['attributes']['firstname'])
            sln.append(dd['data'][z]['attributes']['lastname'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sln,sid),columns=['firstname','lastname','id'])
        deptss['fullname'] = deptss['firstname'] + " " + deptss['lastname']
        LEARNER = st.selectbox(
                "Select a learner",
                (deptss['fullname']),
                index=None,
                placeholder="Select learner here...",
                )
        Learn = deptss[deptss['fullname'] == LEARNER]
        LEARNERID = Learn['id'].values
    except:
         st.write("Please select a cohort above")


    tab1, tab2, tab3, tab4, tab5= st.tabs(["Personal Details", "Contact Details", "Soft Skills Ratings","Technical Skills Ratings","Shaper Learner Review"  ])

    with tab1:
        try:
            url = "http://localhost:1337/api/applicants/" + str(LEARNERID[0])
            d = requests.get(url)
            dd = d.json()
            st.session_state.dff = dd['data']['attributes']
            x = pd.DataFrame(st.session_state.dff, index=[0])
            edited_dff = st.data_editor(x[['firstname','lastname','homelanguage','dob','southafrican','male','idnumber','nextofkin']]) 
            st.session_state.dff = edited_dff
        
            firstname = edited_dff['firstname'][0]
            lastname = edited_dff['lastname'][0]
            homelanguage = edited_dff['homelanguage'][0]
            dob = edited_dff['dob'][0]
            southafrican = edited_dff['southafrican'][0]
            male = edited_dff['male'][0]
            nextofkin = edited_dff['nextofkin'][0]
            idnumber = edited_dff['idnumber'][0]

            if st.button('Edit Personal Details'):

                requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "data": 
                            {
                                "firstname": firstname,
                                "lastname": lastname,
                                "dob": dob,
                                "male": str(male),
                                "southafrican": str(southafrican),
                                "homelanguage": homelanguage,
                                "nextofkin": nextofkin,
                                "idnumber": idnumber,
                            }
                    }))
        except:
            st.write("Please select a learner")


    with tab2:
        try:
            d = requests.get(url)
            dd = d.json()
            st.session_state.dff = dd['data']['attributes']
            x = pd.DataFrame(st.session_state.dff, index=[0])
            edited_dff = st.data_editor(x[['email','province','city','physicaladdress','postaladdress','nextofkin','postalcode','githublink', 'linkedinlink', 'nextofkinnumber']]) 
            st.session_state.dff = edited_dff
    
            email = edited_dff['email'][0]
            province = edited_dff['province'][0]
            city = edited_dff['city'][0]
            physicaladdress = edited_dff['physicaladdress'][0]
            postaladdress = edited_dff['postaladdress'][0]
            nextofkin = edited_dff['nextofkin'][0]
            postalcode = edited_dff['postalcode'][0]
            githublink = edited_dff['githublink'][0]
            linkedinlink = edited_dff['linkedinlink'][0]
            nextofkinnumber = edited_dff['nextofkinnumber'][0]

            if st.button('Edit Contact Details'):
                requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "data": 
                            {
                                "email": email,
                                "province": province,
                                "city": city,
                                "physicaladdress": physicaladdress,
                                "postaladdress": postaladdress,
                                "nextofkin": nextofkin,
                                "postalcode": str(postalcode),
                                "githublink": githublink,
                                "linkedinlink": linkedinlink,
                                "nextofkinnumber": nextofkinnumber,
                            }
                    }))
        except:
            st.write("")
    try:
        url2 = "http://localhost:1337/api/applicants/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews"
        d = requests.get(url2)
        dd = d.json()
    except:
         st.write("")

    with tab3:
        try:
            if (len(dd['data']['attributes']['softskillratings']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['softskillratings']['data'][0]['id']
                st.session_state.dff = dd['data']['attributes']['softskillratings']['data'][0]['attributes']
                edited_dff = st.data_editor(st.session_state.dff)  

                problemsolving = edited_dff['problemsolving'][0]
                interpersonal = edited_dff['interpersonal'][0]
                teamwork =edited_dff['teamwork'][0]
                communication =edited_dff['communication'][0]
                leadership = edited_dff['leadership']
                mostimproved = edited_dff['mostimproved']

                if st.button('Edit Soft Skills Ratings'):
                        ff = "http://localhost:1337/api/softskillratings/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "applicants": str(LEARNERID[0]),
                                    "problemsolving": problemsolving,
                                    "interpersonal": interpersonal,
                                    "communication": communication,
                                    "teamwork": teamwork,
                                    "leadership": leadership,
                                    }
                        }))
        except:
            with st.form("my_form"):
                    problemsolving = st.number_input("Problem Solving:")
                    interpersonal = st.number_input("Interpersonal:")
                    communication = st.number_input("Communication:")
                    teamwork = st.number_input("Team Work:")
                    leadership = st.number_input("Leadership:")
                    mostimproved = st.text_input("Most Improved Skill:")

                    submitted = st.form_submit_button("Add Ratings")
                    if submitted:

                        requests.post(
                        "http://localhost:1337/api/softskillratings/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": str(LEARNERID[0]),
                                    "problemsolving": problemsolving,
                                    "interpersonal": interpersonal,
                                    "communication": teamwork,
                                    "teamwork": communication,
                                    "leadership": leadership,
                                }
                            }
                        ),
                    )
                    
    with tab4:     
        try:
            if (len(dd['data']['attributes']['techskillratings']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['techskillratings']['data'][0]['id']
                st.session_state.dff1 = dd['data']['attributes']['techskillratings']['data'][0]['attributes']
                edited_dff1 = st.data_editor(st.session_state.dff1)  

                skill1 = edited_dff1['skill1'][0]
                skill2 = edited_dff1['skill2'][0]
                skill3 =edited_dff1['skill3'][0]
                skill4 =edited_dff1['skill4'][0]
                skill5 = edited_dff1['skill5'][0]
                mostimproved = edited_dff1['mostimproved'][0]

                if st.button('Edit Tech Skills Ratings'):
                        ff = "http://localhost:1337/api/technicalskills/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    
                                    {
                                    "applicants": str(LEARNERID[0]),
                                    "skill1": skill1,
                                    "skill2": skill2,
                                    "skill3": skill3,
                                    "skill4": skill4,
                                    "skill5": skill5,

                                    }
                        }))
        except:
            with st.form("my_form2"):
                    skill1 = st.number_input("Skill1:")
                    skill2 = st.number_input("Skill2:")
                    skill3 = st.number_input("Skill3:")
                    skill4 = st.number_input("Skill4:")
                    skill5 = st.number_input("Skill5:")
                    mostimproved = st.text_input("Most Improved Skill:")

                    submitted = st.form_submit_button("Add Ratings")
                    if submitted:

                        requests.post(
                        "http://localhost:1337/api/technicalskills/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": str(LEARNERID[0]),
                                    "skill1": skill1,
                                    "skill2": skill2,
                                    "skill3": skill3,
                                    "skill4": skill4,
                                    "skill5": skill5,
                                }
                            }
                        ),
                    )
with tab5:     
        try:
            if (len(dd['data']['attributes']['shaperreviews']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['shaperreviews']['data'][0]['id']
                st.session_state.dff1 = dd['data']['attributes']['shaperreviews']['data'][0]['attributes']
                edited_dff1 = st.data_editor(st.session_state.dff1)  

                review = edited_dff1['review']

                if st.button('Edit Review'):
                        ff = "http://localhost:1337/api/shaperreviews/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "learners": str(LEARNERID[0]),
                                    "review": review,
                                    }
                        }))
        except:
            with st.form("my_form3"):
                    review = st.text_input("Review:")

                    submitted = st.form_submit_button("Add Review")
                    if submitted:

                        requests.post(
                        "http://localhost:1337/api/shaperreviews/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "learners": str(LEARNERID[0]),
                                    "review": review,
                                }
                            }
                        ),
                    )
                     
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
# def connection():
#     conn = psycopg2.connect(database="ems_app",
#         host="localhost",
#         user="postgres",
#         password="",
#         port="5436")
#     cursor = conn.cursor()
#     return cursor, conn

# # --- USER AUTHENTICATION ---


# # load hashed passwords
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)
# credentials = {"usernames":{}}

# for uname,name,pwd in zip(usernames,names,hashed_passwords):
#     user_dict = {"name": name, "password": pwd}
#     credentials["usernames"].update({uname: user_dict})
        
# authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st.error("Username/Password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:
    
#     st.image(image)
#     menu_data = [
#         {'label':"View/Edit/Delete Employee"},
#         {'label':"Add Employees"},
#         {'label':"Add/Edit/Delete Departments"},
#         {'label':"Add/Edit Roles"},
#         {'label':"Add/Edit Skill"},
#         {'label':"Add/Edit Project"},
#         {'label':"View And Approve Leave"},
#         {'label':"Add Contact Details"},
#         {'label':"Add Payment Details"},
#     ]

#     menu_id = hc.nav_bar(menu_definition=menu_data)

#     choice = menu_id

#     if choice=='View/Search Employee':
#         try:
#             conn, cur = connection()
#             conn.execute("SELECT id, dept_name FROM departments")
#             deptss = conn.fetchall()
#             deptss =  pd.DataFrame(deptss, columns=['id','name'])
        
#             COHORT = st.selectbox(
#             "Select department",
#             (deptss['name']),
#             index=None,
#             placeholder="Select department here...",
#             )
#             conn.close()
#         except:
#             st.write("Please make sure that you select a user")
#             st.stop()
            
#         try:
#             conn, cur = connection()
#             conn.execute("SELECT id, firstname, lastname , male, idnumber FROM employees")
#             ddd = conn.fetchall()
#             personal =  pd.DataFrame(ddd, columns=['id','firstname','lastname','male','idnumber'])
#             personal['fullname'] = personal['firstname'] + " " + personal['lastname']
#             conn.close()
#         except:
#             st.write("Please make sure that you select a user")
#             st.stop()

#         option = st.selectbox(
#         "Search for employee",
#         (personal['fullname']),
#         index=None,
#         placeholder="type employee name...",
#         )
#         tab1, tab2, tab3, tab4= st.tabs(["Personal Details", "Contact Details", "Educational Details","Dependants Details" ])

#         with tab1:
                                
#                 if option:
#                     st.header("Personal Details")
#                     try:
#                         st.session_state.dff = personal
#                         edited_dff = st.data_editor(st.session_state.dff)
#                         st.write(edited_dff['id'][0])
#                         st.session_state.dff = edited_dff

#                         id = edited_dff['id'][0]
#                         fn = edited_dff['firstname'][0]
#                         ln =edited_dff['lastname'][0]
#                         male =edited_dff['male'][0]
#                         idnumber = edited_dff['idnumber'].astype(np.int64)
                        
#                         conn, cur = connection()
#                         conn.execute("UPDATE employees SET firstname=%s, lastname=%s, male=%s, idnumber=%s  where id = %s", (fn,ln,bool(male),int(idnumber), int(id)))
#                         cur.commit()
                      
#                         st.write('df at end:',ln)
#                         if st.button("delete"):
#                             conn.execute("DELETE FROM employees where id = %s",(int(id),))
#                             cur.commit()
#                         conn.close()
                        
#                     except:
#                         st.write(int(id))
#                         st.stop()

#         with tab2:
#             st.header("Contact Details")
                                
#             try:
#                 conn, cur = connection()
#                 conn.execute("SELECT id, physicaladdress, postaladdress , phonenumber, email, postalcode FROM employee_contacts where id = %s", (int(id),))
#                 ccc = conn.fetchall()
#                 contacts =  pd.DataFrame(ccc, columns=['id', 'physicaladdress', 'postaladdress' , 'phonenumber', 'email', 'postalcode'])
             
#                 st.session_state.dfff = contacts

#                 edited_dfff = st.data_editor(st.session_state.dfff)
#                 st.write(edited_dfff['id'][0])
#                 st.session_state.dfff = edited_dfff

#                 id = edited_dfff['id'][0]
#                 pa = edited_dfff['physicaladdress'][0]
#                 poa =edited_dfff['postaladdress'][0]
#                 phone =edited_dfff['phonenumber'][0]
#                 email = edited_dfff['email'][0]
                
#                 conn.execute("UPDATE employee_contacts SET physicaladdress=%s, postaladdress=%s,phonenumber=%s, email=%s  where id = %s", (pa,poa,int(phone),email,int(id))
#                 cur.commit()

#                 if st.button("deletion"):
#                     conn.execute("DELETE FROM employee_contacts where id = %s", int(id))
#                     cur.commit()
#                 conn.close()
                                                
#             except:
#                 st.write("Please make sure that you select a user")
#                 st.stop()

#         with tab3:
#             st.header("Educational Details")
                                      

#         with tab4:
#             st.header("Dependants Details")

                            

        
#     elif choice=='Add Employees':
                            
#                 #  st.button("Add"):
#                 with st.form("my_form"):
#                     try:
#                         conn, cur = connection()
#                         conn.execute("SELECT id, name FROM roleees")
#                         roleesoption = conn.fetchall()
#                         roleesoption =  pd.DataFrame(roleesoption, columns=['id','name'])
#                         conn.close()
#                     except:
#                         st.write("Something wrong with reading roleees tables")
#                         st.stop()
#                     try:
#                         conn, cur = connection()
#                         conn.execute("SELECT id, dept_name FROM departments")
#                         deptoption = conn.fetchall()
#                         deptoption =  pd.DataFrame(deptoption, columns=['id','dept_name'])
#                         conn.close()
#                     except:
#                         st.write("Something wrong with reading departments tables")
#                         st.stop()
#                     try:
#                         conn, cur = connection()
#                         conn.execute("SELECT id, skill_name FROM skills")
#                         skilllsoption = conn.fetchall()
#                         skilllsoption =  pd.DataFrame(skilllsoption, columns=['id','skill_name'])
#                         conn.close()
#                     except:
#                         st.write("Something wrong with reading roleees tables")
#                         st.stop()
                        
#                     col1, col2, col3, col4,col5 = st.columns(5)

#                     with col1:
#                         st.header("Personal Info")
#                         fn = st.text_input("Firstname:")
#                         ln = st.text_input("Lastname:")
#                         initials = st.text_input("Initials:")
#                         gender = st.selectbox('Please Select Gender:',
#                                               ('Male', 'Female')) 
#                         if gender =='Male':
#                             genderid = True
#                         idnumber = st.text_input("ID Number:")
                        
#                     with col2:
#                         st.header("Contact Details")
#                         physicaladd = st.text_area("Postal Address")
#                         postaladd = st.text_area("Postal Address:")
#                         phone = st.text_input("Phone Number:")
#                         email = st.text_input("Email:")
#                         postalcode = st.text_input("Postal Code:")
#                     with col3:
#                         st.header("Qualification")
#                         qualification  = st.text_input("Qualification")
#                         level = st.text_input("Level:")
#                         dateobtained = st.date_input("When did you Obtain this?")
#                     with col4:
#                         st.header("Dept/Role/Skill")
#                         role = st.selectbox('Please Select Role Below:',
#                                               (roleesoption['name']))
                        
#                         skill  = st.selectbox('Please Select Skill Below:',
#                                               (skillsoption['skill_name']))

#                         department  = st.selectbox('Please Select Department Below:',
#                                               (deptoption['dept_name']))
                    

#                     with col5:
#                         st.header("Dependants")
#                         Dependant  = st.text_input("Dependant:")   
#                         genderD  = st.selectbox('Please Select Gender Below:',
#                                               ('Male', 'Female'))    
#                         if genderD =='Male':
#                             genderDid = True           
#                         relationship  = st.selectbox('Please Select Relationship Below:',
#                                               ('Spouse', 'Parent', 'Sibling'))    
#                         if relationship =='Spouse':
#                             relationshipid = 1            
#                         phonenumber  = st.text_input("Contact Number:")                    

#                         def validate_email(email):  
#                             if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
#                                 return True  
#                             return st.write("Please make sure email is valid")
    
#                         validate_email(email)

#                 # Every form must have a submit button.
#                     submitted = st.form_submit_button("Submit")
#                     if submitted:
#                         cc = 1
#                         conn, cur = connection()
#                         conn.execute("INSERT into employees(firstname, lastname, initials,male, idnumber, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s )", (fn,ln, initials,genderid, idnumber,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                         cur.commit()

#                         conn.execute("SELECT id from employees where firstname=%s AND lastname=%s", (fn,ln))
#                         ccc = conn.fetchall()
#                         employee =  pd.DataFrame(ccc, columns=['id'])
#                         employeeid = employee['id'][0]

#                         conn.execute("INSERT into employee_contacts(physicaladdress, postaladdress, phonenumber,email, postalcode, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s )", (physicaladd,postaladd, phone,email, postalcode,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                         cur.commit()

#                         conn.execute("SELECT id from employee_contacts where physicaladdress=%s AND phonenumber=%s", (physicaladd,phone))
#                         ccc = conn.fetchall()
#                         employee_contacts =  pd.DataFrame(ccc, columns=['id'])
#                         contactid = employee_contacts['id'][0]

#                         conn.execute("INSERT into employees_employee_contacts_links(employee_id,employee_contact_id,employee_contact_order, employee_order) VALUES (%s, %s, %s, %s )", (int(employeeid),int(contactid), int(contactid),int(contactid)))
#                         cur.commit()

#                         conn.execute("INSERT into educations(qualification, level, dateobtained, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s )", (qualification,level, dateobtained,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                         cur.commit()

#                         conn.execute("SELECT id from educations where qualification=%s AND dateobtained=%s", (qualification,dateobtained))
#                         ccc = conn.fetchall()
#                         education =  pd.DataFrame(ccc, columns=['id'])
#                         educationid = education['id'][0]


#                         conn.execute("INSERT into employees_educations_links(employee_id, education_id,education_order, employee_order) VALUES (%s, %s,%s, %s)", (int(employeeid),int(educationid), int(educationid),int(educationid)))
#                         cur.commit()

#                         conn.execute("INSERT into dependants(name, relationship, phonenumber, male, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s )", (Dependant,relationship, phonenumber,genderDid,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                         cur.commit()

#                         conn.execute("SELECT id from dependants where name=%s AND phonenumber=%s", (Dependant,phonenumber))
#                         ccc = conn.fetchall()
#                         dependants =  pd.DataFrame(ccc, columns=['id'])
#                         dependantsid = dependants['id'][0]


#                         conn.execute("INSERT into employees_dependants_links(employee_id, dependant_id,dependant_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(dependantsid), int(dependantsid),int(dependantsid)))
#                         cur.commit()

#                         # conn.execute("INSERT into roleees(name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (name,description, phonenumber,genderDid,current_dateTime,current_dateTime,current_dateTime,cc,cc))

#                         conn.execute("SELECT id from roleees where name=%s ", (role,))
#                         ccc = conn.fetchall()
#                         roles =  pd.DataFrame(ccc, columns=['id'])
#                         roleeeid = roles['id'][0]


#                         conn.execute("INSERT into employees_rolees_links(employee_id, roleee_id,roleee_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(roleeeid), int(roleeeid),int(roleeeid)))
#                         cur.commit()

#                         conn.execute("SELECT id from departments where dept_name=%s ", (department,))
#                         ccc = conn.fetchall()
#                         depts =  pd.DataFrame(ccc, columns=['id'])
#                         deptid = depts['id'][0]


#                         conn.execute("INSERT into departments_employees_links(employee_id, department_id,department_order, employee_order) VALUES (%s, %s,%s, %s )", (int(employeeid), int(deptid), int(deptid),int(deptid)))
#                         cur.commit()
                  
            
#     elif choice=='Add/Edit Departments':
            
#             with st.form("my_form"):
#                 dept_name = st.text_input("Department Name:")
#                 description = st.text_input("Description:")
#             # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     try:
#                         cc = 1
#                         conn, cur = connection()
#                         conn.execute("INSERT into departments(dept_name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (dept_name,description,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                         cur.commit()
#                         conn.close()
#                     except:
#                         st.write("Something wrong with inserting into departmments tables")
#                         st.stop()
                        
#             try:
#                 conn, cur = connection()
#                 conn.execute("SELECT id, dept_name, description FROM departments")
#                 ddd = conn.fetchall()
#                 conn.close()
#             except:
#                     st.write("Something wrong with selecting from the departmments tables")
#                     st.stop()
                
#             departmentdata =  pd.DataFrame(ddd, columns=['id','dept_name','description'])
#             option = st.selectbox(
#             "Search for employee",
#             (departmentdata['dept_name']),
#             index=None,
#             placeholder="type employee name...",
#             )
#             if option:
#                 departmentdata = departmentdata[departmentdata["dept_name"]== option]
#                 st.header("Show Departments")
#                 try:
#                         conn, cur = connection()

#                         st.session_state.dfffff = departmentdata

#                         departmentdata2 = st.data_editor(st.session_state.dfffff)
#                         st.write(departmentdata2['dept_name'][0])
#                         st.session_state.dfffff = departmentdata2

#                         id = departmentdata2['id'][0]
#                         dn = departmentdata2['dept_name'][0]
#                         ddesc =departmentdata2['description'][0]

#                         conn.execute("UPDATE departments SET dept_name=%s, description=%s  where id = %s", (dn,ddesc, int(id)))
#                         cur.commit()
                      
#                         st.write('df at end:',id)

#                         if st.button("deletess"):
#                             conn.execute("DELETE FROM departments where id = %s",(int(id),))
#                             cur.commit()

#                         conn.close()
                        
#                 except:
#                         st.write(int(id))
#                         st.stop()
        

#     elif choice=='Add/Edit Roles':
#             with st.form("my_form"):
#                 role = st.text_input("Role Name:")
#                 description = st.text_input("Description:")
#             # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     cc = 1
#                     conn, cur = connection()
#                     conn.execute("INSERT into roleees(name, description, created_at, updated_at, published_at, created_by_id, updated_by_id) VALUES (%s, %s,%s, %s, %s, %s, %s )", (role,description,current_dateTime,current_dateTime,current_dateTime,cc,cc))
#                     cur.commit()
#                     conn.close()

#     elif choice=='Add Skill':
#             with st.form("my_form"):
#                 fn = st.text_input("Team Name:")
#                 ln = st.text_input("Description:")

#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("submit")


#     elif choice=='Add Project':
#             with st.form("my_form"):
#                 fn = st.text_input("Team Name:")
#                 ln = st.text_input("Description:")

#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("submit")

    
st.markdown(footer,unsafe_allow_html=True)
