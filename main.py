from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import jwt
import re

class User(BaseModel):
    uid: str
    pwd: str
    verified: bool = False

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="top_secret")

def issue_token(uid, pwd):
    token = uid + "+" + pwd
    return token

def decode_token(toke):
    return toke.split('+')

@app.get('/login/')
async def sign_in():
    with open('signin.html', 'r') as fd:
        signin_HTML = fd.read()
    return HTMLResponse(signin_HTML)

@app.post('/token/')
async def tokenize(request: Request, uid: str = Form(...), pwd: str = Form(...)):
    token = issue_token(uid, pwd)
    request.session["jwt_token"] = token
    return RedirectResponse(url='/', status_code=302)

@app.get("/")
async def land_me(request: Request):
    token = request.session.get('jwt_token', None)
    if token:
        uid, pwd = decode_token(token)
        return {'status': 'pass', 'uid': uid, 'pwd': pwd}
    else:
        return {"status": "fail"}
    
@app.get('/welcome')
async def whoami():
    pass