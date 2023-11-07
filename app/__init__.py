from flask import Flask, render_template, request, session, redirect, url_for, make_response, abort, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = '123'

from app.controlers.default import *