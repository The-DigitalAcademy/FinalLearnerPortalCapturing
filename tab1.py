import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu
def tab1__(url):
                
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