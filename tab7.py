import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu


def tab7a__():
    URLTEAM = "http://localhost:1337/api/teams"
    dd = requests.get(URLTEAM).json()
    z = 0
    teamname=[]
    teamid=[]

    for i in range(len(dd['data'])):
        teamname.append(dd['data'][z]['attributes']['name'])
        teamid.append(dd['data'][z]['id'])
        z = z + 1
                
    deptss = pd.DataFrame(data=zip(teamname,teamid),columns=['name','id'])

    TEAM = st.selectbox(
                    "Select a Team",
                    (deptss['name']),
                    index=None,
                    placeholder="Select team here...",
                    )
    team = deptss[deptss['name'] == TEAM]
    return team['id'].values


def tab7b__(lid, tid):
        url = "http://localhost:1337/api/applicants/" + lid + "?populate=teams"
        dd = requests.get(url).json()
        with st.form("my_formsxdsxdeddfecvdvcddfvsscxxs"):
            try:
                "Current Team is: " + dd['data']['attributes']['teams']['data'][0]['attributes']['name']
            except:
                "No Team Currently assigned to learner"
                submitted = st.form_submit_button("Change team to selected")

        if submitted:
            requests.put(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
            {
                "data": 
                    {
                        "teams": tid,
                    }
            }))
            st.success('This is a success message!', icon="✅")
   