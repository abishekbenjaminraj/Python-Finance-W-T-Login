from flask import Flask,render_template,request,redirect,url_for
import requests
import sqlite3 as sql

app = Flask(__name__)


bank = "https://api.mfapi.in/mf/"


@app.route('/')
def home():
    list_1 = []
    con = sql.connect("table.db")
    cur = con.cursor()
    cur.execute("select * from student")
    fet = cur.fetchall()
    for i in fet:
        id = i[0]
        name = i[1]
        funds = i[2]
        inves = i[3]
        units = i[4]
        completeurl = requests.get(bank + str(funds))
        dict_1 = {}
        dict_1["SNO"] = id
        dict_1["Name"] = name
        dict_1["Fundname"] = completeurl.json().get("meta").get("fund_house")
        dict_1["Invested"] = inves
        dict_1["Unitsheld"] = units
        dict_1["Nav"] = completeurl.json().get("data")[0].get("nav")
        dict_1["Currentvalue"] = float(dict_1.get("Nav"))*dict_1.get("Invested")
        dict_1["Growth"] = float(dict_1.get("Currentvalue"))-dict_1.get("Unitsheld")
        list_1.append(dict_1)
    return render_template ("index.html", box = list_1)

@app.route('/insert', methods = ["GET","POST"])
def insert():
    if request.method == "POST":
        con = sql.connect("table.db")
        cur = con.cursor()
        cur.execute("insert into student (Name,Funds,Invested_Amount,Units_Held) values (?,?,?,?)",
                    (request.form.get("name"),request.form.get("funds"),
                    request.form.get("inves"),request.form.get("units")))
        con.commit()
        return redirect(url_for("home"))
    return render_template ("add.html")

@app.route('/edit/<string:id>', methods = ["GET","POST"])
def edit(id):
    if request.method == "POST":
        con = sql.connect("table.db")
        cur = con.cursor()
        cur.execute("update student set Name=?,Funds=?,Invested_Amount=?,Units_Held=? where ID=?",
                    (request.form.get("name"),request.form.get("funds"),
                    request.form.get("inves"),request.form.get("units"),id))
        data = cur.fetchall()
        con.commit()
        return redirect(url_for("home"))
    conn=sql.connect("table.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from student where ID=?",(id,))
    data=cur.fetchone()
    return render_template ("edit.html",bag=data)

@app.route('/delete/<string:id>')
def delete(id):
    con = sql.connect("table.db")
    cur = con.cursor()
    cur.execute("delete from student where ID=?",(id,))
    con.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)