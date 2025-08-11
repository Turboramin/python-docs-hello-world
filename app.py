from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return '<a href="https://www.linkedin.com/in/ramintopfer/" target="_blank">Subdomain takeover by Ramin Töpfer</a>'
