-- Class: CS 340
-- Group: 61 - Wonderlust
-- Students: Allysa Foot, Michael Hrenko
-- Project Name: Movie Night
-- URL: http://flip3.engr.oregonstate.edu:17818/index
-- This file corresponds to the CS340 Portfolio Project deliverables.

-- Create the tables and populate them with sample data. 

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS movies_actors;
DROP TABLE IF EXISTS movies_genres;
DROP TABLE IF EXISTS users_reviews;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS directors;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS movies (
	movie_id INT NOT NULL AUTO_INCREMENT,
	movie_name VARCHAR(250) NOT NULL UNIQUE,
	movie_year_released YEAR(4) NOT NULL,
	movie_language VARCHAR(250) NOT NULL,
	director_id INT NULL,
	PRIMARY KEY (movie_id),
	FOREIGN KEY (director_id) REFERENCES directors (director_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS actors (
	actor_id INT NOT NULL AUTO_INCREMENT,
	actor_name VARCHAR(250) NOT NULL UNIQUE,
	PRIMARY KEY (actor_id)
);

CREATE TABLE IF NOT EXISTS directors (
	director_id INT NOT NULL AUTO_INCREMENT,
	director_name VARCHAR(250) NOT NULL UNIQUE,
	PRIMARY KEY (director_id)
);

CREATE TABLE IF NOT EXISTS genres (
	genre_id INT NOT NULL AUTO_INCREMENT,
	genre_name VARCHAR(250) NOT NULL UNIQUE,
	PRIMARY KEY (genre_id)
);

CREATE TABLE IF NOT EXISTS users (
	user_id INT NOT NULL AUTO_INCREMENT,
	user_first_name VARCHAR(250) NOT NULL,
	user_last_name VARCHAR(250) NOT NULL,
	user_email VARCHAR(250) NOT NULL UNIQUE,
	PRIMARY KEY (user_id),
    UNIQUE(user_first_name, user_last_name)
);

CREATE TABLE IF NOT EXISTS movies_actors (
	movie_actor_id INT NOT NULL AUTO_INCREMENT,
	movie_id INT NOT NULL,
	actor_id INT NOT NULL,
	PRIMARY KEY (movie_actor_id),
	FOREIGN KEY (actor_id) REFERENCES actors (actor_id) ON DELETE RESTRICT,
	FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
    UNIQUE(movie_id, actor_id)
);

CREATE TABLE IF NOT EXISTS movies_genres (
	movie_genre_id INT NOT NULL AUTO_INCREMENT,
	movie_id INT NOT NULL,
	genre_id INT NOT NULL,
	PRIMARY KEY (movie_genre_id),
	FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE NO ACTION,
	FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
    UNIQUE(movie_id, genre_id)
);

CREATE TABLE IF NOT EXISTS users_reviews (
	review_id INT NOT NULL AUTO_INCREMENT,
	movie_id INT NOT NULL,
	user_id INT NOT NULL,
	movie_rating INT NOT NULL,
	PRIMARY KEY (review_id),
	FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
	FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
	UNIQUE(movie_id, user_id)
);

INSERT INTO movies(movie_id, movie_name, movie_year_released, movie_language, director_id) VALUES
(1, 'Life is Beautiful', 1997, 'Italian', 1), 
(2, "Pan's Labrynth", 2006, 'Spanish', 2), 
(3, 'Parasite', 2019, 'Korean', 3), 
(4, 'Raw', 2016, 'French', 4), 
(5, 'The Mummy', 1999, 'English', 5), 
(6, "Schindler's List", 1993, 'English', 6), 
(7, 'Jurassic Park', 1993, 'English', 6), 
(8, 'Silence of the Lambs', 1991, 'English', 7), 
(9, 'Vice', 2018, 'English', 8), 
(10, 'The Lobster', 2015, 'English', 9),
(11, 'Jurassic World', 2015, 'English', 11)
;

INSERT INTO actors(actor_id, actor_name) VALUES
(1, 'Roberto Benigni'),
(2, 'Nicoletta Braschi'),
(3, 'Giorgio Cantarini'),
(4, 'Ivana Baquero'),
(5, 'Ariadna Gil'),
(6, 'Sergi Lopez'),
(7, 'Song Kang-ho'),
(8, 'Lee Sun-kyun'),
(9, 'Cho Yeo-jeong'),
(10, 'Garance  Marillier '),
(11, 'Ella Rumpf'),
(12, 'Nait Oufella Rabah'),
(13, 'Brendan Fraser'),
(14, 'Rachel Weisz'),
(15, 'John Hannah'),
(16, 'Liam Neeson'),
(17, 'Ralph Fiennes'),
(18, 'Ben Kingsley'),
(19, 'Sam Neill'),
(20, 'Laura Dern'),
(21, 'Jeff Goldblum'),
(22, 'Jodie Foster'),
(23, 'Anthony Hopkins'),
(24, 'Lawrence Bonney'),
(25, 'Christian Bale'),
(26, 'Amy Adams'),
(27, 'Steve Carell'),
(28, 'Colin Farrell'),
(29, 'Jessica Barden'),
(30, 'Maggie Grace'),
(31, 'Famke Janssen'),
(32, 'Chris Pratt'),
(33, 'Bryce Dallas Howard'),
(34, 'Ty Simpkins')
;

INSERT INTO directors(director_id, director_name) VALUES
(1, 'Roberto Benigni'),
(2, 'Guillermo del Toro'),
(3, 'Bong Joon Ho'),
(4, 'Julia Ducournau'),
(5, 'Stephen Sommers'),
(6, 'Steven Spielberg'),
(7, 'Jonathan Demme'),
(8, 'Adam McKay'),
(9, 'Yorgos Lanthimos'),
(10, 'Pierre Morel'),
(11, 'Colin Trevorrow')
;

INSERT INTO genres(genre_id, genre_name) VALUES
(1, 'Action'),
(2, 'Adventure'),
(3, 'Animated'),
(4, 'Comedy'),
(5, 'Drama'),
(6, 'Fantasy'),
(7, 'Historical'),
(8, 'Horror'),
(9, 'Noir'),
(10, 'Romance'),
(11, 'Science fiction'),
(12, 'Thriller'),
(13, 'Western')
;

INSERT INTO users(user_id, user_first_name, user_last_name, user_email) VALUES
(1, 'Frodo', 'Baggins', 'frodo_baggins@gmail.com'), 
(2, 'Bilbo', 'Baggins', 'bilbo_baggins@gmail.com'), 
(3, 'Pippin', 'Took', 'pippin_took@gmail.com'), 
(4, 'Merry', 'Brandybuck', 'merry_brandybuck@gmail.om'), 
(5, 'Thorin', 'Oakenshield', 'thorin_oakenshield@gmail.com'), 
(6, 'Dwalin', 'Oakenshield', 'dwalin_oakenshield@gmail.com'), 
(7, 'Balin', 'Oakenshield', 'balin_oakenshield@gmail.com'), 
(8, 'Kili', 'Oakenshield', 'kili_oakenshield@gmail.com'), 
(9, 'Fili', 'Oakenshield', 'fili_oakenshield@gmail.com'), 
(10, 'Dori', 'Oakenshield', 'dori_oakenshield@gmail.com')
;

INSERT INTO movies_actors(movie_actor_id, movie_id, actor_id) VALUES
(1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 2, 4), 
(5, 2, 5), (6, 2, 6), (7, 3, 7), (8, 3, 8), 
(9, 3, 9), (10, 4, 10), (11, 4, 11), (12, 4, 12), 
(13, 5, 13), (14, 5, 14), (15, 5, 15), (16, 6, 16), 
(17, 6, 17), (18, 6, 18), (19, 7, 19), (20, 7, 20), 
(21, 7, 21), (22, 8, 22), (23, 8, 23), (24, 8, 24), 
(25, 9, 25), (26, 9, 26), (27, 9, 27), (28, 10, 28), 
(29, 10, 14), (30, 10, 29), (31, 11, 32), (32, 11, 33), 
(33, 11, 34)
;

INSERT INTO movies_genres(movie_genre_id, movie_id, genre_id) VALUES
(1, 1, 4), (2, 1, 5), (3, 1, 10), (4, 2, 5), 
(5, 2, 6), (6, 3, 5), (7, 3, 12), (8, 4, 5), 
(9, 4, 8), (10, 5, 1), (11, 5, 2), (12, 5, 6), 
(13, 6, 5), (14, 6, 7), (15, 7, 1), (16, 7, 2), 
(17, 7, 11), (18, 8, 5), (19, 8, 12), (20, 9, 4), 
(21, 9, 5), (22, 10, 5), (23, 10, 10), (24, 10, 11), 
(25, 11, 1), (26, 11, 2)
;

INSERT INTO users_reviews(review_id, movie_id,user_id,movie_rating) VALUES
(1, 7, 1, 4), (2, 6, 1, 5), 
(3, 1, 2, 5), (4, 7, 3, 5), 
(5, 9, 3, 3)
;

SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;