import streamlit as st
import pickle
import pandas as pd
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user


# Create a flask application
app = Flask(__name__)
 
# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "Test0ntime"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()
 
# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)


# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
 
 
# Initialize app with extension
db.init_app(app)
# Create database within app context
 
with app.app_context():
    db.create_all()

# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
# If the user made a POST request, create a new user
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		# Add the user to the database
		db.session.add(user)
		# Commit the changes made
		db.session.commit()
		# Once user account created, redirect them
		# to login route (created later on)
		return redirect(url_for("login"))
	# Renders sign_up template if user made a GET request
	return render_template("sign.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	# If a post request was made, find the user by 
	# filtering for the username
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		# Check if the password entered is the 
		# same as the user's password
		if user.password == request.form.get("password"):
			# Use the login_user method to log in the user
			login_user(user)
			return redirect(url_for("home"))
		# Redirect the user back to the home
		# (we'll create the home route in a moment)
	return render_template("login.html")

@app.route("/")
def home():
	# Render index.html on "/" route, this is where we have recommendations
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
	
def fetch_poster(song_id):
    response = requests.get()
    data = response.json()
    return 



def recommend(song):
    song_index = songs[songs['song_title'] == song].index[0]
    distances = cosine[song_index]
    songs_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]

    recommended_music = []
    for i in songs_list:
        song_id = songs.iloc[i[0]].song_id
        #fetch music from API
        recommended_music.append(songs.iloc[i[0]].song_title)
    return recommended_music

top_songs = pickle.load(open('songs_dict.pkl','rb'))
songs = pd.DataFrame(top_songs)

cosine = pickle.load(open('similarity.pkl','rb'))

st.title('TuneTeller - Music Recommender System')

selected_song_name = st.selectbox(
    'How would you like to be contacted?',
songs['song_title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_song_name)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")
    with col3:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
   
    for i in recommendations:
        st.write(i)
 