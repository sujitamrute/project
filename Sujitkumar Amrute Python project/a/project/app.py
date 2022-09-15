from flask import *
import pymysql

db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "sujit",
    database = "person"
    )

cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    name = "Amit"
    mylist = [10,20,30,40,50]
    return render_template("about.html",username=name,mylist=mylist)

@app.route("/user/<name>")
def user(name):
    return "Hello {}".format(name)

@app.route("/allusers")
def allusers():
    cursor.execute("select * from user")
    data = cursor.fetchall()
    return render_template("allusers.html",userdata=data)

@app.route("/create",methods=["POST"])
def create():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    contact = request.form.get('contact')
    insq = "insert into user(name,password,contact) values ('{}','{}','{}')".format(uname,pwd,contact)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for('allusers')) 
    except:
        db.rollback()
        return "Error in query"

@app.route("/delete")
def delete():    
    id = request.args.get('id')    
    delq = "delete from user where id={}".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for('allusers')) 
    except:
        db.rollback()
        return "Error in query"

@app.route("/edit")
def edit():
    id = request.args.get('id')
    selq ="select * from user where id={}".format(id) 
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template("edit.html",row=data)

@app.route("/update",methods=["POST"])
def update():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    contact = request.form.get('contact')
    uid = request.form.get('uid')
    
    updq ="update user set name='{}',password='{}',contact='{}' where id={}".format(uname,pwd,contact,uid)
    try:
        cursor.execute(updq)
        db.commit()
        return redirect(url_for('alluser')) 
    except:
        db.rollback()
        return "Error in query"



if __name__=="__main__":
    app.run(debug=True)
