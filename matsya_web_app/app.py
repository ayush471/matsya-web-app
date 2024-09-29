
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('matsya.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fishermen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            catch_amount REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catch-data')
def catch_data():
    conn = sqlite3.connect('matsya.db')
    c = conn.cursor()
    c.execute('SELECT * FROM fishermen')
    data = c.fetchall()
    conn.close()
    return render_template('catch_data.html', data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        catch_amount = request.form['catch_amount']
        
        conn = sqlite3.connect('matsya.db')
        c = conn.cursor()
        c.execute("INSERT INTO fishermen (name, location, catch_amount) VALUES (?, ?, ?)", (name, location, catch_amount))
        conn.commit()
        conn.close()

        return redirect(url_for('catch_data'))

    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
