import openai
import tomllib
from aiohttp import web
from database_manager import DatabaseManager

database = DatabaseManager()

with open("./config.toml") as f:
    auth = tomllib.loads(f.read())

openai.api_key = auth["openai_api_key"]


routes = web.RouteTableDef()


@routes.post("/users")
async def new_user(request:web.Request):
    request_json = request.json()
    _new_user = database.create_user(request_json)
    return _new_user

@routes.post("/users/auth")
async def auth_user(request:web.Request):
    request_json = request.json()
    _auth_user = database.auth_user(request_json)
    return _auth_user

@routes.get("/messages/{id}")
async def list_prompts(request:web.Request):
    request_headers = request.headers
    auth = request_headers["Authorization"]



app = web.Application()
app.add_routes(routes)
web.run_app(app, host="localhost")
