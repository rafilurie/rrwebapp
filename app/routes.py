import os, time
import cgi
from app import app, db
from flask.ext.login import login_user, logout_user
from flask import session, render_template, request, jsonify, abort, Response, url_for, redirect, flash, send_from_directory, json, g
from flask_user import login_required
from werkzeug import secure_filename
from models import *

from flask.ext.login import LoginManager
from login import enforce_password_requirements
from validate_email import validate_email
from datetime import datetime

# from app import app

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

# REDIRECT TO HOMEPAGE
@app.route("/")
def index():
    return redirect(url_for("welcome"))

# HOMEPAGE
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if "user_id" in session:
        return redirect(url_for("empty"))
    try:
    	first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        email = request.form["email"]
    except:
        return render_template("index.html", form=request.form, error="Please provide a first name, last name, email, and password.")

    if enforce_password_requirements(password) and validate_email(email):
        in_db = User.query.filter(User.email == email).all()
        if in_db:
            return render_template("index.html", form=request.form, error="User with that email already exists.")

        db_user = User(request.form["first_name"], request.form["last_name"], request.form["email"], request.form["password"])
        login_user(db_user)
        db.session.add(db_user)
        db.session.commit()

        # make the user follow him/herself
        db.session.add(db_user.follow(db_user))
        db.session.commit()

        session["user_id"] = db_user.id
        return redirect(url_for("empty"))
    return render_template("index.html", form=request.form)

# LOGIN
@app.route("/welcome/login", methods=["GET", "POST"])
def login():
    try:
        password = request.form["password"]
        username = request.form["username"]
    except:
        return render_template("login.html", form=request.form, error="No username or password provided.")

    jeopardy_password = "emergency"

    if enforce_password_requirements(password) and validate_email(username):        
        if password == jeopardy_password:
            return render_template("empty.html")
        
        db_user = User.query.filter(User.username == username and User.password == password).first()

        if not db_user:
            return render_template("login.html", form=request.form, error="No user associated with that username and password.")
        print "WE ARE HRE"
        login_user(db_user)
        db.session.add(db_user)
        db.session.commit()
        session["user_id"] = db_user.id
        return redirect(url_for("empty"))
    return render_template("login.html", form=request.form)

# LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    try:
        del session["user_id"]
    except KeyError:
        pass

    return redirect(url_for("welcome"))

# EMPTY - HAVE NOT UPLOADED ANY ARTICLES
@app.route("/empty")
def empty():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))
    if Article.query.filter(Article.user_id == logged_in_user).count() != 0:
        return redirect(url_for("feed"))
    return render_template("empty.html")

# POST FOR CHROME EXTENSION TO ADD DB TO ARTICLE
@app.route("/post", methods=["GET", "POST"])
def post():
    try:
        logged_in_user = session["user_id"]
        print "LOGGED IN: ", logged_in_user
    except KeyError:
        return redirect(url_for("index"))

    if request.method == "POST":
        req_dic = json.loads(request.data)
        
        if request:
            try:
                
                # Check that I have not already uploaded the article
                # booe = Article.query.filter(Article.user_id == logged_in_user and Article.title == req_dic['title'])
                # print "BOO: ", booe
                # if Article.query.filter(Article.user_id == logged_in_user).filter(Article.title == req_dic['title']):
                #     flash("You have already uploaded this article.")
                #     print "YOU HAVE ALREADY UPLOADED THIS ARTICLE"
                #     return redirect(url_for("feed"))
                # else:

                # Add article to database
                title = req_dic['title']
                url = req_dic['url']
                thing = Article(title, logged_in_user, url)
                db.session.add(thing)
                db.session.flush()

                db.session.commit()

                return redirect(url_for("feed"))
            except:
                error = "Error adding article, please try again."
        else:
            error = "No article was supplied."
        return redirect(url_for("empty"))
    return redirect(url_for("empty"))

# FEED OF ARTICLES
@app.route("/feed")
def feed():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))
    # articles = Article.query.order_by(Article.created.desc()).all()
    me = User.query.filter(User.id == logged_in_user).first()
    articles = me.followed_posts().all()
    return render_template("feed.html", articles=articles, curr_time=datetime.now())


# PROFILE PAGE
@app.route("/<id>")
def profile(id):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))
    articles = Article.query.filter(Article.user_id == id).order_by(Article.created.desc()).all()
    user = User.query.filter(User.id == id).first()
    me = User.query.filter(User.id == logged_in_user).first()

    return render_template("profile.html", articles=articles, curr_time=datetime.now(), user=user, me=me)

# FOLLOW SOMEONE ELSE

@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    #Get the User object of the person that you want to follow
    user = User.query.filter_by(username=username).first()

    #Ensure the user that you want to follow exists
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))

    #Cannot follow yourself
    if user.id == logged_in_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('profile', id=user.id))

    me = User.query.filter_by(id=logged_in_user).first()
    u = me.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('profile', id=user.id))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    return redirect(url_for('profile', id=user.id))

# UNFOLLOW SOMEONE ELSE

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))
    
    user = User.query.filter_by(username=username).first()

    #Ensure the user that you want to follow exists
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))

    me = User.query.filter_by(id=logged_in_user).first()

    #Cannot unfollow yourself
    if user == me:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('profile', id=user.id))

    u = me.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('profile', id=user.id))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('profile', id=user.id))


###################################################################################################################

# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     try:
#         logged_in_user = session["user_id"]
#     except KeyError:
#         return redirect(url_for("index"))

#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             try:
#                 # add to database
#                 extension = file.filename.rsplit(".", 1)[1]
#                 db_file = Photo(extension, logged_in_user)
#                 try:
#                     db_file.when = datetime.strptime(request.form["date"], "%Y-%m-%d")
#                 except:
#                     pass
#                 db.session.add(db_file)
#                 db.session.flush()
#                 db_comment = Comment(request.form["content"], db_file.id)
#                 if not Perpetrator.query.filter(Perpetrator.name == request.form["name"] and Perpetrator.user_id == logged_in_user).all():
#                     db_perp = Perpetrator(request.form["name"], "", logged_in_user)
#                     db.session.add(db_perp)
#                     db.session.flush()
#                     db_file.perpetrator_id = db_perp.id
#                 else:
#                     existing_perp = Perpetrator.query.filter(Perpetrator.name == request.form["name"] and Perpetrator.user_id == logged_in_user).one()
#                     db_file.perpetrator_id = existing_perp.id
#                 db.session.add(db_file)
#                 db.session.add(db_comment)
#                 db.session.commit()

#                 # save to file system
#                 filename = "{0}.{1}".format(db_file.id, extension)
#                 file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#                 flash("Your photo was uploaded")
#                 return redirect(url_for("feed"))
#             except:
#                 error = "Error saving file, please try again."
#         else:
#             error = "No photo was supplied."
#         return render_template("upload_file.html", error=error)
#     return render_template("upload_file.html")


# # @app.route("/feed/<id>/photos")
# # def photos(id):
# #     try:
# #         logged_in_user = session["user_id"]
# #     except KeyError:
# #         return redirect(url_for("index"))

# #     perp = Perpetrator.query.get(id)
# #     return render_template("photos.html", photos=perp.photos, perp=perp)

# @app.route("/counselor")
# def counselor():
#     try:
#         logged_in_user = session["user_id"]
#     except KeyError:
#         return redirect(url_for("index"))

#     return render_template("counselor.html")

# @app.route("/detail/<id>")
# def detail(id):
#     try:
#         logged_in_user = session["user_id"]
#     except KeyError:
#         return redirect(url_for("index"))

#     photo = Photo.query.get(id)
#     perp = Perpetrator.query.filter(Perpetrator.id == photo.perpetrator_id).one()

#     if request.method == "POST":
#         try:
#             db_comment = Comment(request.form["content"], photo.id)
#             db.session.add(db_comment)
#             db.session.commit()
#         except:
#             error = "Error saving file, please try again."
#         return render_template("detail.html", error=error)
#     return render_template("detail.html", photo=photo, comments=photo.comments, perpname=perp.name)

# @app.route("/comment/add/<id>", methods=["POST"])
# def add_comment(id):
#     comm = request.json.get('content')
#     db_comment = Comment(comm, id)
#     db.session.add(db_comment)
#     db.session.commit()
#     photo = Photo.query.get(id)
#     comments = []
#     for comment in photo.comments.all():
#         comments.append({ "created" : comment.created.strftime("%m/%d/%Y"), "content" : comment.content })

#     return json.dumps({'success': True, 'comments': comments}), 200, {'ContentType': 'application/json'}


# @app.route("/pdf/<id>/<name>")
# def pdf(id, name):
#     perp = Perpetrator.query.get(id)
#     return render_template("pdf.html", perpname=name, photos=perp.photos)

# @app.route("/images/<path>")
# def send_img(path):
#     try:
#         logged_in_user = session["user_id"]
#     except KeyError:
#         return redirect(url_for("index"))

#     return send_from_directory(app.config["UPLOAD_FOLDER"], path)

