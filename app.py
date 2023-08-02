import csv
import sqlite3
from flask import Flask, render_template, request, jsonify
#import pandas as pd

#df = pd.read_csv('data\LumberFut.csv')
#df.to_sql('LumberFutures', engine, if_exists='replace', index=False)

# create database and table
conn = sqlite3.connect('LumberFutures.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS LumberFutures (Date TEXT, Open REAL, High REAL, Low REAL, Close REAL, AdjClose REAL, Volume REAL)')

# read CSV and insert into database
with open('data\LumberFut.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for row in reader:
        c.execute("INSERT INTO LumberFutures VALUES (?, ?, ?, ?, ?, ?, ?)", row)

conn.commit()
conn.close()

app = Flask(__name__, template_folder="test_template") #Note: by default, "app = Flask(__name__)" is sufficient if you name your HTML folder as "template"

@app.route('/')
def home():
    # get data from database
    connection = sqlite3.connect('LumberFutures.db')
    cur = connection.cursor()
    cur.execute("SELECT Date, Open, High, Low, Close, AdjClose, Volume FROM LumberFutures")
    db_data = cur.fetchall()
    connection.close()
    labelX = [row[0] for row in db_data] #get x-axis data
    valueY = [[row[i] for row in db_data] for i in range(1,7)] #get y-axis data
    # render HTML page with chart
    return render_template('dashboard.html', labels=labelX, values=valueY)

#@app.route('/get_column_data/<column_name>')
#def get_column_data(column_name):
#    conn = sqlite3.connect('LumberFutures.db')
#    cursor = conn.cursor()
#    cursor.execute(f'SELECT Date, {column_name} FROM LumberFutures')
#    data = cursor.fetchall()
#    conn.close()
#    return jsonify(data)

if __name__ == "__main__":
    app.run(debug = True)