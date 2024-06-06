
import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu

def tab8a__():
    URLPROJECT = "http://localhost:1337/api/projects"
    d = requests.get(URLPROJECT)
    dd = d.json()
    z = 0
    sn=[]
    sid=[]

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

def tab8b__(lid):
    url = "http://localhost:1337/api/learners/" + lid+ "?populate=projects"
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