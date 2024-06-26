import streamlit as st
import tab1 as tab1__
import tab2 as tab2__
import tab3 as tab3__
import tab4 as tab4__
import tab5 as tab5__
import tab6 as tab6__
import tab7 as tab7__

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
        # {'label':"Manage Personal Questions"},
        # {'label':"Manage Contact Questions"},
        # {'label':"Manage Education Questions"},
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
                    (['Egypt','PWD','Full Stack']),
                    index=None,
                    placeholder="Select cohort here...",
                    )
        URLCOHORT = "http://localhost:1337/api/learners?filters[$or][0][Program][$eq]="+str(COHORT)
        dd = requests.get(URLCOHORT).json()
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
            url = "http://localhost:1337/api/learners/" + str(LEARNERID[0])   
            tab1_ = tab1__.tab1__(url)
        except:
            st.write("Please select a learner")

    with tab2:
        try:
           url = "http://localhost:1337/api/learners/" + str(LEARNERID[0])  
           tab2_ = tab2__.tab2__(url)
        except:
            st.write("")
 
    with tab3:
        try:
            url2 = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews,responsibilities"
            d = requests.get(url2)
            dd = d.json()
            try:
                tab3_ = tab3__.tab3a__(dd, str(LEARNERID[0]))
            except:
                tab3_ = tab3__.tab3b__(str(LEARNERID[0]))
        except:
            st.write("")

    with tab4:     
        try:
            url2 = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews,responsibilities"
            d = requests.get(url2)
            dd = d.json()
            try:
                tab4_ = tab4__.tab4a__(dd, str(LEARNERID[0]))
            except:
                tab4_ = tab4__.tab4a__(str(LEARNERID[0]))
        except:
            st.write("")

    with tab5:     
        try:
            url2 = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews,responsibilities"
            d = requests.get(url2)
            dd = d.json()
            try:
                tab5_ = tab5__.tab5a__(dd, str(LEARNERID[0]))
            except:
                tab5_ = tab5__.tab5b__(str(LEARNERID[0]))
        except:
             st.write("")

    with tab6:     
        try:
            url2 = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) +"?populate=teams,softskillratings,techskillratings,shaperreviews,responsibilities"
            d = requests.get(url2)
            dd = d.json()
            try:
                tab6_ = tab6__.tab6a__(dd, str(LEARNERID[0]))
            except:
                tab6_ = tab6__.tab6b__(str(LEARNERID[0]))
            
        except:
            st.write("")


    with tab7:
        try:
            tab7_ = tab7__.tab7a__(str(LEARNERID[0]))
        except:
            st.write("")

            
    with tab8:
        try:
            URLPROJECT = "http://localhost:1337/api/projects"
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

                url = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) + "?populate=projects"
                d = requests.get(url)
                dd = d.json()

                with st.form("my_formsxdsxddwceddsdsdsfecvdvcddfvsscxxs"):
                        try:
                            "Current Project is: " + dd['data']['attributes']['projects']['data'][0]['attributes']['projectname']
                        except:
                             "No project currently assigned to learner"

                        submitted = st.form_submit_button("Change project to selected")
                        

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

                url = "http://localhost:1337/api/learners/" + str(LEARNERID[0]) + "?populate=communicationratingdescriptions,interpersonalratingdescriptions,leadershipratingdescriptions,problemsolvingratingdescriptions,teamworkratingdescriptions,techskillsratingdescriptions,softskilldescriptions"
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
                placeholder="Select team leader here...",
                )
        Learn = deptss[deptss['fullname'] == LEADER]
        LEADERID = Learn['id'].values
    except:
         st.write("Please Select a Team Leader Above")


    tab1, tab2 = st.tabs(["Manage Team Leader", "Add Team Leader" ])

    with tab1:
        try:
            url = "http://localhost:1337/api/teamleaders/" + str(LEADERID[0])
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
                        st.success('This is a success message!', icon="✅")
               
if choice=='Manage Team':
    try:
        URLLEADER = "http://localhost:1337/api/teams"
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
            url = "http://localhost:1337/api/teams/" + str(TEAMID[0])
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
                        "http://localhost:1337/api/teams/",
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
            url = "http://localhost:1337/api/projects/" + str(PROJECTID[0]) + "?populate=teams"
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
                        st.success('This is a success message!', icon="✅") 

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
                        st.success('This is a success message!', icon="✅")

if choice=='Manage Personal Questions':
    try:
        URLPERSONAL = "http://localhost:1337/api/personal-questions"
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
            url = "http://localhost:1337/api/personal-questions/" + str(QUESTIONIDID[0])
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
                        "http://localhost:1337/api/personal-questions/",
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
        URLCONTACT = "http://localhost:1337/api/contact-details"
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
            url = "http://localhost:1337/api/contact-details/" + str(QUESTIONIDID[0])
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
                        "http://localhost:1337/api/contact-details/",
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
        URLEDUCATION = "http://localhost:1337/api/qualification-questions"
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
            url = "http://localhost:1337/api/qualification-questions/" + str(QUESTIONIDID[0])
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
                        "http://localhost:1337/api/qualification-questions/",
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
