from flask import Flask, render_template, request, redirect,url_for,flash
import os
import mysql.connector
from forms import SignUp

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test123",
    database="nienluan"
)
print(mydb)

secrect_key = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = secrect_key

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = str(request.form['user'])
        email = str(request.form['email'])
        password = str(request.form['pass'])

        cursor = mydb.cursor()
        cursor.execute('select * from user;')
        rs = cursor.fetchall()
        l = []
        for r in rs:
            l.append(r[0])
        if username not in l:
            flash("Tài khoản không tồn tại","error")
            return redirect(url_for('home'))
        else:
            flash(f"Chào mừng {username}")
            return redirect(url_for('homebase'))
    return render_template("login.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = str(request.form['user'])
        email = str(request.form['email'])
        password = str(request.form['pass'])
        
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from user;')
        rs = cursor.fetchall()
        l = []
        for r in rs:
            l.append(r[0])
        if username not in l:
            print(l)
            cursor.execute('insert into user values(%s,%s,%s);',(username,email,password))
            cursor.execute("select * from user;")
            rs = cursor.fetchall()
            for r in rs:
                print(r)
            mydb.commit()
            s = f'bạn vừa tạo tài khoản thành công cho  {username} '
            flash(s)
            return redirect(url_for('home'))
        else:
            flash("Tài khoản đã tồn tại","error")
            return redirect(url_for('home'))
        
    return render_template("signup.html")

@app.route('/homebase')
def homebase():
    return render_template("homebase.html")


if __name__ == "__main__":
    app.run(debug=True,port=8080)