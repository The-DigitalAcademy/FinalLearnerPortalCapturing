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
        {'label':"Manage Team"},
        {'label':"Manage Team Leader"},
        {'label':"Manage Projects"},
        {'label':"Manage Cohorts"},
        {'label':"Manage Personal Questions"},
        {'label':"Manage Contact Questions"},
        {'label':"Manage Education Questions"},
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
                    (['Data Science','PWD','Full Stack']),
                    index=None,
                    placeholder="Select cohort here...",
                    )
        URLCOHORT = "https://truthful-health-29656117e6.strapiapp.com/api/applicants?filters[$or][0][Program][$eq]="+str(COHORT)
        d = requests.get(URLCOHORT)
        dd = d.json()
        z = 0
        for i in range(len(dd['data'])):
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


    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Personal Details", "Contact Details", "Soft Skills Ratings","Technical Skills Ratings","Shaper Learner Review", "Project Responsibilities", 'Assign Team', 'Assign Project', 'Assign Skill Descriptions'])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/applicants/" + str(LEARNERID[0])
            d = requests.get(url)
            dd = d.json()

            col1, col2, col3, col4, col5 = st.columns(5)
            with st.form("my_formyacdaswd"):
                    with col1:
                        st.image(dd['data']['attributes']['imageurl'], width=120)
                    with col2:
                        firstname = st.text_input("Firstname:",dd['data']['attributes']['firstname'])
                        lastname = st.text_input("Lastname:",dd['data']['attributes']['lastname'])
                    with col3:
                        homelanguage = st.text_input("Homelanguage:",dd['data']['attributes']['homelanguage'])
                        from datetime import datetime
                        dateofbirth = datetime.strptime(dd['data']['attributes']['dob'], '%Y-%m-%d').date()
                        dob = st.date_input("Date of Birth:",dateofbirth)
                    with col4:
                        southafrican = st.text_input("Nationality:",dd['data']['attributes']['southafrican'])
                        male = st.text_input("Gender:",dd['data']['attributes']['male'])
                    with col5:
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
                                        "dob": str(dob),
                                        "male": str(male),
                                        "southafrican": str(southafrican),
                                        "homelanguage": homelanguage,
                                        "nextofkin": nextofkin,
                                        "idnumber": idnumber,
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
        except:
            st.write("Please select a learner")

    with tab2:
        try:
            d = requests.get(url)
            dd = d.json()

            col1, col2, col3, col4 = st.columns(4)
            with st.form("my_formyacdga"):
                    if dd['data']['attributes']['province'] == 'Gauteng':
                        a = 1
                    elif dd['data']['attributes']['province'] == 'North West':
                        a = 2
                    elif dd['data']['attributes']['province'] == 'Mpumalanga':
                        a = 3
                    elif dd['data']['attributes']['province'] == 'Free State':
                        a = 4
                    elif dd['data']['attributes']['province'] == 'Limpopo':
                        a = 5
                    elif dd['data']['attributes']['province'] == 'Northen Cape':
                        a = 6
                    elif dd['data']['attributes']['province'] == 'Western Cape':
                        a = 7
                    elif dd['data']['attributes']['province'] == 'Eastern Cape':
                        a = 8
                    elif dd['data']['attributes']['province'] == 'KwaZulu Natal':
                        a = 9
                    else:
                         a = 1
                   
                    with col1:
                        
                        city = st.text_input("City:",dd['data']['attributes']['city'])
                        province = st.selectbox(
                                            "Province:",
                                            ("Gauteng", "North West", "Mpumalanga", "Free State","Limpopo",
                                              "Northen Cape","Western Cape", "Eastern Cape", "KwaZulu Natal"),
                                             index= a - 1,
                                            )
                        imageurl = st.text_input("Profile Picture URL:",dd['data']['attributes']['imageurl'])

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
                                        "phonenumber": phonenumber,
                                        "postalcode": str(postalcode),
                                        "githublink": githublink,
                                        "linkedinlink": linkedinlink,
                                        "nextofkinnumber": nextofkinnumber,
                                        "imageurl": imageurl,
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
        except:
            st.write("")
    try:
        url2 = "https://truthful-health-29656117e6.strapiapp.com/api/applicants/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews,responsibilities"
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
                    moi = str(dd['data']['attributes']['softskillratings']['data'][0]['attributes']['mostimproved'])
                    if moi == 'communication':
                        a = 1
                    elif moi == 'teamwork':
                        a = 2
                    elif moi == 'leadership':
                        a = 3
                    elif moi == 'interpersonal':
                        a = 4
                    elif moi == 'problemsolving':
                        a = 5
                    else:
                         a = 1
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
                                            ('Communication','Team Work','Leadership','Interpersonal','Problem Solving'),
                                            index= a - 1 )
                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:
                        
                        ff = "https://truthful-health-29656117e6.strapiapp.com/api/softskillratings/"+str(id)
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
                                    "mostimproved" : str(mostimproved)
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
        except:
            with st.form("my_form"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        problemsolving = st.selectbox(
                                            "Problem Solving:",
                                            ('1','2','3','4','5'),
                                            )
                        interpersonal = st.selectbox(
                                            "Interpersonal:",
                                            ('1','2','3','4','5'),
                                            )
                    with col2:
                        communication = st.selectbox(
                                            "Communication:",
                                            ('1','2','3','4','5'),
                                            )
                        teamwork = st.selectbox(
                                            "Teamwork:",
                                            ('1','2','3','4','5'),
                                            )
                    with col3:
                        leadership = st.selectbox(
                                            "Leadership:",
                                            ('1','2','3','4','5'),
                                            )
                        mostimproved = st.selectbox(
                                            "Most Improved:",
                                            ('Communication','Team Work','Leadership','Interpersonal','Problem Solving'),
                                            )

                        submitted = st.form_submit_button("Add Ratings")
                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/softskillratings/",
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
                                    "mostimproved" : mostimproved,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")

    with tab4:     
        try:
            if (len(dd['data']['attributes']['techskillratings']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['techskillratings']['data'][0]['id']
                
                col1, col2, col3 = st.columns(3)
                with st.form("my_formx"):

                    if dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved'] == 'Python':
                        a = 1
                    elif dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved']  == 'ReactJS':
                        a = 2
                    elif dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved']  == 'HTML':
                        a = 3
                    elif dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved']  == 'Javascript':
                        a = 4
                    elif dd['data']['attributes']['techskillratings']['data'][0]['attributes']['mostimproved']  == 'CSS':
                        a = 5
                    else:
                        a = 1
                        
                    with col1:
                        skill1 = st.slider("Skill1:",0,5,int(dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill1']))
                        skill2 = st.slider("Skill2:",0,5,int(dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill2']))
                        skill3 = st.slider("Skill3:",0,5,int(dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill3']))
                    with col3:
                        skill4 = st.slider("Skill4:",0,5,int(dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill4']))
                        skill5 = st.slider("Skill5:",0,5,int(dd['data']['attributes']['techskillratings']['data'][0]['attributes']['skill5']))
                        mostimproved = st.selectbox(
                                            "Most Improvsed:",
                                            ('Python','ReactJS','HTML','Javascript','CSS'),
                                            index= a - 1)
                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:

                        ff = "https://truthful-health-29656117e6.strapiapp.com/api/technicalskills/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data":          
                                    {
                                    "applicants": str(LEARNERID[0]),
                                    "skill1": str(skill1),
                                    "skill2": str(skill2),
                                    "skill3": str(skill3),
                                    "skill4": str(skill4),
                                    "skill5": str(skill5),
                                    "mostimproved": str(mostimproved),

                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
        except:
            with st.form("my_form2"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        skill1 = st.slider("Skill1:",0,5,0)
                        skill2 = st.slider("Skill2:",0,5,0)
                    with col2:
                        skill3 = st.slider("Skill3:",0,5,0)
                        skill4 = st.slider("Skill4:",0,5,0)
                    with col3:
                        skill5 = st.slider("Skill5:",0,5,0)
                        mostimproved = st.selectbox(
                                            "Most Improvsed:",
                                            ('Python','ReactJS','HTML','Javascript','CSS'),
                                            )

                    submitted = st.form_submit_button("Add Ratings")
                    if submitted:

                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/technicalskills/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": str(LEARNERID[0]),
                                    "skill1": str(skill1),
                                    "skill2": str(skill2),
                                    "skill3": str(skill3),
                                    "skill4": str(skill4),
                                    "skill5": str(skill5),
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")
    with tab5:     
        try:
            if (len(dd['data']['attributes']['shaperreviews']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['shaperreviews']['data'][0]['id']
            
                with st.form("my_formsxdsxcs"):
                    review = st.text_input("Shaper Review:",dd['data']['attributes']['shaperreviews']['data'][0]['attributes']['review'])
                    
                    submitted = st.form_submit_button("Edit Review")

                if submitted:
                        ff = "https://truthful-health-29656117e6.strapiapp.com/api/shaperreviews/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "applicants": str(LEARNERID[0]),
                                    "review": review,
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
        except:
            with st.form("my_formxd3"):
                    review = st.text_input("Review:")

                    submitted = st.form_submit_button("Add Review")
                    if submitted:

                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/shaperreviews/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": str(LEARNERID[0]),
                                    "review": review,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")
    with tab6:     
        try:
            if (len(dd['data']['attributes']['responsibilities']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['responsibilities']['data'][0]['id']
                with st.form("my_formsxxsdsqdxcds"):
                    responsibility = st.text_input("Responsibilities:",dd['data']['attributes']['responsibilities']['data'][0]['attributes']['responsibility'])
                    
                    submitted = st.form_submit_button("Edit Responsibility")

                if submitted:
                        ff = "https://truthful-health-29656117e6.strapiapp.com/api/responsibilities/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "applicants": str(LEARNERID[0]),
                                    "responsibility": responsibility,
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
        except:
            with st.form("my_form3waxdsa"):
                    responsibility = st.text_input("Responsibility:")

                    submitted = st.form_submit_button("Add Responsibility")
                    if submitted:
                        responsibility
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/responsibilities/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": str(LEARNERID[0]),
                                    "responsibility": responsibility,
                                }
                            }
                        ),
                    )    
                        st.success('This is a success message!', icon="✅")  

    with tab7:
        try:
            URLTEAM = "https://truthful-health-29656117e6.strapiapp.com/api/teams"
            d = requests.get(URLTEAM)
            dd = d.json()
            z = 0
            sn=[]
            tid=[]
            sid=[]
            sln=[]

            for i in range(len(dd['data'])):
                sn.append(dd['data'][z]['attributes']['name'])
                sid.append(dd['data'][z]['id'])
                z = z + 1
                
            deptss = pd.DataFrame(data=zip(sn,sid),columns=['name','id'])

            TEAM = st.selectbox(
                    "Select a Team",
                    (deptss['name']),
                    index=None,
                    placeholder="Select team here...",
                    )
            team = deptss[deptss['name'] == TEAM]
            TEAMID = team['id'].values
        except:
            st.write("Please Select a Team Above")

        try:
                url = "https://truthful-health-29656117e6.strapiapp.com/api/applicants/" + str(LEARNERID[0]) + "?populate=teams"
                d = requests.get(url)
                dd = d.json()
                with st.form("my_formsxdsxdeddfecvdvcddfvsscxxs"):
                        try:
                            "Current Team is: " + dd['data']['attributes']['teams']['data'][0]['attributes']['name']
                        except:
                             "No Team Currently assigned"
                        submitted = st.form_submit_button("Assign team to selected")

                        if submitted:
                            requests.put(
                            url,
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(
                                {
                                    "data": 
                                        {
                                            "teams": int(TEAMID),
                                        }
                                }))
                            st.success('This is a success message!', icon="✅")
            
        except:
                 st.write("Please select a learner")      
    with tab8:
        try:
            URLPROJECT = "https://truthful-health-29656117e6.strapiapp.com/api/projects"
            d = requests.get(URLPROJECT)
            dd = d.json()
            z = 0
            sn=[]
            tid=[]
            sid=[]
            sln=[]

            for i in range(len(dd['data'])):
                sn.append(dd['data'][z]['attributes']['projectname'])
                sid.append(dd['data'][z]['id'])
                z = z + 1
                
            deptss = pd.DataFrame(data=zip(sn,sid),columns=['projectname','id'])

            PROJECT = st.selectbox(
                    "Select a Project",
                    (deptss['projectname']),
                    index=None,
                    placeholder="Select project here...",
                    )
            project = deptss[deptss['projectname'] == PROJECT]
            PROJECTID = project['id'].values
        except:
            st.write("Please Select a project above")
       
        try:

                url = "https://truthful-health-29656117e6.strapiapp.com/api/applicants/" + str(LEARNERID[0]) + "?populate=projects"
                d = requests.get(url)
                dd = d.json()

                with st.form("my_formsxdsxddwceddsdsdsfecvdvcddfvsscxxs"):
                        try:
                            "Current Project is: " + dd['data']['attributes']['projects']['data'][0]['attributes']['projectname']
                        except:
                             "No Project Currently Assigned"

                        submitted = st.form_submit_button("Assign project to selected")
                        

                        if submitted:
                            requests.put(
                            url,
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(
                                {
                                    "data": 
                                        {
                                            "projects": int(PROJECTID),
                                        }
                                }))
                            st.success('This is a success message!', icon="✅")
            
        except:
                 st.write("Please select a learner")  
    with tab9:
       
        try:

                url = "https://truthful-health-29656117e6.strapiapp.com/api/applicants/" + str(LEARNERID[0]) + "?populate=communicationratingdescriptions,interpersonalratingdescriptions,leadershipratingdescriptions,problemsolvingratingdescriptions,teamworkratingdescriptions,techskillsratingdescriptions,softskilldescriptions"
                d = requests.get(url)
                dd = d.json()

                with st.form("my_formsxdsxddwceddcdsdsdsfecvdvcddfvsscxxs"):
                        submitted = st.form_submit_button("Assign project to selected")
                        
                        if submitted:
                            requests.put(
                            url,
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(
                                {
                                    "data": 
                                        {
                                            "communicationratingdescriptions": 1,
                                            'interpersonalratingdescriptions' : 1,
                                            'leadershipratingdescriptions': 1,
                                            'problemsolvingratingdescriptions': 1,
                                            'teamworkratingdescriptions': 1,
                                            'techskillsratingdescriptions': 1,
                                            'softskilldescriptions': 1

                                        }
                                }))
                            st.success('This is a success message!', icon="✅")
            
        except:
                 st.write("Please select a learner")             
if choice=='Manage Team Leader':
    try:
        URLLEADER = "https://truthful-health-29656117e6.strapiapp.com/api/teamleaders"
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
                placeholder="Select team leader here...",
                )
        Learn = deptss[deptss['fullname'] == LEADER]
        LEADERID = Learn['id'].values
    except:
         st.write("Please Select a Team Leader Above")


    tab1, tab2 = st.tabs(["Manage Team Leader", "Add Team Leader" ])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/teamleaders/" + str(LEADERID[0])
            d = requests.get(url)
            dd = d.json()
            
            with st.form("my_formsxdsxdccxxs"):
                    firstname = st.text_input("Firstname:",dd['data']['attributes']['firstname'])
                    lastname = st.text_input("Lastname:",dd['data']['attributes']['lastname'])

                    submitted = st.form_submit_button("Edit Team Leader Details")

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
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
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
                        "https://truthful-health-29656117e6.strapiapp.com/api/teamleaders/",
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
                        st.success('This is a success message!', icon="✅")
               
if choice=='Manage Team':
    try:
        URLLEADER = "https://truthful-health-29656117e6.strapiapp.com/api/teams"
        d = requests.get(URLLEADER)
        dd = d.json()
        z = 0
        sn=[]
        tid=[]
        sid=[]
        sln=[]

        for i in range(len(dd['data'])):
            sn.append(dd['data'][z]['attributes']['name'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sid),columns=['name','id'])

        TEAM = st.selectbox(
                "Select a Team",
                (deptss['name']),
                index=None,
                placeholder="Select team here...",
                )
        team = deptss[deptss['name'] == TEAM]
        TEAMID = team['id'].values
    except:
         st.write("Please Select a Team Leader Above")


    tab1, tab2 = st.tabs(["Manage Team", "Add Team" ])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/teams/" + str(TEAMID[0])
            d = requests.get(url)
            dd = d.json()

            with st.form("my_formsxdsxdeddfecsscxxs"):
                    name = st.text_input("Team Name:",dd['data']['attributes']['name'])

                    submitted = st.form_submit_button("Edit Team")

                    if submitted:
                        requests.put(
                        url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": 
                                    {
                                        "name": name,
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
            if st.button("Delete This Team"):
                requests.delete(url)
        except:
            st.write("Please select a Team")
    with tab2:
         with st.form("my_form5"):
                    name = st.text_input("Team Name:")
                    submitted = st.form_submit_button("Add Team")

                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/teams/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "name": name,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")

if choice=='Manage Projects':
    try:
        URLPROJECT = "https://truthful-health-29656117e6.strapiapp.com/api/projects"
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
                "Select a project",
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
            url = "https://truthful-health-29656117e6.strapiapp.com/api/projects/" + str(PROJECTID[0]) + "?populate=teams"
            d = requests.get(url)
            dd = d.json()

            col1, col2, col3, col4, col5 = st.columns(5)
            col6, col7, col8, col9, col10 = st.columns(5)
            with st.form("my_formydsacdaddsdcdccswd"):
                    with st.container():
                        with col1:
                            projectname = st.text_input("Project Name:",dd['data']['attributes']['projectname'])
                            problemstatement = st.text_area("Problem Statement:",dd['data']['attributes']['problemstatement'])
                        with col2:
                            solution = st.text_area("Solution:",dd['data']['attributes']['solution'])
                            screenshot1explanation = st.text_area("Screenshot1 Explanation:",dd['data']['attributes']['screenshot1explanation'])
                        with col3:
                            screenshot2explanation = st.text_area("Screenshot2 Explanation:",dd['data']['attributes']['screenshot2explanation'])
                            screenshot3explanation = st.text_area("Screenshot3 Explanation:",dd['data']['attributes']['screenshot3explanation'])
                        with col4:
                            screenshot4explanation = st.text_area("Screenshot4 Explanation:",dd['data']['attributes']['screenshot4explanation'])
                            screenshot5explanation = st.text_area("Screenshot5 Explanation",dd['data']['attributes']['screenshot5explanation'])
                        with col5:
                            screenshot6explanation = st.text_area("Screenshot6 Explanation:",dd['data']['attributes']['screenshot6explanation'])
                            screenshot7explanation = st.text_area("Screenshot7 Explanation",dd['data']['attributes']['screenshot7explanation'])
                    with st.container():
                        with col7:
                            screenshot1_image = st.text_area("Screenshot Image1:",dd['data']['attributes']['screenshot1_image'])
                            screenshot2_image = st.text_area("Screenshot Image2:",dd['data']['attributes']['screenshot2_image'])
                        with col8:
                            screenshot3_image = st.text_area("Screenshot Image3:",dd['data']['attributes']['screenshot3_image'])
                            screenshot4_image = st.text_area("Screenshot Image4:",dd['data']['attributes']['screenshot4_image'])
                        with col9:
                            screenshot5_image = st.text_area("Screenshot Image5:",dd['data']['attributes']['screenshot5_image'])
                            screenshot6_image = st.text_area("Screenshot Image6",dd['data']['attributes']['screenshot6_image'])
                        with col10:
                            screenshot7_image = st.text_area("Screenshot Image7:",dd['data']['attributes']['screenshot7_image'])
                    
                    submitted = st.form_submit_button("Edit Project Details")

                    if submitted:
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
                                        'screenshot2_image' : screenshot2_image,
                                        'screenshot3_image' : screenshot3_image,
                                        'screenshot4_image' : screenshot4_image,
                                        'screenshot5_image' : screenshot5_image,
                                        'screenshot6_image' : screenshot6_image,
                                        'screenshot7_image' : screenshot7_image
                                    }
                            }))
                        st.success('Successfully edited your projects!', icon="✅")
            if st.button("Delete This Project"):
                requests.delete(url)
                st.success('Deleted Successfully!', icon="✅") 
        except:
            st.write("Please select a project")
    with tab2:
         with st.form("my_form6"):
                    projectname = st.text_input("Project Name:")
                    problemstatement = st.text_input("Problem Statement:")

                    submitted = st.form_submit_button("Add a Project")
                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/projects/",
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
                        st.success('This is a success message!', icon="✅") 

if choice=='Manage Cohorts':
    try:
        URLCOHORT = "https://truthful-health-29656117e6.strapiapp.com/api/cohorts"
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
            
            url = "https://truthful-health-29656117e6.strapiapp.com/api/cohorts/" + str(COHORTID[0]) + "?populate=teams"
            d = requests.get(url)
            dd = d.json()
            try:
                 a = dd['data'][0]['attributes']['skill1']
            except:
                 a = "Python"
            try:
                 b = dd['data'][0]['attributes']['skill2']
            except:
                 b = "Python"
            try:
                 c = dd['data'][0]['attributes']['skill3']
            except:
                 c = "Python"
            try:
                 d = dd['data'][0]['attributes']['skill4']
            except:
                 d = "Python"
            try:
                 e = dd['data'][0]['attributes']['skill5']
            except:
                 e = "Python"

            col1, col12 = st.columns(2)
            col2, col3, col4, col5, col6 = st.columns(5)
            col7, col8, col9, col10, col11 = st.columns(5)
            with st.form("my_formx"):
                skillz = ['ReactJS','Python','Machine Learning','Databases','SQL','CSS','Django','Javascript','HTML','Angular','Bootstrap',"Visualisation"]
                
                sk1 = skillz.index(str(a))
                sk2 = skillz.index(str(b))
                sk3 = skillz.index(str(c))
                sk4 = skillz.index(str(d))
                sk5 = skillz.index(str(e))
                 

                with st.container():
                    
                    with col1:
                        name = st.text_input("Cohort Name:",dd['data']['attributes']['name'])
                    with col12:
                        description = st.text_input("Description:",dd['data']['attributes']['description'])
                with st.container():
                    with col2:
                        skill1 = st.selectbox(
                                            "Skill1:",
                                            (skillz),
                                            index = sk1,
                                            )
                    with col3:
                        skill2 = st.selectbox(
                                            "Skill2:",
                                            (skillz),
                                            index = sk2,
                                            )
                    with col4:
                        skill3 = st.selectbox(
                                            "Skill3:",
                                            (skillz),
                                            index = sk3,
                                            )
                    with col5:
                        skill4 = st.selectbox(
                                            "Skill4:",
                                            (skillz),
                                            index = sk4,
                                            )
                    with col6:
                        skill5 = st.selectbox(
                                            "Skill5:",
                                            (skillz),
                                            index = sk5,
                                            )
                with st.container():
                    with col7:
                        skill1_icon = st.text_input("skill1_icon:",dd['data']['attributes']['skill1_icon'])
                    with col8:
                        skill2_icon = st.text_input("skill2_icon:",dd['data']['attributes']['skill2_icon'])
                    with col9:
                        skill3_icon = st.text_input("skill3_icon:",dd['data']['attributes']['skill3_icon'])
                    with col10:
                        skill4_icon = st.text_input("skill4_icon:",dd['data']['attributes']['skill4_icon'])
                    with col11:
                        skill5_icon = st.text_input("skill5_icon:",dd['data']['attributes']['skill5_icon'])

                    submitted = st.form_submit_button("Edit Ratings")

                    if submitted:
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
                        st.success('This is a success message!', icon="✅")
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
                        "https://truthful-health-29656117e6.strapiapp.com/api/cohorts/",
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
                        st.success('This is a success message!', icon="✅")

if choice=='Manage Personal Questions':
    try:
        URLPERSONAL = "https://truthful-health-29656117e6.strapiapp.com/api/personal-questions"
        d = requests.get(URLPERSONAL)
        dd = d.json()
        z = 0
        sn=[]
        tid=[]
        sid=[]
        sln=[]
        sn2 = []
        sn3 = []

        for i in range(len(dd['data'])):
            sn.append(dd['data'][z]['attributes']['question'])
            sn2.append(dd['data'][z]['attributes']['option'])
            sn3.append(dd['data'][z]['attributes']['type'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sn2,sn3,sid),columns=['question','option','type','id'])

        PERSONALQ = st.selectbox(
                "Select a question",
                (deptss['question']),
                index=None,
                placeholder="Select question here...",
                )
        question = deptss[deptss['question'] == PERSONALQ]
        QUESTIONIDID = question['id'].values
    except:
         st.write("Please Select a question above")


    tab1, tab2 = st.tabs(["Manage Questions", "Add Question" ])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/personal-questions/" + str(QUESTIONIDID[0])
            d = requests.get(url)
            dd = d.json()

            with st.form("my_formsxdsxdeddfecsscxxs"):
                    typez = ["Radio","Select","Text","Date","Number"]
                    typez1 = typez.index(str(dd['data']['attributes']['type']))

                    question = st.text_input("Question:",dd['data']['attributes']['question'])
                    option = st.text_input("Options:",dd['data']['attributes']['option'])
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                             index= typez1,
                                            )
                    submitted = st.form_submit_button("Edit Question")

                    if submitted:
                        requests.put(
                        url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": 
                                    {
                                        "question": question,
                                        "option": option,
                                        "type": type
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
            if st.button("Delete This Question"):
                requests.delete(url)
        except:
            st.write("Please select a question")
    with tab2:

        with st.form("my_form5"):
                    question = st.text_input("Question:")
                    option = st.text_input("Options:")
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                            )
                    submitted = st.form_submit_button("Add Question")


                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/personal-questions/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "question": question,
                                    "option": option,
                                    "type": type,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")

if choice=='Manage Contact Questions':
    try:
        URLCONTACT = "https://truthful-health-29656117e6.strapiapp.com/api/contact-details"
        d = requests.get(URLCONTACT)
        dd = d.json()
        z = 0
        sn=[]
        tid=[]
        sid=[]
        sln=[]
        sn2 = []
        sn3 = []

        for i in range(len(dd['data'])):
            sn.append(dd['data'][z]['attributes']['question'])
            sn2.append(dd['data'][z]['attributes']['option'])
            sn3.append(dd['data'][z]['attributes']['type'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sn2,sn3,sid),columns=['question','option','type','id'])

        CONTACTQ = st.selectbox(
                "Select a question",
                (deptss['question']),
                index=None,
                placeholder="Select question here...",
                )
        question = deptss[deptss['question'] == CONTACTQ]
        QUESTIONIDID = question['id'].values
    except:
         st.write("Please Select a question above")


    tab1, tab2 = st.tabs(["Manage Questions", "Add Question" ])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/contact-details/" + str(QUESTIONIDID[0])
            d = requests.get(url)
            dd = d.json()

            with st.form("my_formsxdsxdeddfecsscxxs"):
                    typez = ["Radio","Select","Text","Date","Number"]
                    typez1 = typez.index(str(dd['data']['attributes']['type']))

                    question = st.text_input("Question:",dd['data']['attributes']['question'])
                    option = st.text_input("Options:",dd['data']['attributes']['option'])
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                             index= typez1,
                                            )
                    submitted = st.form_submit_button("Edit Question")

                    if submitted:
                        requests.put(
                        url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": 
                                    {
                                        "question": question,
                                        "option": option,
                                        "type": type
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
            if st.button("Delete This Question"):
                requests.delete(url)
        except:
            st.write("Please select a question")
    with tab2:

        with st.form("my_form5"):
                    question = st.text_input("Question:")
                    option = st.text_input("Options:")
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                            )
                    submitted = st.form_submit_button("Add Question")


                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/contact-details/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "question": question,
                                    "option": option,
                                    "type": type,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")

if choice=='Manage Education Questions':
    try:
        URLEDUCATION = "https://truthful-health-29656117e6.strapiapp.com/api/qualification-questions"
        d = requests.get(URLEDUCATION)
        dd = d.json()
        z = 0
        sn=[]
        tid=[]
        sid=[]
        sln=[]
        sn2 = []
        sn3 = []

        for i in range(len(dd['data'])):
            sn.append(dd['data'][z]['attributes']['question'])
            sn2.append(dd['data'][z]['attributes']['option'])
            sn3.append(dd['data'][z]['attributes']['type'])
            sid.append(dd['data'][z]['id'])
            z = z + 1
            
        deptss = pd.DataFrame(data=zip(sn,sn2,sn3,sid),columns=['question','option','type','id'])

        EDUCATIONQ = st.selectbox(
                "Select a question",
                (deptss['question']),
                index=None,
                placeholder="Select question here...",
                )
        question = deptss[deptss['question'] == EDUCATIONQ]
        QUESTIONIDID = question['id'].values
    except:
         st.write("Please Select a question above")


    tab1, tab2 = st.tabs(["Manage Questions", "Add Question" ])

    with tab1:
        try:
            url = "https://truthful-health-29656117e6.strapiapp.com/api/qualification-questions/" + str(QUESTIONIDID[0])
            d = requests.get(url)
            dd = d.json()

            with st.form("my_formsxdsxdeddfecsscxxs"):
                    typez = ["Radio","Select","Text","Date","Number"]
                    typez1 = typez.index(str(dd['data']['attributes']['type']))

                    question = st.text_input("Question:",dd['data']['attributes']['question'])
                    option = st.text_input("Options:",dd['data']['attributes']['option'])
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                             index= typez1,
                                            )
                    submitted = st.form_submit_button("Edit Question")

                    if submitted:
                        requests.put(
                        url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": 
                                    {
                                        "question": question,
                                        "option": option,
                                        "type": type
                                    }
                            }))
                        st.success('This is a success message!', icon="✅")
            if st.button("Delete This Question"):
                requests.delete(url)
        except:
            st.write("Please select a question")
    with tab2:

        with st.form("my_form5"):
                    question = st.text_input("Question:")
                    option = st.text_input("Options:")
                    type = st.selectbox(
                                            "Type:",
                                            ("Radio","Select","Text","Date","Number"),
                                            )
                    submitted = st.form_submit_button("Add Question")


                    if submitted:
                        requests.post(
                        "https://truthful-health-29656117e6.strapiapp.com/api/qualification-questions/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "question": question,
                                    "option": option,
                                    "type": type,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")

            
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
# st.markdown(footer,unsafe_allow_html=True)
