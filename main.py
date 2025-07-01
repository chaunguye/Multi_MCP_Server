from user_mcp_server.user_retrieve_user301 import mcp301
from user_mcp_server.user_retrieve_user891 import mcp891

from fastmcp import FastMCP
from fastapi import FastAPI


mcp301_app = mcp301.http_app(path='/mcp')
mcp891_app = mcp891.http_app(path='/mcp')

# app = FastAPI(lifespan=mcp301_app.lifespan)
# app = FastAPI(lifespan=mcp891_app.lifespan)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    async with mcp301_app.lifespan(app), mcp891_app.lifespan(app):
        yield

app = FastAPI(lifespan=lifespan)

app.mount("/mcp-user301", mcp301_app)
app.mount("/mcp-user891", mcp891_app)

# if __name__ == "__main__":
#     app.run(transport="http",
#             host="127.0.0.1",
#             port=4205,)