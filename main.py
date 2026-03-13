from flask import Flask, render_template, jsonify, request
import secrets
import json
import logging
import time
import functools

logging.basicConfig (
    filename= "keys.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app = Flask(__name__)

@app.route("/")
def home() :
    return render_template("index.html")

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) :
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f"generated_key ran in {end - start:.4f} seconds")
        return result
    return wrapper

@timer
@app.route("/generate", methods=["POST"])
def generate_key() :
    key = secrets.token_hex(32)
    with open("store.json", 'r+', encoding='utf-8') as f :
        data = json.load(f)
        data.append(key)
        f.seek(0)
        json.dump(data, f)
    logging.info(f"new generated key : {key}")
    return jsonify({"api_key" : key})



if __name__ == "__main__" :
    app.run(debug= True)