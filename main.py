from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import jwt

class User(BaseModel):
    uid: str
    pwd: str
    verified: bool = False

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="top_secret")

@app.post('/login/')
async def sign_in(uid: str, pwd: str, session: dict, request: Request):
    request.session["jwt_token"] = uid+"+"+pwd
    return 'ok'

@app.get("/")
async def land_me(request: Request):
    token = request.session.get('jwt_token', None)
    if token:
        return {"Pass": token}
    else:
        return {"Pass": "You shall not!"}
    

