from flask import Flask,render_template,request, redirect,url_for
import os
from werkzeug.utils import secure_filename
import json

folder_name = "Posts"
os.makedirs(folder_name, exist_ok=True)
app=Flask(__name__)

@app.route("/")
def home():
    files=os.listdir(folder_name)
    posts=[]
    for f in files:
        posts.append(f[:-4])        
    return render_template("home.html",posts=posts)

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if username=="shafey" and password=="111":
            return redirect(url_for("admin_page"))
    return render_template("login_page.html")

@app.route("/admin")
def admin_page():
    files=os.listdir(folder_name)
    posts=[]
    for f in files:
        posts.append(f[:-4])    
    return render_template("admin.html",posts=posts)

@app.route("/post_maker",methods=["POST","GET"])
def post_maker():
    if request.method=="POST":
        heading=request.form.get("heading")
        paragraph=request.form.get("paragraph")
        safe_heading = secure_filename(heading)
        if not safe_heading:
            return render_template(
          "post_maker.html",
          error="Invalid title! Please use alphanumeric characters.",
            )
        filename=f"Posts/{safe_heading}.json"

        file_names = os.listdir("Posts")
        
        safe_heading+=".json"
        if safe_heading in file_names:
            return render_template("post_maker.html", error="A post with this title already exists!")
        with open(filename,"w",encoding="utf-8") as f:
            data={"heading":heading,"paragraph":paragraph}
            json.dump(data,f,indent=4)

    return render_template("post_maker.html")
@app.route("/post_display/<filename>")
def post_display(filename):
    safeTitle= secure_filename(filename)
    filePath=os.path.join(folder_name,f"{safeTitle}.json")
    if not os.path.exists(filePath):
        return "Post not found", 404

    with open(filePath,"r",encoding="utf-8") as f:
       data=json.load(f)


    return render_template("post_display.html",post_data=data)
if __name__== "__main__":
    app.run(debug=True)