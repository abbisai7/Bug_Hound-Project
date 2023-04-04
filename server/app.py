from flask import Flask,g,request,render_template,session
import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = "ThisisSecret!"


def connect_db():
    sql = sqlite3.connect('C:\\Users\\029421793\\Bughound_Project\\server\\db\\bughound.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,"sqlite3"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = str(request.form['username'])
        password = str(request.form['password'])
        db = get_db()
        query = 'SELECT * FROM employees WHERE username = "{0}" and password ="{1}"'.format(username,password)
        cur = db.execute(query)
        account = cur.fetchall()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]["emp_id"]
            session['username'] = account[0]["username"]
            session['user_level'] = account[0]["userlevel"]
            condition = False
            if session['user_level']==3:
                condition=True
            return render_template('index.html',condition=condition,name=session["username"],userlevel=session["user_level"])
        else:
            return render_template("login.html",msg="True")
    return render_template('login.html')
@app.route("/add_bug")
def add_bug():
    return render_template("add_bug.html")

@app.route("/database_maintenance")
def database_maintenance():
    return render_template("database_maintenance.html")

@app.route("/update_bug")
def update_bug():
    return render_template("update_bug.html")
    
#Employee Functions
#add employee
@app.route("/add_employee",methods=["GET","POST"])
def add_employee():
    if "loggedin" not in session:

        return render_template("login.html")
    inp = request.get_json()
    name = inp["name"]
    username = inp["username"]
    password = inp["password"]
    user_level = inp["user_level"]
    db=get_db()
    db.execute('insert into employees (name,username,password,userlevel) values(?,?,?,?)',[name,username,password,user_level] )
    db.commit()
    return inp

#Update Employee
@app.route("/update_employee",methods=["POST"])
def update_employee():
    inp = request.get_json()
    emp_id = inp["emp_id"]
    inp.pop("emp_id")
    update_stmts = []
    for key, value in inp.items():
        if isinstance(value,int):
           update_stmts.append(f"{key} = {value}") 
        else:
            update_stmts.append(f"{key} = '{value}'")
    
    update_query = f"UPDATE employees SET {', '.join(update_stmts)} WHERE emp_id = {emp_id}"
    print(update_query)
    db = get_db()
    db.execute(update_query)
    db.commit()

    return "employee data updated Successfully"

#delete Employee
@app.route("/delete_employee",methods=["POST"])
def delete_employee():
    inp = request.get_json()
    emp_id = inp["emp_id"]
    db=get_db()
    db.execute('delete from employees where emp_id={0}'.format(emp_id))
    db.commit()

    return "employee deletd successfully"


#add programs
@app.route("/add_program",methods=["GET","POST"])
def add_program():
    db=get_db()
    cur = db.execute('select * from programs')
    programs = cur.fetchall()
    if request.method == "GET":
        return render_template("add_programs.html",programs=programs,conditon="False")
    program = request.form['program']
    program_release = request.form["program_release"]
    program_version = request.form["program_version"]
    db.execute('insert into programs (program,program_release,program_version) values(?,?,?)',[program,program_release,program_version] )
    db.commit()
    cur = db.execute('select * from programs')
    programs = cur.fetchall()
    return render_template("add_programs.html",programs=programs,condition="True",program=program,\
                           release=program_release,version=program_version)

#Update Program
@app.route("/update_program",methods=["POST"])
def update_program():
    inp = request.get_json()
    prog_id = inp["prog_id"]
    inp.pop("prog_id")
    update_stmts = []
    for key, value in inp.items():
        if isinstance(value,int):
           update_stmts.append(f"{key} = {value}") 
        else:
            update_stmts.append(f"{key} = '{value}'")
    
    update_query = f"UPDATE programs SET {', '.join(update_stmts)} WHERE prog_id = {prog_id}"
    db = get_db()
    db.execute(update_query)
    db.commit()

    return "program data updated Successfully"

#delete programs
@app.route("/delete_program",methods=["POST"])
def delete_program():
    inp = request.get_json()
    prog_id = inp["prog_id"]
    db=get_db()
    db.execute('delete from programs where prog_id={0}'.format(prog_id))
    db.commit()

    return 

#add areas
@app.route("/add_area",methods=["GET,POST"])
def add_area():
    if request.method == "GET":
        return render_template('add_area.html')
    inp = request.get_json()
    prog_id = inp["prog_id"]
    area = inp["area"]
    db=get_db()
    db.execute('insert into areas (prog_id,area) values(?,?)',[prog_id,area] )
    db.commit()
    return inp

#Update Area
@app.route("/update_area",methods=["POST"])
def update_area():
    inp = request.get_json()
    area_id = inp["area_id"]
    inp.pop("area_id")
    update_stmts = []
    for key, value in inp.items():
        if isinstance(value,int):
           update_stmts.append(f"{key} = {value}") 
        else:
            update_stmts.append(f"{key} = '{value}'")
    
    update_query = f"UPDATE areas SET {', '.join(update_stmts)} WHERE area_id = {area_id}"
    db = get_db()
    db.execute(update_query)
    db.commit()

    return "program data updated Successfully"

#delete area
@app.route("/delete_area",methods=["POST"])
def delete_area():
    inp = request.get_json()
    area_id = inp["area_id"]
    db=get_db()
    db.execute('delete from areas where prog_id={0}'.format(area_id))
    db.commit()

    return "delted successfully"

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)

