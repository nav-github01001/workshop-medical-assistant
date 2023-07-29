import openai
import tomllib
from aiohttp import web



with open("./auth.toml") as f:
    auth = tomllib.loads(f.read())

openai.api_key = auth["openai_api_key"]


routes = web.RouteTableDef()


@routes.post("/post")
async def return_index_webpage(request):
    ...


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="localhost")
