import openai
import tomllib
from aiohttp import web
from database_manager import DatabaseManager

database = DatabaseManager()

with open("./config.toml") as f:
    auth = tomllib.loads(f.read())

openai.api_key = auth["openai_api_key"]


routes = web.RouteTableDef()
@routes.get("/")
async def index(request:web.Request):
    return web.json_response(data={"message":"Hello World"})

@routes.post("/users")
async def new_user(request:web.Request):
    request_json = await request.json()
    print(request_json)
    _new_user = database.create_user(request_json)
    return web.json_response(data=_new_user[0],status=_new_user[1])

@routes.post("/users/auth")
async def auth_user(request:web.Request):
    request_json = await request.json()
    _auth_user = database.auth_user(request_json)
    return web.json_response(data=_auth_user[0],status=_auth_user[1])


@routes.get("/messages/{id}")
async def list_prompts(request:web.Request):
    authorization = request.headers.get("Authorization")
    lis = database.list_prompts(authorization)
    return web.json_response(data=lis[0],status=lis[1])

@routes.post("/messages")
async def create_prompts(request:web.Request):
    authorization = request.headers.get("Authorization")
    #return web.json_response(data=lis[0],status=lis[1])
    


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8080)
