from user_mcp_server.user_retrieve_user119 import user_retrieve_user119
from user_mcp_server.user_retrieve_user459 import user_retrieve_user459
from user_mcp_server.user_retrieve_user555 import user_retrieve_user555


from fastmcp import FastMCP
from fastapi import FastAPI


mcp119_app = user_retrieve_user119.http_app(path='/mcp')
mcp459_app = user_retrieve_user459.http_app(path='/mcp')
mcp555_app = user_retrieve_user555.http_app(path='/mcp')


# app = FastAPI(lifespan=mcp301_app.lifespan)
# app = FastAPI(lifespan=mcp891_app.lifespan)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    async with mcp119_app.lifespan(app), mcp459_app.lifespan(app), mcp555_app.lifespan(app):
        yield

app = FastAPI(lifespan=lifespan)

app.mount("/mcp-user119", mcp119_app)
app.mount("/mcp-user459", mcp459_app)
app.mount("/mcp-user555", mcp555_app)

# if __name__ == "__main__":
#     app.run(transport="http",
#             host="127.0.0.1",
#             port=4205,)