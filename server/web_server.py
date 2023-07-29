from aiohttp import web



routes = web.RouteTableDef()


@routes.post("/post")
async def return_index_webpage(request):
    return web.Response(body=index, content_type="text/html")


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="localhost")
