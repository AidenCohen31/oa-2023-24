from flask import Flask, request
from flask_cors import CORS
import sqlite3
import os
import json
import codecs

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    con = sqlite3.connect("ascii")
    con.row_factory = sqlite3.Row  
    c = con.cursor() 
    c.execute(""" CREATE TABLE IF NOT EXISTS ASCII (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    X integer NOT NULL,
                    Y integer NOT NULL,
                    sym integer NOT NULL
    )""")
   
    rows = [i["name"] for i in c.execute("""SELECT DISTINCT NAME FROM ASCII""").fetchall()]
    for file in os.listdir("."):
        if file.endswith(".txt") and not file in rows:
            coords = asciiToCoords(file)
            for i in coords:
                c.execute("""INSERT INTO ASCII (name,X,Y,sym) VALUES (?,?,?,?)""", (file,i[0], i[1], i[2]))
                con.commit()
    c.close()
    
    return rows
@app.route("/all", methods=["GET"])
def all():
    con = sqlite3.connect("ascii")
    con.row_factory = sqlite3.Row
    c = con.cursor()
    rows = c.execute("SELECT * FROM ASCII").fetchall()
    c.close()
    return [[i["name"], i["X"], i["Y"], i["sym"]] for i in rows]
@app.route("/name", methods=["GET"])
def getNames():
    con = sqlite3.connect("ascii")
    con.row_factory = sqlite3.Row
    c = con.cursor()
    rows = c.execute("SELECT DISTINCT NAME FROM ASCII").fetchall()
    c.close()
    return [i["name"] for i in rows]

@app.route("/data", methods=["GET"])
def getData():
    con = sqlite3.connect("ascii")
    con.row_factory = sqlite3.Row 
    args = request.args
    c = con.cursor() 
    print(args["name"])
    c.execute(f"""SELECT X,Y,sym FROM ASCII WHERE name=?""", (args["name"],))
    rows = c.fetchall()
    c.close()
    return [[i["X"], i["Y"], i["sym"]] for i in rows]
def asciiToCoords(file):
    coords = []
    rowc = 0
    with codecs.open(file, encoding='utf-8', mode="r") as f:
        while r:= f.readline():
            rowc += 1
            colc = 0
            for i in r:
                coords.append((rowc,colc,i))
                colc += 1
    return coords

if __name__ == "__main__":
    app.run(debug=True)