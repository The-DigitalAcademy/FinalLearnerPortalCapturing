import streamlit as st
# @st.cache(suppress_st_warning=False)
st.set_page_config(layout="wide")

from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd

from psycopg2.extensions import AsIs
import hydralit_components as hc



st.title("Shaper Learner Portal App")
# menu=["View Learner","Add Team Leader","Add Cohort","Add Team","Add Team"]
# navbar = option_menu(
# menu_title="SmartStart App",
# options=menu,
# icons=["info", "info","envelope"],
# default_index=0,
# orientation="horizontal")

#     #choice=st.sidebar.selectbox("Menu",menu)
# choice=navbar


menu_data = [
    {'label':"View Learner"},
    {'label':"Add Team Leader"},
    {'label':"Add Cohort"},
    {'label':"Add Team"},
    {'label':"Add Team App"},
    {'label':"Add Soft Skill Rating"},
    {'label':"Add Tech Skill Rating"},
    {'label':"Search"},
]

menu_id = hc.nav_bar(menu_definition=menu_data)

choice = menu_id

if choice=='View Learner':
    
    COHORT = st.selectbox(
    "Select Cohort",
    ('DS', 'FS'),
    index=None,
    placeholder="Select cohort here...",
    )
    conn = psycopg2.connect(database="shaper",
    host="dpg-ckp2uroujous73d8htug-a.oregon-postgres.render.com",
    user="admin",
    password="NFLa5XvzRkU9ihAFxJ91WsX0zfy1jdcv",
    port="5432")
    cursor = conn.cursor()
    ddd = []
    if COHORT == "DS":
        cursor.execute("SELECT firstname, lastname FROM learners")
        ddd = cursor.fetchall()
        cursor.close()
    elif COHORT == "FS":
        cursor.execute("SELECT firstname, lastname FROM learners" )
        ddd = cursor.fetchall()
        cursor.close()


    option = st.selectbox(
    "Search for Learner",
    (ddd),
    index=None,
    placeholder="Select contact method...",
    )
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Contact Details", "Tech Skills", "Soft Skills","Personal Details", "Learner App",
                                                            "Duplicated Rows", "Data Types", "Dataset Summary" ])

    with tab1:
                                
                                    try:
                                        firstname = option[:-1][0]
                                        lastname = option[1:][0]
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM learners where firstname = %s and  lastname = %s", (firstname, lastname))
                                        fff = cursor.fetchall()


                                        id = fff[0][0]
                                        email = fff[0][2]
                                        name = fff[0][1]
                                        surname = fff[0][2]
                                        idnumber = fff[0][12]
                                        homelanguage = fff[0][22]
                                        male = fff[0][3]
                                        southafrican = fff[0][4]
                                        matric = fff[0][6]
                                        currentlystudying = fff[0][5]
                                        qualification = fff[0][14]
                                        nokname = fff[0][8]
                                        noknumber = fff[0][10]
                                        province = fff[0][21]
                                        city = fff[0][20]
                                        phonenumber = fff[0][9]
                                        address = fff[0][7]
                                        postalcode = fff[0][6]
                                
                                    except:
                                            st.write("Please make sure that you select a user")
                                            st.stop()

                                    st.header("Show Contacts")
                                    

                                    contacts = pd.DataFrame([[email,province,city,phonenumber,address,postalcode]], columns=['email','province','city','phonenumber','address','postalcode'])
                                    st.write(contacts)
    with tab2:
                                    st.header("Show Tech Skills Rating")
                                    try:
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM tech_skills where id = %s", (id,))
                                        ts = cursor.fetchall()
                                        ts1 = float(ts[0][1])
                                        ts2 = float(ts[0][2])
                                        ts3 = float(ts[0][3])
                                        ts4 = float(ts[0][4])
                                        ts5 = float(ts[0][5])
                                    
                                        chart_data = pd.DataFrame({"techskill": [ts1, ts2, ts3, ts4, ts5], "initials": [ts4, ts4, ts5, ts3, ts1]})
                                        st.bar_chart(chart_data)

                                    
                                    except:
                                            st.write("Please make sure that you select a user")
                                            st.stop()
    with tab3:
                                    st.header("Show Soft Skills Rating")
                                    try:
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM softskills where id = %s", (id,))
                                        ss = cursor.fetchall()
                                        ss1 = float(ss[0][1])
                                        ss2 = float(ss[0][2])
                                        ss3 = float(ss[0][3])
                                        ss4 = float(ss[0][4])
                                        ss5 = float(ss[0][5])
                                    
                                        chart_data = pd.DataFrame({"techskill": [ss1, ss2, ss3, ss4, ss5], "initials": [ss4, ss5, ss5, ss3, ss1]})
                                        st.bar_chart(chart_data)

                                    
                                    except:
                                            st.write("Please make sure that you select a user")
                                            st.stop()

    with tab4:
                                    st.header("Show Personal Details")

                                    try:
                                        firstname = option[:-1][0]
                                        lastname = option[1:][0]
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM learners where firstname = %s and  lastname = %s", (firstname, lastname))
                                        fff = cursor.fetchall()


                                        id = fff[0][0]
                                        email = fff[0][2]
                                        name = fff[0][1]
                                        surname = fff[0][2]
                                        idnumber = fff[0][12]
                                        homelanguage = fff[0][22]
                                        male = fff[0][3]
                                        southafrican = fff[0][4]
                                        matric = fff[0][6]
                                        currentlystudying = fff[0][5]
                                        qualification = fff[0][14]
                                        nokname = fff[0][8]
                                        noknumber = fff[0][10]
                                        province = fff[0][21]
                                        city = fff[0][20]
                                        phonenumber = fff[0][9]
                                        address = fff[0][7]
                                        postalcode = fff[0][6]
                                        if male == True:
                                            gender = "Male"
                                        # st.write(" Gender: " + gender)
                                        if southafrican == True:
                                            citizenship = "South African"
                                        # st.write(" Citizenship:" + citizenship)
                                        PersonalD = pd.DataFrame([[name,surname,idnumber,homelanguage,gender,citizenship]], columns=['name','surname','idnumber','homelanguage','gender','citizenship'])
                                        st.write(province)
                                    except:
                                            st.write("Please make sure that you select a user", "vsdfmnkn")
                                            st.stop()

                        
    with tab5:
                                    st.header("Learner App")
                                    
                                    try:
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM projects")
                                        la = cursor.fetchall()
                                        appname =la[0][1]
                                        description = la[0][3]
                                        problemstatement = la[0][4]
                                        solution = la[0][5]
                                        learnerapp = pd.DataFrame([[appname,description,problemstatement,solution]], columns=['App Name',"Description"'Problem Statement','Solution'])
                                        st.write(learnerapp)
                                    
                                    except:
                                            st.write("Please make sure that you select a user")
                                            st.stop()

    with tab6:
                                    st.header("Show Duplicated Rows")
                                    st.write(f"Number of Duplicate Rows")

    with tab7:
                                    st.header("Data Types")
                                    st.write("data_types")

    with tab8:
                                    st.header("Dataset Summary")
                                    st.write("efwv")
    
elif choice=='Add Team Leader':
        
        conn = psycopg2.connect(database="shaper",
        host="dpg-ckp2uroujous73d8htug-a.oregon-postgres.render.com",
        user="admin",
        password="NFLa5XvzRkU9ihAFxJ91WsX0zfy1jdcv",
        port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT name, cohortid FROM cohorts")
        cohorts = cursor.fetchall()
        cid =[]
        for c in cohorts:
            cid.append(c[0])
        from datetime import datetime
        import random
        current_dateTime = datetime.now()
        with st.form("my_form"):
            fn = st.text_input("Firstname:")
            ln = st.text_input("Lastname:")
            cohort = st.selectbox("Select Cohort", cid)
            cursor.execute("SELECT cohortid FROM cohorts where name = %s", (cohort,))
            cohortid = cursor.fetchall()
            cohortid = cohortid[0][0]
            st.write(cohortid)
           # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                tid = "team"
                cc = 1
                tlid =  random.randrange(00000000,99999999)
                cursor = conn.cursor()
                # cursor.execute("INSERT INTO() * FROM softskills where id = %s", (id,))
                cursor.execute("INSERT into teamleaders(firstname, lastname, tlid, created_at, updated_at, published_at, created_by_id, updated_by_id, teamid) VALUES (%s, %s,%s, %s, %s, %s, %s,%s, %s )", (fn,ln,str(tlid),current_dateTime,current_dateTime,current_dateTime,cc,cc,cohortid,))
                # conn.commit()
 
                # # Closing the connection
                # conn.close()
elif choice=='Add Cohort':
        with st.form("my_form"):
            fn = st.text_input("Cohort Name:")
            ln = st.text_input("Description:")
            start = st.date_input("Start Date", value=None)
            end = st.date_input("End Date", value=None)

            # Every form must have a submit button.
            submitted = st.form_submit_button("submit")


elif choice=='Add Team':
        with st.form("my_form"):
            fn = st.text_input("Team Name:")
            ln = st.text_input("Description:")

            # Every form must have a submit button.
            submitted = st.form_submit_button("submit")

elif choice=='Add Team App':
        with st.form("my_form"):
            fn = st.text_input("Team Name:")
            ln = st.text_input("Description:")

            # Every form must have a submit button.
            submitted = st.form_submit_button("submit")


elif choice=='Add Soft Skill Rating':
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
