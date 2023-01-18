import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, session
from datetime import datetime
from werkzeug.exceptions import abort
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    connection.close()

    app.logger.info("Status Okay")
    return post


# Define the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

# sqllite 3 does not allow for database connections to be counted.
# counting flask sessions on a page instead.
# Flask by default deletes the sessions when the browser is closed.
def db_connection_count():
    if "db_connections" in session:
        session["db_connections"] = session.get("db_connections") + 1
    else:
        session["db_connections"] = 1
    return f'db_connections {session.get("db_connections")}'


# Define the main route of the web application
@app.route("/")
def index():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    db_connection_count()
    app.logger.info(f"Landing page visited - - {[datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}")
    return render_template("index.html", posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(
            f"404 Request to retrieve non-existent post - - {[datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}"
        )
        return render_template("404.html"), 404
    else:
        db_connection_count()
        app.logger.info(
            f"retrieved '{post['title']}' successfully - - {[datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}"
        )
        return render_template("post.html", post=post)


# Define the About Us page
@app.route("/about")
def about():
    app.logger.info(
        f"About Page request was successful - - {[datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}"
    )
    db_connection_count()
    return render_template("about.html")


# Define the post creation functionality
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            connection.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            connection.commit()
            connection.close()
            db_connection_count()
            app.logger.info(
                f"created '{title}' post successfully - - {[datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}"
            )

            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/healthz", methods=("GET", "POST"))
def healthz():
    # return a 200 status code if the application is healthy with
    # a JSON object stating {result: OK-healthy}
    response = app.response_class(
        response=json.dumps({"result": "OK-Healthy"}), status=200, mimetype="application/json"
    )
    db_connection_count()
    return response


@app.route("/metrics", methods=("GET", "POST"))
def metrics():
    # HTTP endpoint with the Status Code of 200
    # JSON response with the total amount of posts in the DB
    # Total and the total amount of connections to the DB
    connection = get_db_connection()
    count_posts = connection.execute("SELECT count(*) FROM posts")
    results = [tuple(row) for row in count_posts][0]
    count = json.dumps(results[0] + 1)
    connection.close()

    response = app.response_class(
        response=json.dumps({"post_count": count, "db_connection_count": db_connection_count()}),
        status=200,
        mimetype="application/json",
    )
    return response


# start the application on port 3111
if __name__ == "__main__":
    # Capture any Python logs at the DEBUG level.
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port="3111")
