from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
DATA_FILE = "user.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return "✅ 服务正常运行！接口：/api/getUserInfo  /api/uploadUserInfo"

@app.route('/api/uploadUserInfo', methods=["POST"])
def uploadUserInfo():
    data = request.get_json()
    nick = data.get("nick")
    sign = data.get("sign")
    res_list = data.get("res_list", [])
    if not nick:
        return jsonify({"code":400,"msg":"昵称不能为空"}),400
    user_data = load_data()
    user_data["info"] = {
        "nick": nick,
        "sign": sign,
        "res_list": res_list
    }
    save_data(user_data)
    return jsonify({"code":200,"msg":"上传成功"})

@app.route('/api/getUserInfo', methods=["GET"])
def getUserInfo():
    user_data = load_data()
    info = user_data.get("info", {})
    return jsonify({"code":200,"data": info})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
