from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#reading is done here
@app.route('/')
def index():
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute('select * from data')
	result = c.fetchall()
	return render_template('index.html', icerik=result)


#create
@app.route('/create', methods=['POST'])
def create():
	icerik = request.form['icerik']
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute('insert into data(icerik) values(?)', [icerik])
	conn.commit()
	return redirect(url_for('index'))

#update
@app.route('/update/<int:entry_id>')
def update(entry_id):
	#take from database
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute('select * from data where id = ?', [entry_id])
	result = c.fetchone()
	return render_template('edit.html', icerik=result)


#edit
@app.route('/edit', methods=['POST'])
def edit():
	icerik = request.form['icerik']
	entry_id = request.form['entry_id']
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute('update data set icerik = ? where id = ?', (icerik, entry_id))
	conn.commit()
	return redirect(url_for('index'))

#read
@app.route('/read', methods=['GET'])
def read():
	return 'read'

#delete
@app.route('/delete/<int:entry_id>')
def delete(entry_id):
	#connect db
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute('delete from data where id = ?', [entry_id])
	conn.commit()
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(debug=True)