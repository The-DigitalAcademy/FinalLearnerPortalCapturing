import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu


def tab6a__(dd, lid):
    if (len(dd['data']['attributes']['responsibilities']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['responsibilities']['data'][0]['id']
                with st.form("my_formsxxsdsqdxcds"):
                    responsibility = st.text_input("Responsibilities:",dd['data']['attributes']['responsibilities']['data'][0]['attributes']['responsibility'])
                    
                    submitted = st.form_submit_button("Edit Responsibility")

                if submitted:
                        ff = "http://localhost:1337/api/responsibilities/"+str(id)
                        requests.put(
                        ff,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                    "data": 
                                    {
                                    "applicants": lid,
                                    "responsibility": responsibility,
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")

def tab6b__(lid):
       with st.form("my_form3waxdsa"):
                    responsibility = st.text_input("Responsibility:")

                    submitted = st.form_submit_button("Add Responsibility")
                    if submitted:
                        responsibility
                        requests.post(
                        "http://localhost:1337/api/responsibilities/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": lid,
                                    "responsibility": responsibility,
                                }
                            }
                        ),
                    )    
                        st.success('This is a success message!', icon="✅") 