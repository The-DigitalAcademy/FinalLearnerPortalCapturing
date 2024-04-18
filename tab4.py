import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu

def tab4a__(dd, lid):
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
                                            "Most Improved:",
                                            ('Python','ReactJS','HTML','Javascript','CSS'),
                                            index= a - 1)
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
                                    "applicants": str(lid),
                                    "skill1": str(skill1),
                                    "skill2": str(skill2),
                                    "skill3": str(skill3),
                                    "skill4": str(skill4),
                                    "skill5": str(skill5),
                                    "mostimproved": str(mostimproved),

                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
        
def tab4b__(lid):
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
                                            "Most Improved:",
                                            ('Python','ReactJS','HTML','Javascript','CSS'),
                                            )

                    submitted = st.form_submit_button("Add Ratings")
                    if submitted:

                        requests.post(
                        "http://localhost:1337/api/technicalskills/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": lid,
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