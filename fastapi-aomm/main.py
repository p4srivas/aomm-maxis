import uvicorn
from fastapi import FastAPI, HTTPException, Request, Query, Body, Depends, Form, status
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helper import insert_new_user, get_users, get_all_users, get_user_data, get_user_by_email, verify_password, change_password, get_user_role_by_session_id, update_last_login, update_user, get_user_ops_data
from helper import get_sub_dimensions, get_attributes, get_capbilities, insert_update_user_response, get_capbilities_for_user_response, get_capbilities_for_review
from helper import get_display_values, get_dashboard_graphs, get_dashboard_index_table, get_display_text, get_autotext
import pandas as pd
from pydantic import EmailStr, Field
from fastapi.security import OAuth2PasswordBearer
import re
#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from database import engine, get_db
from models import UserSchema, UserLogin, User, Base
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decodeJWT, signJWT, signoutJWT, encode_session, decode_session

import hashlib
from datetime import datetime, timezone

from app_config import setenv

setenv()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# JWT authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom exception handler for validation errors"""
    return RedirectResponse(url="/error?error_message=" + str(exc), status_code=status.HTTP_303_SEE_OTHER)

favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/error', response_class=HTMLResponse)
async def error_page(request: Request, error_message: str):
    """Render error page"""
    #print('in error get method')
    return templates.TemplateResponse('error.html', {"request": request, "error_message": error_message})


async def get_current_user(access_token: str = Depends(oauth2_scheme), 
                            db: AsyncSession = Depends(get_db)):
    """Get current user from JWT token"""
    try:
        payload = decodeJWT(access_token)
        email = payload.get("user_id")
        if not email:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        user = await get_user_by_email(db, email.upper())
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@app.get('/logout', response_class=HTMLResponse)
async def signout(request: Request,
                        session_id: str):
    """Render signup page"""
    #print('in signout get method')
    expired_access_token = signoutJWT(session_id)
    #if not decodeJWT(expired_access_token):
    #    print("access_token expired.", expired_access_token)

    return templates.TemplateResponse(
                                        'login.html', 
                                        {
                                            "request": request, 
                                            "access_token": None,
                                            "session_id": None, 
                                            "error_message": None, "success_message": None, 
                                            "user_table": None
                                        }
                                    )


@app.get('/signup', response_class=HTMLResponse)
async def signup_page(request: Request,
                        access_token: str,
                        session_id: str):
    """Render signup page"""
    #print('in signup get method')
    return templates.TemplateResponse(
                                        'signup.html', 
                                        {
                                            "request": request, 
                                            "access_token": access_token, 
                                            "session_id": session_id,
                                            "error_message": None, 
                                            "success_message": None, 
                                            "user_table": None
                                        }
                                    )

@app.post("/signup", dependencies=[Depends(JWTBearer())])
async def create_user(
        request: Request,
        access_token: str = Form(),
        session_id: str = Form(),
        user_ops_map: str = Form(),
        role: str = Form(),
        fname: str = Form(),
        lname: str = Form(),
        email: str = Form(), 
        hashed_password: str = Form(),
        confirm_hashed_password: str = Form(),
        db: AsyncSession = Depends(get_db)
    ):
    try:
        user_role = get_user_role_by_session_id(decode_session(session_id))
        
        if user_role != 'admin':
            raise HTTPException(status_code=401, detail="Insufficient priviledges for this operation : '" + decode_session(session_id) + "'")

        if not EMAIL_REGEX.match(email):
            raise HTTPException(status_code=401, detail="Invalid email '" + email + "'. Format of email address is not correct.")

        if hashed_password != confirm_hashed_password:
            raise HTTPException(status_code=401, detail="Password and Confirm Password do not match.")

        if not user_ops_map or user_ops_map == "operations,":
            raise HTTPException(status_code=401, detail="Atleast one operational domain should be assigned to a user.")

        # Find user by email
        db_user = await get_user_by_email(db, email.upper())

        if db_user:
            raise HTTPException(status_code=401, detail="User with email '" + email + "' already exists.")

        # Hash the password before storing
        sha256_hashed_password = hash_password(hashed_password)
        
        user_data = insert_new_user(role, fname, lname, email.upper(), sha256_hashed_password, user_ops_map)
        #print(user_data)
        #print(user_ops_map)
        #if not access_token or access_token=="":
        #    new_access_token = signJWT(email)   
        #    access_token = new_access_token["access_token"]    

        return templates.TemplateResponse(
            'signup.html',
            {
                'request': request,
                "access_token": access_token,
                "session_id": session_id,
                "error_message": None, "success_message": "Form submitted successfully!",
                'user_table': user_data.to_html(classes='display', index=False, index_names=False, border=0)
            }
        )                
    except Exception as e:
        return templates.TemplateResponse('signup.html', {'request': request, 
                                            "access_token": access_token, "session_id": session_id, 
                                            "error_message": str(e), "success_message": None})


@app.get('/selectusertoedit', response_class=HTMLResponse)
async def select_edituser_page(request: Request,
                        access_token: str,
                        session_id: str):
    """Render edituser page"""
    try:
        user_role = get_user_role_by_session_id(decode_session(session_id).upper())
        
        if user_role != 'admin':
            raise HTTPException(status_code=401, detail="Insufficient priviledges for this operation : '" + decode_session(session_id) + "'")    
    

        user_table_data, user_data = get_all_users()
        return templates.TemplateResponse(
                                            'edituser.html', 
                                            {
                                                "request": request,
                                                "access_token": access_token, 
                                                "session_id": session_id,
                                                "user_id": None,
                                                "error_message": None, 
                                                "success_message": None, 
                                                #"user_table": user_table_data.to_html(classes='display', index=False, index_names=False, border=0),
                                                "user_table": None,
                                                "show_table": True,
                                                "user_data": user_data
                                            }
                                        )
    except Exception as e:
        return templates.TemplateResponse('edituser.html', {'request': request, 
                                            "access_token": access_token, "session_id": session_id, 
                                            "error_message": str(e), "success_message": None})

@app.get('/edituser', response_class=HTMLResponse)
async def show_edituser_page(request: Request,
                        access_token: str,
                        session_id: str,
                        user_id: str):
    """Render edituser page"""
    try:
        user_role = get_user_role_by_session_id(decode_session(session_id))
        
        if user_role != 'admin':
            raise HTTPException(status_code=401, detail="Insufficient priviledges for this operation : '" + decode_session(session_id) + "'")    
    

        user_data, user_ops_list = get_user_data(user_id)
        return templates.TemplateResponse(
                                            'edituser.html', 
                                            {
                                                "request": request,
                                                "access_token": access_token, 
                                                "session_id": session_id,
                                                "user_id": user_id,
                                                "error_message": None, 
                                                "success_message": None, 
                                                #"user_table": user_data.to_html(classes='display', index=False, index_names=False, border=0)
                                                "show_table": False,
                                                "user_table": None,
                                                "user_data": user_data,
                                                "user_ops_list": user_ops_list
                                            }
                                        )
    except Exception as e:
        return templates.TemplateResponse('edituser.html', {'request': request, 
                                            "access_token": access_token, "session_id": session_id, 
                                            "error_message": str(e), "success_message": None})

@app.post("/edituser", dependencies=[Depends(JWTBearer())])
async def update_edituser_page(
        request: Request,
        access_token: str = Form(),
        session_id: str = Form(),
        user_id: str = Form(),
        role: str = Form(),
        fname: str = Form(),
        lname: str = Form(),
        hashed_password: str = Form(),
        confirm_hashed_password: str = Form(),
        user_ops_map: str = Form(),
        db: AsyncSession = Depends(get_db)
    ):
    try:
        user_role = get_user_role_by_session_id(decode_session(session_id))
        
        if user_role != 'admin':
            raise HTTPException(status_code=401, detail="Insufficient priviledges for this operation : '" + decode_session(session_id) + "'")

        if hashed_password != confirm_hashed_password:
            raise HTTPException(status_code=401, detail="Password and Confirm Password do not match.")

        if not user_ops_map or user_ops_map == "operations,":
            raise HTTPException(status_code=401, detail="Atleast one operational domain should be assigned to a user.")

        # Find user by email
        email = user_id
        db_user = await get_user_by_email(db, email)

        if not db_user:
            raise HTTPException(status_code=401, detail="User with email '" + email + "' does not exist.")

        # Hash the password before storing
        sha256_hashed_password = hash_password(hashed_password)
        user_data, user_ops_list = update_user(user_id, role, fname, lname, sha256_hashed_password, 't', user_ops_map)
        #print(user_id, role, fname, lname, hashed_password, confirm_hashed_password, sha256_hashed_password, user_ops_map)
        return templates.TemplateResponse(
            'edituser.html',
            {
                "request": request,
                "access_token": access_token,
                "session_id": session_id,
                "user_id": user_id,
                "error_message": None, "success_message": "Form submitted successfully!",
                "show_table": False,
                "user_data": user_data,
                "user_table": None,
                "user_ops_list": user_ops_list
            }
        )                
    except Exception as e:
        return templates.TemplateResponse('edituser.html', {'request': request, 
                                            "access_token": access_token, "session_id": session_id, 
                                            "error_message": str(e), "success_message": None})


@app.get('/', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def root_page(request: Request):
    """Render login page"""
    #print('in root get method')
    return templates.TemplateResponse('login.html', {"request": request, "error_message": None, "success_message": None, "user_table": None})

@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    """Render login page"""
    #print('in login get method')
    return templates.TemplateResponse('login.html', {"request": request, "error_message": None, "success_message": None, "user_table": None})

@app.post("/login")
async def user_login(
        request: Request,
        email: str = Form(), 
        hashed_password: str = Form(), 
        db: AsyncSession = Depends(get_db)
    ):
    try:
        """User login endpoint"""

        if not EMAIL_REGEX.match(email):
            raise HTTPException(status_code=401, detail="Invalid login Id '" + email + "'. Login Id is in format of email address.")

        # Find user by email
        db_user = await get_user_by_email(db, email.upper())

        if not db_user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        # Verify password
        if not verify_password(hashed_password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        # Generate JWT token
        access_token = signJWT(email.upper()) 
        session_id = encode_session(email.upper())      

        # Update last login timestamp 
        update_last_login(email.upper())

        return RedirectResponse(url="/assessment?access_token="+access_token["access_token"]+"&session_id="+session_id+"&service=SERVICE_MOBILE&operation=OP_AO&operation_sub_group=OP_AO_01", status_code=302)
    except Exception as e:
        return templates.TemplateResponse('login.html', {"request": request, "error_message": str(e)})  

@app.get('/password', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def password_change_page(request: Request,
                                access_token: str,
                                session_id: str):
    """Render password change page"""
    #print('in password get method')
    return templates.TemplateResponse('password.html', {
                                                        "request": request,
                                                        "access_token": access_token,
                                                        "session_id": session_id,
                                                        "error_message": None, "success_message": None,
                                                        "user_id": decode_session(session_id), "user_table": None})

@app.post('/password', dependencies=[Depends(JWTBearer())])
async def save_password_page(
        request: Request,
        access_token: str = Form(),
        session_id: str = Form(),
        user_id: str = Form(), 
        email: str = Form(),
        password_string: str = Form(), 
        new_password_string: str = Form(),
        db: AsyncSession = Depends(get_db)):

    #print(access_token, session_id, user_id, email, password_string, new_password_string)

    try:
        """User change password endpoint"""
        # Find user by email
        db_user = await get_user_by_email(db, user_id)


        if not db_user:
            raise HTTPException(status_code=401, detail="Incorrect email")

        # Verify password
        if not verify_password(password_string, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        sha256_hashed_password = hash_password(new_password_string)
        user_data = change_password(user_id, sha256_hashed_password)  

        return templates.TemplateResponse('password.html', {
                                                            "request": request,
                                                            "access_token": access_token,
                                                            "session_id": session_id,
                                                            "error_message": None, "success_message": "Password saved successfully.",
                                                            "user_id": decode_session(session_id)})
        
    except Exception as e:
        return templates.TemplateResponse('password.html', {"request": request, "error_message": str(e), "success_message": None, "user_id": decode_session(session_id)})    
    

@app.get('/assessment', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def assessment_page(request: Request, 
                            access_token: str,
                            session_id: str,
                            service: str, 
                            operation: str, 
                            operation_sub_group: str):
    try:      
        user_ops_list = get_user_ops_data(decode_session(session_id))
        capability_data = get_capbilities(service, operation, operation_sub_group)
        no_of_capabilities = len(capability_data)
        user_selection = {'service':service, 'operation':operation, 'operation_sub_group': operation_sub_group}

        print("session_id:", session_id, "user_id:", decode_session(session_id), "operation:", operation, "operation_sub_group:", operation_sub_group)
        return templates.TemplateResponse(
                    'assessment.html',
                    {
                        "request": request,
                        "access_token": access_token,
                        "session_id": session_id,
                        "error_message": None, "success_message": None,
                        "user_id": decode_session(session_id),
                        "user_selection": user_selection,
                        "no_of_capabilities": no_of_capabilities,
                        "user_selection_text": get_display_values(service, operation, operation_sub_group),
                        "capability_data": capability_data,
                        "user_ops_list": user_ops_list
                    }
                )   
    except Exception as e:
        return templates.TemplateResponse('assessment.html', {"request": request, "access_token": access_token, "error_message":  str(e), "success_message": None})

@app.post('/dashboard', dependencies=[Depends(JWTBearer())])
async def save_assessment_page(request: Request, 
                            access_token: str = Form(),
                            session_id: str = Form(),
                            user_id: str = Form(),
                            service: str = Form(), 
                            operation: str = Form(), 
                            operation_sub_group: str = Form(),
                            no_of_capabilities: int = Form(),
                            user_response: str = Form()                            
            ):
    try:
        #print(access_token, session_id, user_id, service, operation, operation_sub_group, no_of_capabilities, list(eval(user_response).values()))
        sa_uuid = insert_update_user_response(user_id, service, operation, operation_sub_group, no_of_capabilities, list(eval(user_response).values()))
        index_data = get_dashboard_index_table(service, operation, operation_sub_group)
        fig1, fig2 = get_dashboard_graphs(user_id, service, operation, operation_sub_group)
        user_ops_list = get_user_ops_data(decode_session(session_id))
        capability_data = get_capbilities_for_user_response(user_id, service, operation, operation_sub_group)
        autotext = get_autotext(user_id, service, operation, operation_sub_group)
        return templates.TemplateResponse(
                    'dashboard.html',
                    {
                        "request": request,
                        "access_token": access_token,
                        "session_id": session_id,
                        "error_message": None, "success_message": None,
                        "user_id": user_id,
                        "user_selection": {'service':service, 'operation':operation, 'operation_sub_group': operation_sub_group},
                        "no_of_capabilities": len(capability_data),
                        "user_selection_text": get_display_values(service, operation, operation_sub_group),
                        "index_table": index_data.to_html(classes='display', index=False, index_names=False, border=0),
                        "fig1": fig1.to_html(None, full_html=False),
                        "fig2": fig2.to_html(None, full_html=False),
                        "capability_data": capability_data,
                        "user_ops_list": user_ops_list,
                        "autotext": autotext
                    }
                ) 
    
    except Exception as e:
        return templates.TemplateResponse('dashboard.html', {"request": request, "access_token": access_token, "error_message":  str(e), "success_message": None})

@app.get('/dashboard', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def dashboard_page(request: Request, 
                            access_token: str,
                            session_id: str,
                            service: str, 
                            operation: str, 
                            operation_sub_group: str):
    try: 
        user_id = decode_session(session_id)
        index_data = get_dashboard_index_table(service, operation, operation_sub_group)
        fig1, fig2 = get_dashboard_graphs(user_id, service, operation, operation_sub_group)
        user_ops_list = get_user_ops_data(decode_session(session_id))
        capability_data = get_capbilities_for_user_response(user_id, service, operation, operation_sub_group)
        autotext = get_autotext(user_id, service, operation, operation_sub_group)
        return templates.TemplateResponse(
                    'dashboard.html',
                    {
                        "request": request,
                        "access_token": access_token,
                        "session_id": session_id,
                        "error_message": None, "success_message": None, 
                        "user_selection": {'service':service, 'operation':operation, 'operation_sub_group': operation_sub_group},
                        "user_selection_text": get_display_values(service, operation, operation_sub_group),
                        "index_table": index_data.to_html(classes='display', index=False, index_names=False, border=0),
                        "fig1": fig1.to_html(None, full_html=False),
                        "fig2": fig2.to_html(None, full_html=False),                        
                        "capability_data": capability_data,
                        "user_ops_list": user_ops_list,
                        "autotext": autotext
                    }
                ) 
    
    except Exception as e:
        return templates.TemplateResponse('dashboard.html', {"request": request, "access_token": access_token, "error_message":  str(e), "success_message": None})

@app.get('/attributes/{sub_dimension_id}', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def attributesbysubdimension_page(request: Request, access_token: str, sub_dimension_id: str):
    try:      
        attributes_data = get_attributes(sub_dimension_id)
        return templates.TemplateResponse(
            'attributes.html',
            {
                "request": request,
                "access_token": access_token,
                "error_message": None, "success_message": None,
                "attributes_table": attributes_data.to_html(classes='display', index=False, index_names=False, border=0)
            }
        )    
    
    except Exception as e:
        return templates.TemplateResponse('attributes.html', {'request': request, "access_token": access_token, "error_message": str(e)})



@app.get('/criteria', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def criteria_page(request: Request, access_token: str, session_id: str, dimension: str, sub_dimension: str):
    try:      
        attributes_data = get_attributes(sub_dimension)

        return templates.TemplateResponse(
                    'criteria.html',
                    {
                        "request": request,
                        "access_token": access_token,
                        "session_id": session_id,
                        "user_selection": {'dimension':dimension, 'sub_dimension':sub_dimension},
                        "user_selection_text": get_display_text(dimension, sub_dimension),
                        "error_message": None, "success_message": None,
                        "criteria_table": attributes_data.to_html(classes='display', index=False, index_names=False, border=0)
                    }
                ) 
    
    except Exception as e:
        return templates.TemplateResponse('criteria.html', {'request': request, "access_token": access_token, "error_message": str(e)})


# @app.get('/review', response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
# async def review_page(request: Request, 
#                             access_token: str,
#                             session_id: str,
#                             service: str, 
#                             operation: str, 
#                             operation_sub_group: str):
#     try: 
#         user_id = decode_session(session_id)
#         #print(access_token, session_id, user_id, service, operation, operation_sub_group)
#         user_ops_list = get_user_ops_data(decode_session(session_id))
#         review_data = get_capbilities_for_review(service, operation, operation_sub_group)
#         return templates.TemplateResponse(
#                     'review.html',
#                     {
#                         "request": request,
#                         "access_token": access_token,
#                         "session_id": session_id,
#                         "error_message": None, "success_message": None, 
#                         "user_selection": {'service':service, 'operation':operation, 'operation_sub_group': operation_sub_group},
#                         "user_selection_text": get_display_values(service, operation, operation_sub_group),
#                         "user_ops_list": user_ops_list,
#                         "review_data": review_data
#                     }
#                 ) 
    
#     except Exception as e:
#         return templates.TemplateResponse('review.html', {"request": request, "access_token": access_token, "error_message":  str(e), "success_message": None})
