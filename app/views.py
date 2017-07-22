#!flask/bin/python
import os
from flask import render_template, flash, abort,redirect, request,g,url_for, session, make_response, jsonify
from app import app_
from flask_googlemaps import GoogleMaps, Map
import MySQLdb

GoogleMaps(app_, key = 'AIzaSyAI-Qv_8HTk3NhCLYbphdWYjyK9OgWhdW8')

def connect_to_cloudsql():
    # Connect using the unix socket located at
    # /cloudsql/cloudsql-connection-name.
    cloudsql_unix_socket = '/cloudsql/'+'euphoric-oath-172818:us-east1:apitestdb'

    db = MySQLdb.connect(
        unix_socket = cloudsql_unix_socket,
        user = 'root',
        passwd = 'hadoop',
        db = 'api_db')

    return db

conn = connect_to_cloudsql()
c = conn.cursor()

@app_.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_.route('/')
@app_.route('/index')
def begin():
    return render_template('base.html')

@app_.route('/entries')
def show_entries():
    c.execute('select id,pname,lat,lon from signals order by id ASC')
    entries = c.fetchall()
    markers = []
    for row in entries[:10]:
        markers.append((row[2],row[3],row[1]))
    mymap = Map(
        identifier = 'view-side',
        lat = markers[5][0],
        lng =  markers[5][1],
        markers = markers
    )
    return render_template('show_entries.html', entries=entries, mymap = mymap)

@app_.route('/add',methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    c.execute("insert into signals (id, pname, lat, lon) \
               values ('%s','%s', '%s','%s')" \
              % (request.form['ID'], request.form['Name'], \
                 request.form['Lat'], request.form['Lon']))
    conn.commit()
    flash('updated')
    return redirect('/entries')

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
            return redirect('/index')
    return render_template('login.html', error=error)

@app_.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('/index')
