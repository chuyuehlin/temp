from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import requests

app = Flask(__name__)


# Index
@app.route('/')
def index():
    return render_template('homepage.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# Register Form Class
class RegisterForm(Form):
    username = StringField('Email (Username)', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate() == False:
			error = 'Passwords do not match'
			return render_template('register.html', form=form,error=error)

		username = form.username.data
		password = form.password.data 
		# Create cursor
		result = requests.post('http://stock-recommender-backend.herokuapp.com/signup/', json={"email": username,"password": password})

		result = result.json()

		if "detail" in result:
			error = result["detail"]
			return render_template('register.html', form=form,error=error)
        
		flash('You are now registered and can log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
        # Get Form Fields
		username = request.form['username']
		password = request.form['password']

		result = requests.post('http://stock-recommender-backend.herokuapp.com/login/', json={"username": username,"password": password})

		result = result.json()

		if "detail" in result:
			error = result["detail"]
			return render_template('login.html', error=error)
		
		session['logged_in'] = True
		session['username'] = username
		flash('You are now logged in', 'success')
		return redirect(url_for('index'))

	return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/quicksearch/<string:song>', methods=['GET', 'POST'])
@is_logged_in
def quicksearch(song):
    if request.method == 'POST':
        song = request.form['Song']
        cur = mysql.connection.cursor()
        sql='Select * from song_records where Performer like %s union Select distinct * from song_records where Song like %s union Select distinct * from song_records where spotify_track_album like %s'
        args=[song+'%',song+'%',song+'%']
        result = cur.execute(sql,args)
        if result > 0:
            data = cur.fetchall()
            return render_template('search.html', songs = data)
        else:
            msg = 'NO SONGS FOUND'
            return render_template('search.html', msg = msg)

    cur = mysql.connection.cursor()
    sql='Select * from song_records where Performer like %s union Select distinct * from song_records where Song like %s union Select distinct * from song_records where spotify_track_album like %s'
    args=[song+'%',song+'%',song+'%']
    result = cur.execute(sql,args)
    if result > 0:
        data = cur.fetchall()
        return render_template('search.html', songs = data)
    else:
        msg = 'NO SONGS FOUND'
        return render_template('search.html', msg = msg)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        song = request.form['Stock']
        searchjson = {"query": {"term": {"symbolId": {"value": song}}}}
        print(searchjson)
        result = requests.post('http://clip3.cs.nccu.edu.tw:9200/chart/_search', json=searchjson)
        result = result.json()
        if result['hits']['total']['value'] != 0:
            return render_template('search.html', songs = result)
        else:
            msg = 'NO STOCKS FOUND'
            return render_template('search.html', error = msg)

        print(result.json())
    return render_template('search.html')

@app.route('/playlist')
@is_logged_in
def playlist():
    # Create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM playlists,song_records WHERE user = %s AND song_records.songID = playlists.recordsongID", [session['username']])
    mysongs = cur.fetchall()

    if result > 0:
        return render_template('playlist.html', mysongs=mysongs)
    else:
        msg = 'No Songs Yet'
        return render_template('playlist.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/addtoPlaylist/<string:song>')
@is_logged_in
def addtoPlaylist(song):

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM playlists WHERE recordsongID = %s", [song])
    if result > 0:
        flash('Song Already in your playlist', 'danger')
        cur.close()
        return redirect(url_for('search'))
    else:

        cur1 = mysql.connection.cursor()
        cur1.execute("INSERT INTO playlists(recordsongID, user) VALUES(%s, %s)", (song, [session['username']]))
        mysql.connection.commit()
        cur1.close()
        cur.close()
        flash('Song Added to your playlist', 'success')
        return redirect(url_for('search'))

@app.route('/removesong/<string:id>')
@is_logged_in
def removesong(id):
    # Create cursor
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM playlists WHERE recordsongID = %s", [id])
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Song Removed From Playlist', 'success')
    return redirect(url_for('playlist'))

class SettingForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
@app.route('/setting', methods=['GET', 'POST'])
@is_logged_in
def setting():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [session['username']])
    detail = cur.fetchone()
    cur.close()
    form = SettingForm(request.form)
    form.name.data = detail['name']
    form.email.data = detail['email']
    if request.method == 'POST' and form.validate():
        print('123')
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute ("UPDATE users SET name=%s, email=%s WHERE username=%s",(name,email,session['username']))
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('Your profile have been updated', 'success')
        return redirect(url_for('index'))
    return render_template('setting.html', form=form)

@app.route('/reccomend')
@is_logged_in
def reccomend():
    cur = mysql.connection.cursor()
    result = cur.execute("WITH avgval AS  ( SELECT AVG(danceability) as avgdance, AVG(energy) as avgenergy, AVG(loudness) as avgloudness, AVG(speechiness) as avgspeech, avg(acousticness) as avgacoustic, avg(liveness) as avglive FROM playlists, song_records WHERE playlists.recordsongID = song_records.SongID AND playlists.user = %s ) SELECT * FROM song_records, avgval WHERE song_records.danceability between avgval.avgdance-0.2 and avgval.avgdance+0.2 and song_records.energy between avgval.avgenergy-0.2 and avgval.avgenergy+0.2 and song_records.loudness between avgval.avgloudness-0.2 and avgval.avgloudness+0.2 and song_records.speechiness between avgval.avgspeech-0.2 and avgval.avgspeech+0.2 and song_records.acousticness between avgval.avgacoustic-0.2 and avgval.avgacoustic+0.2 and song_records.liveness between avgval.avglive-0.2 and avgval.avglive+0.2 LIMIT 15", [session['username']])
    if result > 0:
        data = cur.fetchall()
        return render_template('reccomend.html', songs = data)
    else:
        msg = 'NO SONGS FOUND'
        return render_template('reccomend.html', msg = msg)
    return render_template('reccomend.html')



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
