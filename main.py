import uvicorn
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from starlette.applications import Starlette
from starlette_apispec import APISpecSchemaGenerator

from db.db import create_database
from middleware import middleware
from src.routes import routes

app = Starlette(routes=routes, middleware=middleware)

schemas = APISpecSchemaGenerator(
    APISpec(
        title="Example API",
        version="1.0",
        openapi_version="3.0.0",
        info={"description": "explanation of the api purpose"},
        plugins=[MarshmallowPlugin()],
    )
)

@app.route("/schema", methods=["GET"], include_in_schema=False)
def schema(request):
    return schemas.OpenAPIResponse(request=request)


if __name__ == "__main__":
    create_database()
    uvicorn.run("main:app", port=5000, log_level="info")
