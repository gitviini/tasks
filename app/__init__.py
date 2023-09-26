from flask import Flask, render_template, request, session, redirect, url_for, make_response, abort, flash
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
app.secret_key = '123'
CORS(app)

from app.controlers.default import *