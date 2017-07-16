#!flask/bin/python
from flask import render_template, flash, abort,redirect, request,g,url_for, session, make_response, jsonify
from app import app_
from .forms import LoginForm
import sqlite3
import MySQLdb

def connect_db():
    conn=sqlite3.connect(app_.config['DATABASE'])
    conn.row_factory = sqlite3.Row #allow column names
    return conn

def get_db():
    if not hasattr(g, 'sqlite_db'): # g means global, aplication context instead of request context
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app_.teardown_appcontext # Its executed every time the application context tears down
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app_.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app_.route('/index')
@app_.route('/')
def show_entries():
    conn = get_db()
    c = conn.cursor()
    c.execute('select * from entries')
    entries = c.fetchall()
    for entry in entries:
        print(entry['author'], entry['body'])
    return render_template('show_entries.html',entries = entries)

@app_.route('/add',methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    conn = get_db()
    c = conn.cursor()
    c.execute('insert into entries values (?,?)',[request.form['author'], request.form['body']])
    conn.commit()
    flash('updated')
    return redirect('/')

@app_.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app_.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app_.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect('/')
    return render_template('login.html', error=error)

@app_.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))




