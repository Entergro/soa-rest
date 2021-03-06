from fastapi import FastAPI
import os

from starlette.staticfiles import StaticFiles
import image
import models
import user
from db import engine

basedir = os.path.abspath(os.path.dirname(__file__))
models.Base.metadata.create_all(bind=engine)
# Create the connexion application instance

# Get the underlying Flask app instance
app = FastAPI()

app.include_router(user.router)
app.include_router(image.router)
if not os.path.exists('./images'):
    os.mkdir('./images', 0o777)
app.mount("/images", StaticFiles(directory="images"), name="images")
if not os.path.exists('./pdf'):
    os.mkdir('./pdf', 0o777)
app.mount("/pdf", StaticFiles(directory="pdf"), name="pdf")


