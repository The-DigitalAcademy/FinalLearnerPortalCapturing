import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu

def tab5a__(dd, lid):
    if (len(dd['data']['attributes']['shaperreviews']['data'][0]['attributes'])> 0):
                id = dd['data']['attributes']['shaperreviews']['data'][0]['id']
            
                with st.form("my_formsxdsxcs"):
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
                                    "applicants": lid,
                                    "review": review,
                                    }
                        }))
                        st.success('This is a success message!', icon="✅")
                
def tab5b__():
       with st.form("my_formxd3"):
                    review = st.text_input("Review:")

                    submitted = st.form_submit_button("Add Review")
                    if submitted:

                        requests.post(
                        "http://localhost:1337/api/shaperreviews/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
                                    "applicants": lid,
                                    "review": review,
                                }
                            }
                        ),
                    )
                        st.success('This is a success message!', icon="✅")