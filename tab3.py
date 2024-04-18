import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu


def tab3a__(dd, lid):
    
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
                        
                        ff = "http://localhost:1337/api/softskillratings/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "applicants": lid,
                                    "problemsolving": problemsolving,
                                    "interpersonal": interpersonal,
                                    "communication": communication,
                                    "teamwork": teamwork,
                                    "leadership": leadership,
                                    "mostimproved" : str(mostimproved)
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")

def tab3b__(url, lid):
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
                        "http://localhost:1337/api/softskillratings/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": lid,
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