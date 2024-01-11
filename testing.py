import streamlit as st

st.set_page_config(page_title="Employee Management Tool", page_icon=":bar_chart:", layout="wide")
import json
from datetime import datetime
import hydralit_components as hc
import pandas as pd  
import requests
from PIL import Image
from streamlit_option_menu import option_menu

image = Image.open('logo.jpeg')
st.image(image)
current_dateTime = datetime.now()


menu_data = [
        {'label':"Manage Learner"},
        {'label':"Manage Team Leader"},
        {'label':"Manage Projects"},
        {'label':"Manage Cohorts"},
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

            col1, col2, col3, col4 = st.columns(4)
            with st.form("my_formyacdaswd"):
                    with col1:
                        firstname = st.text_input("Firstname:",dd['data']['attributes']['firstname'])
                        lastname = st.text_input("Lastname:",dd['data']['attributes']['lastname'])
                    with col2:
                        homelanguage = st.text_input("Homelanguage:",dd['data']['attributes']['homelanguage'])
                        from datetime import datetime
                        dateofbirth = datetime.strptime(dd['data']['attributes']['dob'], '%Y-%m-%d').date()
                        dob = st.date_input("Date of Birth:",dateofbirth)
                    with col3:
                        southafrican = st.text_input("Nationality:",dd['data']['attributes']['southafrican'])
                        male = st.text_input("Gender:",dd['data']['attributes']['male'])
                    with col4:
                        nextofkin = st.text_input("Next of Kin:",dd['data']['attributes']['nextofkin'])
                        idnumber = st.text_input("ID Number:",dd['data']['attributes']['idnumber'])
                  
                    submitted = st.form_submit_button("Edit Personal Details")
    

                    if submitted:

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

            col1, col2, col3, col4 = st.columns(4)
            with st.form("my_formyacdga"):
                    with col1:
                        city = st.text_input("City:",dd['data']['attributes']['city'])
                        province = st.selectbox(
                                            "Province:",
                                            ("Gauteng", "North West", "Mpumalanga", "Free State","Limpopo",
                                              "Northen Cape","Western Cape", "Eastern Cape", "KwaZulu Natal"),
                                            index=None,
                                            placeholder=dd['data']['attributes']['province'],
                                            )
                    with col2:
                        physicaladdress = st.text_input("Physical Address:",dd['data']['attributes']['physicaladdress'])
                        postaladdress = st.text_input("Postal Address:",dd['data']['attributes']['postaladdress'])
                        postalcode = st.number_input("Postal Code:",dd['data']['attributes']['postalcode'])
                    with col3:
                        nextofkinnumber = st.text_input("Next of Kin Number:",dd['data']['attributes']['nextofkinnumber'])
                        phonenumber = st.text_input("Phone Number:",dd['data']['attributes']['phonenumber'])
                    with col4:
                        email = st.text_input("Email:",dd['data']['attributes']['email'])
                        githublink = st.text_input("Github Link:",dd['data']['attributes']['githublink'])
                        linkedinlink = st.text_input("Linkedin Link:",dd['data']['attributes']['linkedinlink'])

                    submitted = st.form_submit_button("Edit Contact Details")
      
                    if submitted:
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
                
                col1, col2, col3 = st.columns(3)
                with st.form("my_formyes"):
                    with col1:
                        problemsolving = st.selectbox(
                                            "Problem Solving:",
                                            ('1','2','3','4','5'),
                                            index=int(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['problemsolving'])-1,
                                            )
                        interpersonal = st.selectbox(
                                            "Interpersonal:",
                                            ('1','2','3','4','5'),
                                            index=int(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['interpersonal'])-1,
                                            )
                    with col2:
                        communication = st.selectbox(
                                            "Communication:",
                                            ('1','2','3','4','5'),
                                            index=int(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['communication'])-1,
                                            )
                        teamwork = st.selectbox(
                                            "Team Work:",
                                            ('1','2','3','4','5'),
                                            index=int(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['teamwork']) - 1,
                                            )
                    with col3:

                        leadership = st.selectbox(
                                            "Leadership:",
                                            ('1','2','3','4','5'),
                                            index=int(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['leadership']) - 1,
                                            )
                        mostimproved = st.selectbox(
                                            "Most Improved:",
                                            ('communication','teamwork','leadership','interpersonal','problemsolving'),
                                            placeholder=str(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['mostimproved']),
                                            )
                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:
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
                                    "mostimproved" : mostimproved
                                    }
                        }))
        except:
            with st.form("my_form"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        problemsolving = st.number_input("Problem Solving:")
                        interpersonal = st.number_input("Interpersonal:")
                    with col2:
                        communication = st.number_input("Communication:")
                        teamwork = st.number_input("Team Work:")
                    with col3:
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

                col1, col2, col3 = st.columns(3)
                with st.form("my_formx"):
                    with col1:
                        skill1 = st.number_input("Skill1:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill1'])
                        skill2 = st.number_input("Skill2:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill2'])
                    with col2:
                        skill3 = st.number_input("Skill3:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill3'])
                        skill4 = st.number_input("Skill4:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill4'])
                    with col3:
                        skill5 = st.number_input("Skill5:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill5'])
                        mostimproved = st.text_input("Most Improved:",dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved'])

                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:
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
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        skill1 = st.number_input("Skill1:")
                        skill2 = st.number_input("Skill2:")
                    with col2:
                        skill3 = st.number_input("Skill3:")
                        skill4 = st.number_input("Skill4:")
                    with col3:
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
            
                with st.form("my_formss"):
                    review = st.text_input("Shaper Review:",dd['data']['attributes']['shaperreviews']['data'][0]['attributes']['review'])
                    
                    submitted = st.form_submit_button("Edit Review")

                if submitted:
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
                        
if choice=='Manage Team Leader':
    try:
        
        URLLEADER = "http://localhost:1337/api/teamleaders"
        d = requests.get(URLLEADER)
        dd = d.json()
        z = 0
        sn=[]
        tid=[]
        sid=[]
        sln=[]

        for i in range(len(dd['data'])):
            sn.append(dd['data'][z]['attributes']['firstname'])
            sln.append(dd['data'][z]['attributes']['lastname'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sln,sid),columns=['firstname','lastname','id'])
        deptss['fullname'] = deptss['firstname'] + " " + deptss['lastname']

        LEADER = st.selectbox(
                "Select a Team Leader",
                (deptss['fullname']),
                index=None,
                placeholder="Select learner here...",
                )
        Learn = deptss[deptss['fullname'] == LEADER]
        LEADERID = Learn['id'].values
    except:
         st.write("Please Select a Team Leader Above")


    tab1, tab2 = st.tabs(["Manage Team Leader", "Add Team Leader" ])

    with tab1:
        try:
            url = "http://localhost:1337/api/teamleaders/" + str(LEADERID[0]) + "?populate=teams"
            d = requests.get(url)
            dd = d.json()
            
            st.session_state.dff = dd['data']['attributes']
            x = pd.DataFrame(st.session_state.dff, index=[0])
            edited_dff = st.data_editor(x) 
            st.session_state.dff = edited_dff
        
            firstname = edited_dff['firstname'][0]
            lastname = edited_dff['lastname'][0]
            teams = edited_dff['teams'][0]

            st.write("Current Team is: " + dd['data']['attributes']['teams']['data'][0]['attributes']['name'])

            if st.button('Edit Team Leader Details'):

                requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "data": 
                            {
                                "firstname": firstname,
                                "lastname": lastname,
                                "teams": teams,
                            }
                    }))
            if st.button("Delete This Team Leader"):
                requests.delete(url)
        except:
            st.write("Please select a Team Leader")
    with tab2:
         with st.form("my_form5"):
                    firstname = st.text_input("Firstname:")
                    lastname = st.text_input("Lastname:")

                    submitted = st.form_submit_button("Add Team Leader")
                    if submitted:
                        requests.post(
                        "http://localhost:1337/api/teamleaders/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "firstname": firstname,
                                    "lastname": lastname,
                                }
                            }
                        ),
                    )

if choice=='Manage Projects':
    try:
        URLPROJECT = "http://localhost:1337/api/projects"
        d = requests.get(URLPROJECT)
        dd = d.json()
        z = 0
        projectname_ = []
        tid=[]
        sid=[]
        problemstatement_ = []
        solution_ = []
        screenshot1explanation_ = []
        screenshot2explanation_ = []
        screenshot3explanation_ = []
        screenshot4explanation_ = []
        screenshot5explanation_ = []
        screenshot6explanation_ = []
        screenshot7explanation_ = []

        screenshot1_image_ = []
        screenshot2_image_ = []
        screenshot3_image_ = []
        screenshot4_image_ = []
        screenshot5_image_ = []
        screenshot6_image_ = []
        screenshot7_image_ = []
        imageurl_ = []

        for i in range(len(dd['data'])):
            projectname_.append(dd['data'][z]['attributes']['projectname'])
            problemstatement_.append(dd['data'][z]['attributes']['problemstatement'])
            solution_.append(dd['data'][z]['attributes']['solution'])
 
            screenshot1explanation_.append(dd['data'][z]['attributes']['screenshot1explanation'])
            screenshot2explanation_.append(dd['data'][z]['attributes']['screenshot2explanation'])
            screenshot3explanation_.append(dd['data'][z]['attributes']['screenshot3explanation'])
            screenshot4explanation_.append(dd['data'][z]['attributes']['screenshot4explanation'])
            screenshot5explanation_.append(dd['data'][z]['attributes']['screenshot5explanation'])
            screenshot6explanation_.append(dd['data'][z]['attributes']['screenshot6explanation'])
            screenshot7explanation_.append(dd['data'][z]['attributes']['screenshot7explanation'])

            screenshot1_image_.append(dd['data'][z]['attributes']['screenshot1_image'])
            screenshot2_image_.append(dd['data'][z]['attributes']['screenshot2_image'])
            screenshot3_image_.append(dd['data'][z]['attributes']['screenshot3_image'])
            screenshot4_image_.append(dd['data'][z]['attributes']['screenshot4_image'])
            screenshot5_image_.append(dd['data'][z]['attributes']['screenshot5_image'])
            screenshot6_image_.append(dd['data'][z]['attributes']['screenshot6_image'])
            screenshot7_image_.append(dd['data'][z]['attributes']['screenshot7_image'])
            
            sid.append(dd['data'][z]['id'])
            
            imageurl_.append(dd['data'][z]['attributes']['imageurl'])
            z = z + 1

        deptss = pd.DataFrame(data=zip(projectname_,problemstatement_,solution_,screenshot1explanation_,
                                       screenshot2explanation_,screenshot3explanation_,screenshot4explanation_,
                                       screenshot5explanation_,screenshot6explanation_,screenshot7explanation_,
                                       screenshot1_image_,screenshot2_image_,screenshot3_image_,screenshot4_image_,
                                       screenshot5_image_,screenshot6_image_,screenshot7_image_,imageurl_,sid),
                                       columns=['projectname','problemstatement','solution','screenshot1explanation',
                                       'screenshot2explanation','screenshot3explanation','screenshot4explanation',
                                       'screenshot5explanation','screenshot6explanation','screenshot7explanation',
                                       'screenshot1_image','screenshot2_image','screenshot3_image','screenshot4_image',
                                       'screenshot5_image','screenshot6_image','screenshot7_image','imageurl','id'])
        
        PROJECT = st.selectbox(
                "Select a projects",
                (deptss['projectname']),
                index=None,
                placeholder="Select project here...",
                )
        Learn = deptss[deptss['projectname'] == PROJECT]
        PROJECTID = Learn['id'].values
    except:
         st.write("Please Select a projects Above")

    tab1, tab2 = st.tabs(["Manage Project", "Add Project" ])
    with tab1:
        try:
            url = "http://localhost:1337/api/projects/" + str(PROJECTID[0]) + "?populate=teams"
            d = requests.get(url)
            dd = d.json()
            
            st.session_state.dff = dd['data']['attributes']
            x = pd.DataFrame(st.session_state.dff, index=[0])
            edited_dff = st.data_editor(x) 
            st.session_state.dff = edited_dff
        
            projectname = edited_dff['projectname'][0]
            problemstatement = edited_dff['problemstatement'][0]
            solution = edited_dff['solution'][0]

            screenshot1explanation = edited_dff['screenshot1explanation'][0]
            screenshot2explanation = edited_dff['screenshot2explanation'][0]
            screenshot3explanation = edited_dff['screenshot3explanation'][0]
            screenshot4explanation = edited_dff['screenshot4explanation'][0]
            screenshot5explanation = edited_dff['screenshot5explanation'][0]
            screenshot6explanation = edited_dff['screenshot6explanation'][0]
            screenshot7explanation = edited_dff['screenshot7explanation'][0]

            screenshot1_image = edited_dff['screenshot1_image'][0]
            screenshot2_image = edited_dff['screenshot2_image'][0]
            screenshot3_image = edited_dff['screenshot3_image'][0]
            screenshot4_image = edited_dff['screenshot4_image'][0]
            screenshot5_image = edited_dff['screenshot5_image'][0]
            screenshot6_image = edited_dff['screenshot6_image'][0]
            screenshot7_image = edited_dff['screenshot7_image'][0]
            teams = edited_dff['teams'][0]

            st.write("Current Team is: " + dd['data']['attributes']['teams']['data'][0]['attributes']['name'])

            if st.button('Edit Project Details'):

                requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "data": 
                            {
                                "projectname": projectname,
                                "problemstatement": problemstatement,
                                "solution" : solution,
                                'screenshot1explanation' : screenshot1explanation,
                                'screenshot2explanation' : screenshot2explanation,
                                'screenshot3explanation' : screenshot3explanation,
                                'screenshot4explanation' : screenshot4explanation,
                                'screenshot5explanation' : screenshot5explanation,
                                'screenshot6explanation' : screenshot6explanation,
                                'screenshot7explanation' : screenshot7explanation,
                                'screenshot1_image' : screenshot1_image,
                                'screenshot2_image' : screenshot1_image,
                                'screenshot3_image' : screenshot1_image,
                                'screenshot4_image' : screenshot1_image,
                                'screenshot5_image' : screenshot1_image,
                                'screenshot6_image' : screenshot1_image,
                                'screenshot7_image' : screenshot1_image
                            }
                    }))
            if st.button("Delete This Project"):
                requests.delete(url)
        except:
            st.write("Please select a project")
    with tab2:
         with st.form("my_form6"):
                    projectname = st.text_input("Project Name:")
                    problemstatement = st.text_input("Problem Statement:")

                    submitted = st.form_submit_button("Add a Project")
                    if submitted:
                        requests.post(
                        "http://localhost:1337/api/projects/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "projectname": projectname,
                                    "problemstatement": problemstatement,
                                }
                            }
                        ),
                    )    

if choice=='Manage Cohorts':
    try:
        URLCOHORT = "http://localhost:1337/api/cohorts"
        d = requests.get(URLCOHORT)
        dd = d.json()
        z = 0
        name_=[]
        tid=[]
        sid_=[]
        teams_ = []
        description_=[]
        skill1_ = []
        skill2_= []
        skill3_ = []
        skill4_ = []
        skill5_ = []
        skill6_ = []
        skill7_ = []      
        skill1_icon_ = []
        skill2_icon_= []
        skill3_icon_ = []
        skill4_icon_ = []
        skill5_icon_ = []
        skill6_icon_ = []
        skill7_icon_ = []       

        for i in range(len(dd['data'])):
            name_.append(dd['data'][z]['attributes']['name'])
            description_.append(dd['data'][z]['attributes']['description'])
            sid_.append(dd['data'][z]['id'])
            
            skill1_.append(dd['data'][z]['attributes']['skill1'])
            skill2_.append(dd['data'][z]['attributes']['skill2'])
            skill3_.append(dd['data'][z]['attributes']['skill3'])
            skill4_.append(dd['data'][z]['attributes']['skill4'])
            skill5_.append(dd['data'][z]['attributes']['skill5'])
            skill6_.append(dd['data'][z]['attributes']['skill6'])
            skill7_.append(dd['data'][z]['attributes']['skill7'])
            skill1_icon_.append(dd['data'][z]['attributes']['skill1_icon'])
            skill2_icon_.append(dd['data'][z]['attributes']['skill2_icon'])
            skill3_icon_.append(dd['data'][z]['attributes']['skill3_icon'])
            skill4_icon_.append(dd['data'][z]['attributes']['skill4_icon'])
            skill5_icon_.append(dd['data'][z]['attributes']['skill5_icon'])
            skill6_icon_.append(dd['data'][z]['attributes']['skill6_icon'])
            skill7_icon_.append(dd['data'][z]['attributes']['skill7_icon'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(name_,description_,skill1_,skill2_,skill3_,skill4_,skill5_,skill6_,skill7_,
                                       skill1_icon_,skill2_icon_,skill3_icon_,skill4_icon_,
                                       skill5_icon_,skill6_icon_,skill7_icon_,sid_),columns=['name','description','skill1','skill2',
                                       'skill3','skill4','skill5','skill6','skill7',
                                       'skill1_icon','skill2_icon','skill3_icon','skill4_icon',
                                       'skill5_icon','skill6_icon','skill7_icon','id'])
        
        COHORT = st.selectbox(
                "Select a Cohort",
                (deptss),
                index=None,
                placeholder="Select cohort here...",
                )
        Learn = deptss[deptss['name'] == COHORT]
        COHORTID = Learn['id'].values
    except:
         st.write("Please Select a Cohort")

    tab1, tab2 = st.tabs(["Manage Cohort", "Add New Cohort" ])
    with tab1:
        try:
            url = "http://localhost:1337/api/cohorts/" + str(COHORTID[0]) + "?populate=teams"
            d = requests.get(url)
            dd = d.json()

            col1, col2, col3 = st.columns(3)
            with st.form("my_formx"):
                    with col1:
                        name = st.text_input("name:",dd['data']['attributes']['name'])
                        description = st.text_input("description:",dd['data']['attributes']['description'])
                        teams = st.text_input("teams:",dd['data']['attributes']['teams'])

                    with col2:
                        skill1 = st.text_input("Skill1:",dd['data']['attributes']['skill1'])
                        skill2 = st.text_input("Skill2:",dd['data']['attributes']['skill2'])
                        skill3 = st.text_input("skill3:",dd['data']['attributes']['skill3'])
                        skill4 = st.text_input("Skill2:",dd['data']['attributes']['skill4'])
                        skill5 = st.text_input("skill3:",dd['data']['attributes']['skill5'])
                    with col3:
                        skill1_icon = st.text_input("skill1_icon:",dd['data']['attributes']['skill1_icon'])
                        skill2_icon = st.text_input("skill2_icon:",dd['data']['attributes']['skill2_icon'])
                        skill3_icon = st.text_input("skill3_icon:",dd['data']['attributes']['skill3_icon'])
                        skill4_icon = st.text_input("skill4_icon:",dd['data']['attributes']['skill4_icon'])
                        skill5_icon = st.text_input("skill5_icon:",dd['data']['attributes']['skill5_icon'])

                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:
                        st.write(teams)
                        requests.put(
                        url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": 
                                    {
                                        "name": name,
                                        "description": description,
                                        'skill1' : skill1,
                                        'skill2' : skill2,
                                        'skill3' : skill3,
                                        'skill4' : skill4,
                                        'skill5' : skill5,
                                  
                                        'skill1_icon' : skill1_icon,
                                        'skill2_icon' : skill2_icon,
                                        'skill3_icon' : skill3_icon,
                                        'skill4_icon' : skill4_icon,
                                        'skill5_icon' : skill5_icon,
                                    }
                            }))
                    if st.button("Delete This Cohort"):
                        requests.delete(url)
        except:
            st.write("Please select a cohort")
    with tab2:
         with st.form("my_form7"):
                    name = st.text_input("Cohort Name:")
                    description = st.text_input("Description:")

                    submitted = st.form_submit_button("Add Cohort")
                    if submitted:
                        requests.post(
                        "http://localhost:1337/api/cohorts/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "name": name,
                                    "description": description,
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
st.markdown(footer,unsafe_allow_html=True)
