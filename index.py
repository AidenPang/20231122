import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    X = "作者:黃植達 2023-11-22<br>"
    X += "<a href=/db>課程網頁</a><br>"
    X += "<a href=/alex?nick=alex>個人介紹及系統時間</a><br>"
    X += "<a href=/account>表單傳值</a><br>"
    X += "<br><a href=/read>讀取Firestore資料</a><br>"
    X += "<br><a href=/read2>人選之人─造浪者</a><br>"
    X += "<br><a href=/read3>圖書精選</a><br>"
    X += "<br><a href=/search>Search</a><br>"
    return X

@app.route("/db")
def db():
    return "<a href='https://drive.google.com/drive/folders/1JGHLQWpzT2QxSVPUwLxrIdYowijWy4h1'>海青班資料庫管理課程</a>"

@app.route("/alex", methods=["GET", "POST"])
def alex():
    tz = timezone(timedelta(hours=+8))
    now = str(datetime.now(tz))
    #now = str(datetime.now())
    user = request.values.get("nick")
    return render_template("alex.html", datetime=now, name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["user"]
        Result = "Input name : " + keyword

        Result += "<br>"
        db = firestore.client()
        collection_ref = db.collection("人選之人─造浪者")    
        docs = collection_ref.order_by("birth").get()
        for doc in docs:         
            x = doc.to_dict()
            if keyword in x["name"]:
                Result += "Name : " + x["name"] + ", Role : " + x["role"] + ", Birth : " + str(x["birth"]) + "<br>"
        return Result
    else:
        return render_template("search.html")
    
@app.route("/read")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("黃植達")    
    docs = collection_ref.get()
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/read2")
def read2():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.order_by("birth").get()
    for doc in docs:         
        x = doc.to_dict()
        Result += "Name : " + x["name"] + ", Role : " + x["role"] + ", Birth : " + str(x["birth"]) + "<br>"    
    return Result

@app.route("/read3")
def read3():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")    
    docs = collection_ref.order_by("anniversary").get()
    for doc in docs:
        book = doc.to_dict()
        Result += "Title : <a href = " + book["url"] + ">" + book["title"] + "</a><br>"
        Result += "Author : " + book["author"] + "<br>"
        Result += "Anniversary : " + str(book["anniversary"]) + "<br>"
        Result += "<img src = " + book["cover"] + ">" + "</img><br>"
    return Result

#if __name__ == "__main__":
    #app.run()
