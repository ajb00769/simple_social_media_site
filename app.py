from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from cs50 import SQL
from better_profanity import profanity

# took most of these from pset9 finance, heavily inspired by how it was constructed in the app config and session

app = Flask(__name__)
app.secret_key = "this is just a test"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
logins = SQL("sqlite:///logins.db")


# taken from pset9 finance

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# also take nfrom pset9

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():

    # creates a local "error" variable for this route where it can be accessed if any of the conditionals to display an error message

    error = None

    # if a current session is active, routes user to the active session

    if request.method == "GET" and session.get('logged_in'):
        return redirect(url_for("home"))

    elif request.method == "POST":

        # there 2 forms in the html doc, i took most of the css design from https://www.youtube.com/watch?v=p1GmFCGuVjw&pp=ygUSbG9nIGluIHBhZ2UgZGVzaWdu and added little modifications of my own later on, but the backend was made entirely by me where i took some time researching how to make it work by using the "name" attirbute to pass values in the input boxes, select boxes, etc into the backend for processing

        login_pressed = request.form.get("loginbutton", None)
        register_pressed = request.form.get("registerbutton", None)

        # login_pressed listens if the name="loginbutton" attribute is clicked, when clicked it will return the value of "login" which was set in the html attributes

        if login_pressed == "login":

            # takes inputs from the name attributed items in the form when login button is pressed

            email = request.form.get("em")
            password = request.form.get("pw")

            if not email or not password:
                error = "All fields must be filled"
            else:
                check_login = logins.execute("SELECT * FROM logins WHERE email=?", email)
                returned_login = list(check_login)

                # checks if login credentials are correct, using encryption and hashing as per best practices shared in week9 finance lecture

                if not len(returned_login):
                    error = "Account not found"
                elif email == returned_login[0]['email'] and not check_password_hash(returned_login[0]['password'], password):
                    error = "Wrong Password"
                elif email == returned_login[0]['email'] and check_password_hash(returned_login[0]['password'], password):
                    session["logged_in"] = True
                    session["user_id"] = returned_login[0]['id']
                    return redirect(url_for("home"))

        # same as login above where it listens if the register button is clicked and returns the value "register" if the first condition above is false or if login_pressed returned None from the request.form.get() method, using encryption and hashing as per best practices shared in week9 finance lecture just in case database gets hacked at least there are not plain text passwords, though i think it can be decrypted if someone has the source of the werkzeug module

        elif register_pressed == "register":
            uname = request.form.get("uname-reg")
            email = request.form.get("email-reg")
            password = generate_password_hash(request.form.get("pw-reg"))

            # put in place just in case someone tries to circumvent the "required" attribute of the form

            if not uname or not email or not password:
                error = "All fields must be filled"

            user_count = logins.execute("SELECT COUNT(*) FROM logins")

            # check if email or username already taken

            is_username_taken = logins.execute("SELECT username FROM logins WHERE username=?", uname)
            is_email_taken = logins.execute("SELECT email FROM logins WHERE email=?", email)

            if len(is_username_taken):
                error = "Username already taken"
            elif len(is_email_taken):
                error = "Email already registered"
            else:

                # i didn't use autoincrement in the sql db because at the time i started this before doing pset9 finance and didn't want to go through all the trouble of touching the table

                id_num = 0
                int_user_count = user_count[0]['COUNT(*)']
                id_num = int_user_count

                logins.execute("INSERT INTO logins (id, username, email, password) VALUES (?, ?, ?, ?)",
                               id_num, uname, email, password)
                logins.execute("INSERT INTO profile_info (profile_img_id, user_id) VALUES (?, ?)", 1, id_num)
    return render_template("landing.html", error=error)


@app.route("/home", methods=["POST", "GET"])
@login_required
def home():

    # already has the @login_required decorator but still kept the code below, not sure if it's redunant at this point but it works, i started this part before i did pset9 and i didn't want to change it anymore, might also add an additional layer of security?

    if request.method == "GET" and not session.get('logged_in'):
        return redirect(url_for("login"))
    elif request.method == "POST":
        post_button_pressed = request.form.get("poststatus", None)

        if post_button_pressed == "postclick":
            post_item = request.form["statustext"]
            if len(post_item) > 145:
                error = "Cannot exceed 145 characters."
                flash(error)
                return redirect(url_for("home"))
            elif any(len(post_item) > 30 for post_item in post_item.split()):
                error = "A single word cannot exceed 30 characters."
                flash(error)
                return redirect(url_for("home"))
            else:
                post_id_counter = logins.execute("SELECT COUNT(*) FROM post_ids")
                post_count = int(post_id_counter[0]["COUNT(*)"]) + 1
                print(post_count)
                logins.execute("INSERT INTO post_ids (user_id, post_id, post) VALUES (?, ?, ?)",
                            session["user_id"], post_count, post_item)
                return redirect(url_for("home"))
    elif request.method == "GET" and session.get('logged_in'):

        # if user is logged in this fetches the 10 most recent posts into the feed, this is the default page when someone logs in, the first conditional as stated previously, kicks them back to the login page if they try to access the home page if not logged in

        get_posts = logins.execute("SELECT post, username, img_url FROM post_ids JOIN logins ON logins.id=post_ids.user_id JOIN profile_info ON profile_info.user_id=logins.id JOIN profile_imgs ON profile_imgs.img_id=profile_info.profile_img_id WHERE post_ids.date_posted<=DATETIME('now', 'localtime') ORDER BY post_ids.date_posted DESC LIMIT 10")
        post_feed = []
        for i in range(len(get_posts)):
            post_kvp = {
                'username': get_posts[i]["username"],
                'post': profanity.censor(get_posts[i]["post"]),
                'prof_pic': get_posts[i]["img_url"]
            }
            post_feed.append(post_kvp)
        user_profile = logins.execute("SELECT img_url FROM profile_imgs JOIN profile_info ON profile_info.profile_img_id=profile_imgs.img_id WHERE user_id=?", session["user_id"])
        return render_template("home.html", post_feed=post_feed, profile_pic=user_profile[0]["img_url"])


@app.route("/profile", methods=["GET"])
def profile():

    # a simple user profile page where it fetches the user's bio and previously selected profile image, if none has been selected before OR if they just created the account it defaults into the cs50 cat! :)

    get_prof = logins.execute("SELECT img_url, username, bio FROM profile_imgs JOIN profile_info ON profile_info.profile_img_id=profile_imgs.img_id JOIN logins ON logins.id=profile_info.user_id WHERE user_id=?", session["user_id"])
    return render_template("profile.html", profile_pic=get_prof[0]["img_url"], username=get_prof[0]["username"], user_bio=get_prof[0]["bio"])


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":

        # gets all available profile pics they can choose, i didn't allow the option to upload and instead chose to have a pre-determined list to prevent people from uploading anything explicit or any form of nudity since I don't know how to filter that one out, if I'm not mistaken facebook even hires actual people to moderate content

        get_pic_opts = logins.execute("SELECT img_desc FROM profile_imgs WHERE img_desc NOT LIKE 'mod' AND img_desc NOT LIKE 'administrator'")
        return render_template("settings.html", prof_imgs=get_pic_opts)
    elif request.method == "POST":

        # similar how to the double form login page worked, this listens for a button click which returns the corresponding value and if it evaluates to true it proceeds to execute the specific task for that form

        submit_pic = request.form.get("submitpic", None)
        submit_bio = request.form.get("submitbio", None)

        if submit_pic == "submitpic":

            # got stuck on this one for an hour because of how complicated the relational database/tables became, well relatively complex, for veteran programmers i'm sure this would have been a piece of cake but not for me, hopefully I'll get better though and cut the time to implement down!

            chosen_pic = request.form.get("selectedimg")
            get_img_id = logins.execute("SELECT img_id FROM profile_imgs WHERE img_desc=?", chosen_pic)

            if get_img_id[0]["img_id"] == 6 or get_img_id[0]["img_id"] == 8:
                flash("Invalid input.")
                return redirect(url_for("settings"))
            else:
                logins.execute("UPDATE profile_info SET profile_img_id=? WHERE user_id=?", get_img_id[0]["img_id"], session["user_id"])
                return redirect(url_for("profile"))
        elif submit_bio == "submitbio":
            user_input = request.form.get("bio")

            # i chose this way of limiting characters because i'm not too keen on javascript, i'll spend some time later learning more on that or maybe when i take the cs50 web course after this!

            if len(user_input) > 500:
                flash("Cannot exceed 500 characters")
                return redirect(url_for("settings"))
            else:
                logins.execute("UPDATE profile_info SET bio=? WHERE user_id=?", user_input, session["user_id"])
                return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# requirement for better profanity to work
if __name__ == '__main__':
    profanity.load_censor_words()
    app.run()