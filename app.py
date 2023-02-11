# Sources:
#
# (1) "flask-starter-app", mlapresta, Andrew Kamand, https://github.com/osu-cs340-ecampus/flask-starter-app
#   - Scope: Every route below.
#   - Date: First instance of using the code started on 10/08/2022.
#   - Originality: Our code/approach was based on this source, but it deviated materially 
#       as we learned additional techniques via trial and error. 
#
# (2) "how to safely generate a SQL LIKE statement using python db-api", StackOverflow, 
#   https://stackoverflow.com/questions/2097475/how-to-safely-generate-a-sql-like-statement-using-python-db-api
#   - Scope: The where statement in the movies_filtered route.
#   - Date: 11/15/2022
#   - Originality: Our code/approach was based on this source.

from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request

app = Flask(__name__)
mysql = MySQL(app)

###################################################################################################################################
#                                                   Database and port info                                                        #
###################################################################################################################################

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config['MYSQL_USER'] = 'cs340_hrenkom'
app.config['MYSQL_PASSWORD'] = '6070'
app.config['MYSQL_DB'] = 'cs340_hrenkom'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

portNbr = 17818

###################################################################################################################################
#                                               READ Operation for index Entity                                                  #
###################################################################################################################################

# Route to index page when user enters URL without a path name
@app.route("/")
def home():
    return redirect("/index")

# Get route for index page
@app.route("/index", methods=["GET"])
def index():
    query = "SELECT DISTINCT movie_id, movie_name FROM movies ORDER BY movie_id"
    cur = mysql.connection.cursor()
    cur.execute(query)
    movie_list = cur.fetchall()

    # Render index page and pass the movie_list data (used in dropdown select)
    return render_template("index.j2", movie_list=movie_list)

###################################################################################################################################
#                                               CRUD Operations for movies Entity                                                 #
###################################################################################################################################

# Get and insert routes for movies page
@app.route("/movies", methods=["POST", "GET"])
def movies():

    if request.method == "POST":

        if request.form.get("Add_Movie"):

            movie_name = request.form["movie_name"] 
            movie_year_released = request.form["movie_year_released"]
            movie_language = request.form["movie_language"]
            director_id = request.form["director_id"] 

            # Insert a movie into movies
            try:
                
                if director_id == "":
                    query = "INSERT INTO movies (movie_name, movie_year_released, movie_language) VALUES (%s, %s, %s)"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (movie_name, movie_year_released, movie_language))
                    mysql.connection.commit()
                        
                else:
                    query = "INSERT INTO movies (movie_name, movie_year_released, movie_language, director_id) VALUES (%s, %s, %s, %s)"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (movie_name, movie_year_released, movie_language, director_id))
                    mysql.connection.commit()

                # Render movies page after insert.
                return redirect("/movies")   

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":

        # Select all movies
        query1 = "SELECT \
                movies.movie_id, \
                movies.movie_name, \
                movies.movie_year_released, \
                movies.movie_language, \
                directors.director_name \
                FROM \
                movies LEFT JOIN directors ON \
                movies.director_id = directors.director_id \
                ORDER BY \
                movies.movie_id"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select all directors for dropdown select
        query2 = "SELECT DISTINCT director_id, director_name FROM directors ORDER BY director_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        director_list_data = cur.fetchall()

        # Render movies page and pass the movie list data.
        return render_template("movies.j2", data=data, director_list=director_list_data)

# Filtered movies route for movies_filtered page
@app.route("/movies_filtered", methods=["POST"])
def movies_filtered():

        movie_name = request.form["movie_name"]
        
        # Select movies that match the passed movie_name (exact match)
        query = "SELECT \
        movies.movie_id, \
        movies.movie_name, \
        movies.movie_year_released, \
        movies.movie_language, \
        directors.director_name \
        FROM \
        movies LEFT JOIN directors ON \
        movies.director_id = directors.director_id \
        WHERE movies.movie_name LIKE '%s' " % ('%' + movie_name + '%')
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # If the query returns no data, render the movies page.
        # Add message notifying user.
        if len(data) == 0:
            return redirect("/movies")
        else:
            # Render movies_filtered page and pass the movie list data.
            return render_template("movies_filtered.j2", data=data)

# Edit route for movies page
@app.route("/edit_movie/<int:movie_id>", methods=["POST", "GET"])
def edit_movie(movie_id):

    if request.method == "GET":

        # Select the movie with this movie_id
        query1 = "SELECT \
        movies.movie_id, \
        movies.movie_name, \
        movies.movie_year_released, \
        movies.movie_language, \
        directors.director_name \
        FROM \
        movies LEFT JOIN directors ON \
        movies.director_id = directors.director_id \
        WHERE movies.movie_id = %s" % (movie_id)
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select all directors (but selected) for dropdown select
        query2 = "SELECT DISTINCT director_id, director_name FROM directors ORDER BY director_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        director_list_data = cur.fetchall()

        # Select the director for this movie_id
        query3 = "SELECT \
        directors.director_id, \
        directors.director_name \
        FROM \
        directors INNER JOIN movies ON \
        directors.director_id = movies.director_id \
        WHERE movies.movie_id = %s" % (movie_id)
        cur = mysql.connection.cursor()
        cur.execute(query3)
        director_selected = cur.fetchall()

        # Render edit_movie page and pass the movie and director data
        return render_template("edit_movie.j2", data=data, director_list=director_list_data, director_selected=director_selected)

    if request.method == "POST":

        if request.form.get("Edit_Movie"):

            movie_id = request.form["movie_id"]
            movie_name = request.form["movie_name"]
            movie_year_released = request.form["movie_year_released"]
            movie_language = request.form["movie_language"]
            director_id = request.form["director_id"]

            try:
                # Edit the movie with this movie_id and director_id is null.
                if director_id == "":
                    query = "UPDATE movies SET movies.movie_name = %s, movies.movie_year_released = %s, movies.movie_language = %s, movies.director_id = NULL WHERE movies.movie_id = %s"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (movie_name, movie_year_released, movie_language, movie_id))
                    mysql.connection.commit()

                # Edit the movie with this movie_id
                else:
                    query = "UPDATE movies SET movies.movie_name = %s, movies.movie_year_released = %s, movies.movie_language = %s, movies.director_id = %s WHERE movies.movie_id = %s"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (movie_name, movie_year_released, movie_language, director_id, movie_id))
                    mysql.connection.commit()

                # Render movies page after edit
                return redirect("/movies")
    
            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for movies page
@app.route("/delete_movie/<int:movie_id>")
def delete_movie(movie_id):

    try:
        # Delete the movie with this movie_id
        query = "DELETE FROM movies WHERE movie_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (movie_id,))
        mysql.connection.commit()

        # Render movies page after delete.
        return redirect("/movies")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for actors Entity                                                 #
###################################################################################################################################

# Get and insert routes for actors page
@app.route("/actors", methods=["POST", "GET"])
def actors():

    if request.method == "POST":

        if request.form.get("Add_Actor"):

            actor_name = request.form["actor_name"] 

            try:
                # Insert an actor into actors
                query = "INSERT INTO actors (actor_name) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (actor_name,))
                mysql.connection.commit()

                # Render actors page after insert.
                return redirect("/actors")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
        
        # Select all actors
        query = "SELECT actor_id, actor_name FROM actors ORDER BY actor_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render actors page and pass the actors list data
        return render_template("actors.j2", data=data)

# Edit route for actors page
@app.route("/edit_actor/<int:actor_id>", methods=["POST", "GET"])
def edit_actor(actor_id):
    if request.method == "GET":

        # Select the actor with this actor_id
        query = "SELECT actor_id, actor_name FROM actors WHERE actor_id = %s" % (actor_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render edit_actor page and pass the actor data
        return render_template("edit_actor.j2", data=data)

    if request.method == "POST":

        if request.form.get("Edit_Actor"):

            actor_id = request.form["actor_id"]
            actor_name = request.form["actor_name"]

            try:
                # Edit the actor with this actor_id
                query = "UPDATE actors SET actors.actor_name = %s WHERE actors.actor_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (actor_name, actor_id))

                mysql.connection.commit()

                # Render actors page after edit
                return redirect("/actors")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for actors page
@app.route("/delete_actor/<int:actor_id>")
def delete_actor(actor_id):
   
    try:
        # Delete the actor with this actor_id
        query = "DELETE FROM actors WHERE actor_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (actor_id,))
        mysql.connection.commit()

        # Render actors page after delete.
        return redirect("/actors")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for directors Entity                                              #
###################################################################################################################################

# Get and insert routes for directors page
@app.route("/directors", methods=["POST", "GET"])
def directors():

    if request.method == "POST":

        if request.form.get("Add_Director"):

            director_name = request.form["director_name"] 

            try:
                # Insert a director into directors
                query = "INSERT INTO directors (director_name) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (director_name,))
                mysql.connection.commit()

                # Render directors page after insert.
                return redirect("/directors")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
        
        # Select all directors
        query = "SELECT DISTINCT director_id, director_name FROM directors ORDER BY director_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render directors page and pass the directors list data
        return render_template("directors.j2", data=data)

# Edit route for directors page
@app.route("/edit_director/<int:director_id>", methods=["POST", "GET"])
def edit_director(director_id):

    if request.method == "GET":

        # Select the director with this director_id
        query = "SELECT director_id, director_name FROM directors WHERE director_id = %s" % (director_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render edit_director page and pass the director data
        return render_template("edit_director.j2", data=data)

    if request.method == "POST":

        if request.form.get("Edit_Director"):

            director_id = request.form["director_id"]
            director_name = request.form["director_name"]

            try:
                # Edit the director with this director_id
                query = "UPDATE directors SET directors.director_name = %s WHERE directors.director_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (director_name, director_id))

                mysql.connection.commit()

                # Render directors page after edit
                return redirect("/directors")
    
            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for directors page
@app.route("/delete_director/<int:director_id>")
def delete_director(director_id):
     
    try:
        # Delete the director with this director_id
        query = "DELETE FROM directors WHERE director_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (director_id,))
        mysql.connection.commit()

        # Render directors page after delete.
        return redirect("/directors")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for genres Entity                                                 #
###################################################################################################################################

# Get and insert routes for genres page
@app.route("/genres", methods=["POST", "GET"])
def genres():

    if request.method == "POST":

        if request.form.get("Add_Genre"):

            genre_name = request.form["genre_name"] 

            try:
                # Insert a genre into genres
                query = "INSERT INTO genres (genre_name) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (genre_name,))
                mysql.connection.commit()

                # Render genres page after insert.
                return redirect("/genres")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
        
        # Select all genres
        query = "SELECT genre_id, genre_name FROM genres ORDER BY genre_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render genres page and pass the genres list data
        return render_template("genres.j2", data=data)

# Edit route for genres page
@app.route("/edit_genre/<int:genre_id>", methods=["POST", "GET"])
def edit_genre(genre_id):
    if request.method == "GET":
        
        # Select the genre with this genre_id
        query = "SELECT genre_id, genre_name FROM genres WHERE genre_id = %s" % (genre_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render edit_genre page and pass the genre data
        return render_template("edit_genre.j2", data=data)

    if request.method == "POST":

        if request.form.get("Edit_Genre"):

            genre_id = request.form["genre_id"]
            genre_name = request.form["genre_name"]

            try:
                # Edit the genre with this genre_id
                query = "UPDATE genres SET genres.genre_name = %s WHERE genres.genre_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (genre_name, genre_id))

                mysql.connection.commit()

                # Render genres page after edit
                return redirect("/genres")
    
            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for genres page
@app.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):

    try:
        # Delete the genre with this genre_id
        query = "DELETE FROM genres WHERE genre_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (genre_id,))
        mysql.connection.commit()

        # Render genres page after delete.
        return redirect("/genres")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for users Entity                                                  #
###################################################################################################################################

# Get and insert routes for users page
@app.route("/users", methods=["POST", "GET"])
def users():

    if request.method == "POST":

        if request.form.get("Add_User"):

            user_first_name = request.form["user_first_name"]
            user_last_name = request.form["user_last_name"]
            user_email = request.form["user_email"]

            try:
                # Insert a user into users
                query = "INSERT INTO users (user_first_name, user_last_name, user_email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (user_first_name, user_last_name, user_email))
                mysql.connection.commit()

                # Render users page after insert.
                return redirect("/users")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
      
        # Select all users
        query = "SELECT user_id, user_first_name, user_last_name, user_email FROM users ORDER BY user_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render users page and pass the users list data
        return render_template("users.j2", data=data)

# Edit route for users page
@app.route("/edit_user/<int:user_id>", methods=["POST", "GET"])
def edit_user(user_id):
    if request.method == "GET":
        
        # Select the user with this user_id
        query = "SELECT user_id, user_first_name, user_last_name, user_email FROM users WHERE user_id = %s" % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render edit_user page and pass the user data
        return render_template("edit_user.j2", data=data)

    if request.method == "POST":

        if request.form.get("Edit_User"):

            user_id = request.form["user_id"]
            user_first_name = request.form["user_first_name"]
            user_last_name = request.form["user_last_name"]
            user_email = request.form["user_email"]

            try:
                # Edit the user with this user_id
                query = "UPDATE users SET users.user_first_name = %s, users.user_last_name = %s, users.user_email = %s WHERE users.user_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (user_first_name, user_last_name, user_email, user_id))

                mysql.connection.commit()

                # Render users after edit
                return redirect("/users")
            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for users page
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    
    try:
        # Delete the user with this user_id
        query = "DELETE FROM users WHERE user_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        mysql.connection.commit()

        # Render users page after delete.
        return redirect("/users")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for movies actors Entity                                          #
###################################################################################################################################

# Get and insert routes for movies_actors page
@app.route("/movies_actors", methods=["POST", "GET"])
def movies_actors():

    if request.method == "POST":

        if request.form.get("Add_Movie_Actor"):

            movie_id = request.form["movie_id"]
            actor_id = request.form["actor_id"]       

            try:
                # Insert a movie_id and actor_id combination into into movies_actors
                query = "INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movie_id, actor_id))
                mysql.connection.commit()

                # Render movies_actors page after insert.
                return redirect("/movies_actors")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
        
        # Select all movie name and actor name combinations
        query1 = "SELECT \
                movies_actors.movie_actor_id, \
                movies.movie_name, \
                actors.actor_name \
                FROM movies_actors \
                INNER JOIN movies ON \
                movies_actors.movie_id = movies.movie_id \
                INNER JOIN actors ON \
                movies_actors.actor_id = actors.actor_id \
                ORDER BY \
                movies_actors.movie_actor_id"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select all movies for dropdown select
        query2 = "SELECT DISTINCT movie_id, movie_name FROM movies ORDER BY movie_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        movie_list_data = cur.fetchall()

        # Select all actors for dropdown select
        query3 = "SELECT DISTINCT actor_id, actor_name FROM actors ORDER BY actor_id"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        actor_list_data = cur.fetchall()

        # Render movies_actors page and pass the movie and actor data
        return render_template("movies_actors.j2", data=data, movie_list=movie_list_data, actor_list=actor_list_data)

# Delete route for movies_actors page
@app.route("/delete_movie_actor/<int:movie_actor_id>")
def delete_movie_actor(movie_actor_id):
    
    try:
        # Delete the movie_id and actor_id combination with this movie_actor_id
        query = "DELETE FROM movies_actors WHERE movie_actor_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (movie_actor_id,))
        mysql.connection.commit()

        # Render movies_actors page after delete.
        return redirect("/movies_actors")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for movies genres Entity                                          #
###################################################################################################################################

# Get and insert routes for movies_genres page
@app.route("/movies_genres", methods=["POST", "GET"])
def movies_genres():

    if request.method == "POST":

        if request.form.get("Add_Movie_Genre"):

            movie_id = request.form["movie_id"]
            genre_id = request.form["genre_id"]

            try:
                # Insert a movie_id and genre_id combination into into movies_genres
                query = "INSERT INTO movies_genres (movie_id, genre_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movie_id, genre_id))
                mysql.connection.commit()

                # Render movies_genres page after insert.
                return redirect("/movies_genres")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":
        
        # Select all movie name and genre name combinations
        query1 = "SELECT \
                movies_genres.movie_genre_id, \
                movies.movie_name, \
                genres.genre_name \
                FROM movies_genres \
                INNER JOIN movies ON \
                movies_genres.movie_id = movies.movie_id \
                INNER JOIN genres ON \
                movies_genres.genre_id = genres.genre_id \
                ORDER BY \
                movies_genres.movie_genre_id"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select all movies for dropdown select
        query2 = "SELECT DISTINCT movie_id, movie_name FROM movies ORDER BY movie_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        movie_list_data = cur.fetchall()

        # Select all genres for dropdown select
        query3 = "SELECT DISTINCT genre_id, genre_name FROM genres ORDER BY genre_id"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        genre_list_data = cur.fetchall()

        # Render movies_genres page and pass the movie and genre data
        return render_template("movies_genres.j2", data=data, movie_list=movie_list_data, genre_list=genre_list_data)

# Delete route for movies_genres page
@app.route("/delete_movie_genre/<int:movie_genre_id>")
def delete_movie_genre(movie_genre_id):

    try:
        # Delete the movie_id and genre_id combination with this movie_genre_id
        query = "DELETE FROM movies_genres WHERE movie_genre_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (movie_genre_id,))
        mysql.connection.commit()

        # Render movies_genres page after delete.
        return redirect("/movies_genres")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               CRUD Operations for users reviews Entity                                          #
###################################################################################################################################

# Get and insert routes for users_reviews page
@app.route("/users_reviews", methods=["POST", "GET"])
def users_reviews():

    if request.method == "POST":

        if request.form.get("Add_User_Review"):

            movie_id = request.form["movie_id"]
            user_id = request.form["user_id"]
            movie_rating = request.form["movie_rating"]

            try:
                # Insert a movie_id, user_id, and movie rating combination into into users_reviews
                query = "INSERT INTO users_reviews (movie_id, user_id, movie_rating) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movie_id, user_id, movie_rating))
                mysql.connection.commit()

                # Render users_reviews page after insert.
                return redirect("/users_reviews")

            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

    if request.method == "GET":

        # Select all movie name, user name, and movie rating combinations
        query1 = "SELECT \
                users_reviews.review_id, \
                movies.movie_name, \
                CONCAT(users.user_first_name,' ', users.user_last_name) AS user_name, \
                users_reviews.movie_rating \
                FROM users_reviews \
                INNER JOIN movies ON \
                users_reviews.movie_id = movies.movie_id \
                INNER JOIN users ON \
                users_reviews.user_id = users.user_id \
                ORDER BY \
                users_reviews.review_id"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select all movies for dropdown select
        query2 = "SELECT DISTINCT movie_id, movie_name FROM movies ORDER BY movie_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        movie_list_data = cur.fetchall()

        # Select all users for dropdown select
        query3 = "SELECT DISTINCT user_id, CONCAT(users.user_first_name,' ', users.user_last_name) AS user_name FROM users ORDER BY user_id"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        user_list_data = cur.fetchall()

        # Render users_reviews page and pass the movie and user data
        return render_template("users_reviews.j2", data=data, movie_list=movie_list_data, user_list=user_list_data)

# Edit route for users_reviews page
@app.route("/edit_user_review/<int:review_id>", methods=["POST", "GET"])
def edit_user_review(review_id):

    if request.method == "GET":
        
        # Select the user review with this review_id
        query = "SELECT \
                users_reviews.review_id, \
                movies.movie_name, \
                CONCAT(users.user_first_name,' ', users.user_last_name) AS user_name, \
                users_reviews.movie_rating \
                FROM users_reviews \
                INNER JOIN movies ON \
                users_reviews.movie_id = movies.movie_id \
                INNER JOIN users ON \
                users_reviews.user_id = users.user_id \
                WHERE users_reviews.review_id = %s"  % (review_id)        
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Render edit_user_review page and pass the user review data
        return render_template("edit_user_review.j2", data=data)

    if request.method == "POST":

        if request.form.get("Edit_User_Review"):

            review_id = request.form["review_id"]
            movie_rating = request.form["movie_rating"]

            try:
                # Edit the user review with this review_id
                query = "UPDATE users_reviews SET users_reviews.movie_rating = %s WHERE users_reviews.review_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movie_rating, review_id))

                mysql.connection.commit()

                # Render users_reviews after edit
                return redirect("/users_reviews")
                
            # Render exception page
            except Exception as e:
                return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

# Delete route for users_reviews page
@app.route("/delete_user_review/<int:review_id>")
def delete_user_review(review_id):
    
    try:
        # Delete the movie_id and user_id combination with this review_id
        query = "DELETE FROM users_reviews WHERE review_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (review_id,))
        mysql.connection.commit()

        # Render users_reviews page after delete.
        return redirect("/users_reviews")

    # Render exception page
    except Exception as e:
        return render_template("500_error.j2", error_nbr = e.args[0], error_msg = str(e.args[1]))

###################################################################################################################################
#                                               READ Operation for movie summary Entity                                          #
###################################################################################################################################

# Get routes for movies_actors page
@app.route("/movie_summary", methods=["POST", "GET"])
def movie_summary():
    
    movie_id = request.form["movie_id"]

    if request.method == "POST":
        
        # Select the movie data from movies with this movie_id
        query1 = "SELECT \
        movies.movie_id, \
        movies.movie_name, \
        movies.movie_year_released, \
        movies.movie_language, \
        directors.director_name \
        FROM \
        movies LEFT JOIN directors ON \
        movies.director_id = directors.director_id \
        WHERE movies.movie_id = %s" % (movie_id)
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # Select the actor data from actors for this movie_id (joining on movies_actors)
        query2 = "SELECT \
        actors.actor_name \
        FROM movies_actors \
        INNER JOIN actors ON \
        movies_actors.actor_id = actors.actor_id \
        INNER JOIN movies ON \
        movies_actors.movie_id = movies.movie_id \
        WHERE movies.movie_id = %s" % (movie_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        actors = cur.fetchall()

        # Select the genre data from genres for this movie_id (joining on movies_genres)
        query3 = "SELECT \
        genres.genre_name \
        FROM movies_genres \
        INNER JOIN genres ON \
        movies_genres.genre_id = genres.genre_id \
        INNER JOIN movies ON \
        movies_genres.movie_id = movies.movie_id \
        WHERE movies.movie_id = %s" % (movie_id)
        cur = mysql.connection.cursor()
        cur.execute(query3)
        genres = cur.fetchall()

        # Select the user review data from users_reviews for this movie_id.
        query4 = "SELECT \
                CONCAT(users.user_first_name,' ', users.user_last_name) AS user_name, \
                users_reviews.movie_rating \
                FROM users_reviews \
                INNER JOIN users ON \
                users_reviews.user_id = users.user_id \
                WHERE users_reviews.movie_id = %s"  % (movie_id)        
        cur = mysql.connection.cursor()
        cur.execute(query4)
        reviews = cur.fetchall()

    # Render movie_summary page and pass the movie, actor, genre, and user review data.
    return render_template("movie_summary.j2", data=data, actors=actors, genres=genres, reviews=reviews)

###################################################################################################################################
#                                                           Run the app                                                           #
###################################################################################################################################

if __name__ == "__main__":
    app.run(port=portNbr, debug=True)