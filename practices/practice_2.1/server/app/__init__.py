from flask import Flask

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

from app.views import index
from app.views import configure_routing