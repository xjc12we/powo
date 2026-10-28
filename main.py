from flask import Flask,jsonify
import os
app = Flask(__name__)

# 测试接口，AndLua可以GET访问
@app.route("/")
def index():
    return jsonify({"msg":"Slope nest后端正常运行","code":200})

# 示例：获取资源列表接口，你后面可以扩展
@app.route("/api/res")
def get_res():
    data = [
        {"name":"测试资源1","url":"https://xxx"},
        {"name":"测试资源2","url":"https://xxx"}
    ]
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        