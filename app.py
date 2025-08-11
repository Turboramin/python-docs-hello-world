from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return 'PoC by Ramin Topfer (<a href="https://www.linkedin.com/in/ramintopfer/" target="_blank">LinkedIn</a>)'
    
