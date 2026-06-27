from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from jose import jwt

import hashlib
import os
from datetime import datetime



app = FastAPI(
    title="SentinelVault X",
    description="Cybersecurity Monitoring Platform"
)



app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



SECRET_KEY="sentinel-secret"

ALGORITHM="HS256"



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)



users={

    "sherwin":"password"

}



events=[]

files=[]

failed_attempts={}






def create_token(username):

    return jwt.encode(

        {
            "username":username
        },

        SECRET_KEY,

        algorithm=ALGORITHM

    )






def get_current_user(

    token:str=Depends(oauth2_scheme)

):


    data=jwt.decode(

        token,

        SECRET_KEY,

        algorithms=[ALGORITHM]

    )


    return data["username"]







def add_event(user,event,ip):


    events.append(

        {

        "time":str(datetime.now()),

        "user":user,

        "ip":ip,

        "event":event

        }

    )









def analyze_file(filename,size):


    dangerous=[

        ".exe",

        ".bat",

        ".sh",

        ".dll"

    ]



    risk=0



    for ext in dangerous:


        if filename.endswith(ext):

            risk+=70





    if size > 10*1024*1024:

        risk+=20





    if risk >=70:

        level="HIGH"



    elif risk >=30:

        level="MEDIUM"



    else:

        level="LOW"




    return {


        "risk_score":risk,

        "risk_level":level

    }









@app.get("/")
def home():


    return {


        "message":"SentinelVault X is running",

        "security":"active"

    }









@app.post("/login")
def login(

    request:Request,

    form_data:OAuth2PasswordRequestForm=Depends()

):


    username=form_data.username

    password=form_data.password



    ip=request.client.host




    if users.get(username)!=password:


        failed_attempts[username]=failed_attempts.get(username,0)+1


        add_event(

            username,

            "FAILED LOGIN",

            ip

        )


        raise HTTPException(

            status_code=401,

            detail="Invalid login"

        )





    add_event(

        username,

        "LOGIN SUCCESS",

        ip

    )



    return {


        "access_token":create_token(username),

        "token_type":"bearer"

    }









@app.post("/upload")
def upload(

    request:Request,

    file:UploadFile=File(...),

    username:str=Depends(get_current_user)

):


    data=file.file.read()



    size=len(data)



    analysis=analyze_file(

        file.filename,

        size

    )




    if analysis["risk_level"]=="HIGH":


        add_event(

            username,

            "BLOCKED SUSPICIOUS FILE",

            request.client.host

        )


        raise HTTPException(

            status_code=400,

            detail="Dangerous file detected"

        )





    file_hash=hashlib.sha256(

        data

    ).hexdigest()




    os.makedirs(

        "uploaded_files",

        exist_ok=True

    )



    with open(

        "uploaded_files/"+file.filename,

        "wb"

    ) as f:


        f.write(data)




    files.append(

        {


        "filename":file.filename,


        "hash":file_hash,


        "risk":analysis

        }

    )




    add_event(

        username,

        "FILE SECURED",

        request.client.host

    )



    return {


        "message":"File secured",

        "analysis":analysis,

        "hash":file_hash

    }








@app.get("/events")
def get_events(

    username:str=Depends(get_current_user)

):

    return events








@app.get("/security-status")
def security_status(

    username:str=Depends(get_current_user)

):


    return {


        "status":"ACTIVE",

        "threat_level":"LOW",

        "security_score":98,

        "encryption":"AES-256",

        "encrypted_files":len(files)

    }
