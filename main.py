from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 开启全部跨域，AndLua直接访问

# 数据库文件
DB_FILE = "database.json"

# 初始化数据库文件
def init_db():
    if not os.path.exists(DB_FILE):
        init_data = {
            "resources": [
                {"id": 1, "name": "测试资源1", "url": "https://xxx.example.com/file1", "desc": "示例资源"},
                {"id": 2, "name": "测试资源2", "url": "https://xxx.example.com/file2", "desc": "示例资源2"}
            ],
            "users": []
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(init_data, f, ensure_ascii=False, indent=2)

# 读取数据库
def read_db():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 写入数据库
def write_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

init_db()

# 根接口，检测服务是否在线
@app.route("/", methods=["GET"])
def index():
    return jsonify({"code": 200, "msg": "Slope nest API 正常运行"})

# 获取资源列表接口
@app.route("/api/res", methods=["GET"])
def get_resource():
    db = read_db()
    return jsonify({"code":200, "data": db["resources"]})

# 提交用户信息（昵称、签名）
@app.route("/api/user/save", methods=["POST"])
def save_user():
    db = read_db()
    nick = request.form.get("nick")
    sign = request.form.get("sign")
    if not nick:
        return jsonify({"code":400, "msg":"昵称不能为空"})
    # 简单去重，相同昵称覆盖
    exist = False
    for u in db["users"]:
        if u["nick"] == nick:
            u["sign"] = sign
            exist = True
            break
    if not exist:
        db["users"].append({"nick":nick, "sign":sign})
    write_db(db)
    return jsonify({"code":200, "msg":"用户信息保存成功"})

# 查询用户信息
@app.route("/api/user/get", methods=["GET"])
def get_user():
    nick = request.args.get("nick")
    db = read_db()
    for u in db["users"]:
        if u["nick"] == nick:
            return jsonify({"code":200, "data":u})
    return jsonify({"code":404, "msg":"用户不存在"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
