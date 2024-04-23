import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu


def tab7a__(lid):
    try:
            URLTEAM = "http://localhost:1337/api/teams"
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
                url = "http://localhost:1337/api/applicants/" + str(lid) + "?populate=teams"
                d = requests.get(url)
                dd = d.json()
                with st.form("my_formsxdsxdeddfecvdvcddfvsscxxs"):
                        try:
                            st.write("Current Team is: " + dd['data']['attributes']['teams']['data'][0]['attributes']['name'])
                        except:
                             st.write("No Team Currently assigned to learner")
                        submitted = st.form_submit_button("Change team to selected")

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