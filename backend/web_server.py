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
    new_user = database.create_user(request_json)
    return new_user


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="localhost")
