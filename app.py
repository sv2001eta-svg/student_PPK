from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    name = request.args.get('nickname')
    return f'{name}, привет!'

# ← ВСТАВИТЬ СЮДА ↑
@app.route("/help")
def help():
    return render_template("help.html")

app.run()