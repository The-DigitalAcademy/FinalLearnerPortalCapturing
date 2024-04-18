import streamlit as st
import json
from datetime import datetime

import hydralit_components as hc
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu

def tab2__(url): 
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
            province = st.selectbox("Province:",("Gauteng", "North West", "Mpumalanga", "Free State","Limpopo",
                                    "Northen Cape","Western Cape", "Eastern Cape", "KwaZulu Natal"),
                                    index= a - 1,)
            imageurl = st.text_input("Profile Picture URL:",dd['data']['attributes']['imageurl'])

            with col2:
                physicaladdress = st.text_input("Physical Address:",dd['data']['attributes']['physicaladdress'])
                postaladdress = st.text_input("Postal Address:",dd['data']['attributes']['postaladdress'])
                postalcode = st.number_input("Postal Code:",dd['data']['attributes']['postalcode'])
            with col3:
                # nextofkinnumber = st.text_input("Next of Kin Number:",dd['data']['attributes']['nextofkinnumber'])
                phonenumber = st.text_input("Phone Number:",dd['data']['attributes']['phonenumber'])
                nextofkinnumber = st.text_input("Next of kin Number:",dd['data']['attributes']['nextofkinnumber'])

            with col4:
                email = st.text_input("Email:",dd['data']['attributes']['email'])
                githublink = st.text_input("Github Link:",dd['data']['attributes']['githublink'])
                linkedinlink = st.text_input("Linkedin Link:",dd['data']['attributes']['linkedinlink'])

            submitted = st.form_submit_button("Edit Contact Details")
      
            if submitted:
                requests.put(url,
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