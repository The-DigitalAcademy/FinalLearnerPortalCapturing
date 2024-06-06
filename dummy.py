
        

import requests, json
requests.post(
     "http://localhost:1337/api/learners/",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "data": {
        "firstname": "Freddys",
        "lastname": "Khumalo",
        "province": "Gauteng",
        "email": "fk@gmail.com",
        "dob": "1983-08-11",
        "southafrican": True,
        "male": True,
        "city": "Johannesburg",
        "physicaladdress": "123 Time Square Avenue\nBraamfonteinwerf\n2001",
        "postaladdress": "123 Time Square Avenue\nBraamfonteinwerf\n2001",
        "homelanguage": "Sotho",
        "highestqualification": "Diploma",
        "nextofkin": "Gerald",
        "postalcode": 1245,
        "currentlystudying": True,
        "githublink": "https://www.linkedin.com/in/sbusiso-phakathi-6085a849/",
        "linkedinlink": "https://www.linkedin.com/in/sbusiso-phakathi-6085a849/",
        "previouscompany1": "The Real Coffee",
        "previouscompany2": "Shop Fresh",
        "company1position": "Barrister",
        "company2position": "Teller",
        "termofcontractcompany1": 3,
        "termofcontractcompany2": 2,
        "keyresponsibilitiescompany1": "Preparing Coffee",
        "keyresponsibilitiescompany2": "Checking out customers",
        "Program": "Egypt",
        "idnumber": "29837464323",
        "phonenumber": "432534576543",
        "nextofkinnumber": "4565876543",
        "imageurl": "https://github.com/Sbusiso-Phakathi/recruit/blob/main/Steve_Shogwe.png?raw=true",
        "createdAt": "2024-06-06T11:36:39.845Z",
        "updatedAt": "2024-06-06T12:55:40.876Z",
        "publishedAt": "2024-06-06T11:40:41.052Z"
                                }
                            }
                        ),
                    )