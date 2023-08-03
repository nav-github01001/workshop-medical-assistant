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


@routes.get("/messages/")
async def list_prompts(request:web.Request):
    authorization = request.headers.get("Authorization")
    lis = database.list_prompts(authorization)
    return web.json_response(data=lis[0],status=lis[1])

@routes.post("/messages/")
async def create_prompt(request:web.Request):
    request_json = await request.json()
    authorization = request.headers.get("Authorization").removeprefix("Bearer ")
    cleaned_prompts = [{"role":"system",
                        "content":""}]
    existing_prompts = database.list_prompts(authorization)["prompts"]
    for prompt in existing_prompts:
        cleaned_prompts.append({"role":"user","content":prompt["prompt"]})
        cleaned_prompts.append({"role":"assistant","content":prompt["response"]})
    api_response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages = cleaned_prompts
    )
    bot_response = api_response.choices[0].message
    _created_prompt = database.create_prompt(authorization,request_json["prompt"],bot_response)
    return web.json_response(data=_created_prompt[0],status=_created_prompt[1])
    


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8080)
