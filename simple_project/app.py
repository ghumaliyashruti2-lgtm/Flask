import sqlite3

conn = sqlite3.connect("database.db")

#  // hello world //
'''from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)'''
    
    
# // use index file from template folder //
'''from flask import Flask, render_template
app = Flask(__name__) # object 
@app.route("/")
def home():
    return render_template("index.html")'''


# // dynamic url //
'''from flask import Flask, render_template
from flask import request
app = Flask(__name__)
@app.route("/user/<name>") #user/shruti
def user(name):
    return f"Hello {name}" #hello shruti '''

#// dynamic data //
''' @app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        name = request.form["username"]
        return name
    return render_template("index.html")

app.run(debug=True)'''


# // mini website created //

'''from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)'''



# // login register code //

from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

    user = cursor.fetchone()

    conn.close()

    if user:
        session["user"] = username
        return redirect("/dashboard")

    return "Invalid Login"


@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template("dashboard.html", user=session["user"])

    return redirect("/")


@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/")


app.run(debug=True)



# // Todo app //

'''from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"]) # this url set in action value index file . 
def add():

    task = request.form["task"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks(task) VALUES(?)",(task,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/")


app.run(debug=True)'''


# //rest api//

'''from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api")
def api():

    # dictionary 
    data = {
        "name":"Shruti",
        "course":"Python Flask",
        "status":"learning"
    }
    # convert dictionary to json .. 
    return jsonify(data)

# multiple data 
@app.route("/users")
def users():

    users = [
        {"id":1,"name":"Rahul"},
        {"id":2,"name":"Shruti"},
        {"id":3,"name":"Amit"}
    ]

    return jsonify(users)

# api with parameter (indivisual user fetch by id )
@app.route("/user/<int:id>")
def user(id):

    users = {
        1:"Rahul",
        2:"Shruti",
        3:"Amit"
    }

    return {"id":id,"name":users.get(id)}

# //post api //
# (send data: url send in postman post method go to body and json paste data herer click send message show)
from flask import request

@app.route("/adduser", methods=["POST"])
def adduser():

    data = request.json

    name = data["name"]

    return {"message":f"{name} added successfully"}
app.run(debug=True)'''
