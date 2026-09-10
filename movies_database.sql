/* =====================================================================
   MOVIES DATABASE SETUP & SCHEMA
   ===================================================================== */

CREATE DATABASE movies_db;
GO

USE movies_db;
GO

CREATE TABLE Movie
(
    Movie_ID int, 
    Movie_Title varchar(30), 
    Movie_Year int, 
    Movie_Time int, 
    Movie_Language varchar(10), 
    Movie_Release_Date date,
    Movie_Release_Country varchar(50),
    PRIMARY KEY (Movie_ID)
);

INSERT INTO Movie VALUES 
(901, 'Vertigo', 1958, 128, 'English', '1958-08-24', 'UK'),
(902, 'The Innocents', 1961, 100, 'English', '1962-02-19', 'SW'),
(903, 'Lawrence of Arabia', 1962, 216, 'English', '1962-12-11', 'UK'),
(904, 'The Deer Hunter', 1978, 183, 'English', '1979-03-08', 'UK'),
(905, 'Amadeus', 1984, 160, 'English', '1985-01-07', 'UK'),
(906, 'Blade Runner', 1982, 117, 'English', '1982-09-09', 'UK'),
(907, 'Eyes Wide Shut', 1999, 159, 'English', NULL, 'UK'),
(908, 'The Usual Suspects', 1995, 106, 'English', '1995-08-25', 'UK'),
(909, 'Chinatown', 1974, 130, 'English', '1974-08-09', 'UK'),
(910, 'Boogie Nights', 1997, 155, 'English', '1998-02-16', 'UK'), 
(911, 'Annie Hall', 1977, 93, 'English', '1977-04-20', 'USA'), 
(912, 'Princess Mononoke', 1997, 134, 'Japanese', '2001-10-19', 'UK'), 
(913, 'The Shawshank Redemption', 1994, 142, 'English', '1995-02-17', 'UK'), 
(914, 'American Beauty', 1999, 122, 'English', NULL, 'UK'), 
(915, 'Titanic', 1997, 194, 'English', '1998-01-23', 'UK'), 
(916, 'Good Will Hunting', 1997, 126, 'English', '1998-06-03', 'UK'), 
(917, 'Deliverance', 1972, 109, 'English', '1982-10-05', 'UK'), 
(918, 'Trainspotting', 1996, 94, 'English', '1996-02-23', 'UK'), 
(919, 'The Prestige', 2006, 130, 'English', '2006-11-10', 'UK'), 
(920, 'Donnie Darko', 2001, 113, 'English', NULL, 'UK'), 
(921, 'Slumdog Millionaire', 2008, 120, 'English', '2009-01-09', 'UK'),
(922, 'Aliens', 1986, 137, 'English', '1986-08-29', 'UK'),
(923, 'Beyond the Sea', 2004, 118, 'English', '2004-11-26', 'UK'),
(924, 'Avatar', 2009, 162, 'English', '2009-12-17', 'UK'), 
(925, 'Braveheart', 1995, 178, 'English', '1995-09-08', 'UK'),
(926, 'Seven Samurai', 1954, 207, 'Japanese', '1954-04-26', 'JP'),
(927, 'Spirited Away', 2001, 125, 'Japanese', '2003-09-12', 'UK'),
(928, 'Back to the Future', 1985, 116, 'English', '1985-12-04', 'UK');

CREATE TABLE Actor (
    Actor_ID int,
    First_Name varchar(30),
    Last_Name varchar(30),
    Gender char(1),
    PRIMARY KEY (Actor_ID)
);

INSERT INTO Actor VALUES 
(101, 'James', 'Stewart', 'M'),
(102, 'Deborah', 'Kerr', 'F'),
(103, 'Peter', 'OToole', 'M'),
(104, 'Robert', 'De Niro', 'M'),
(105, 'F. Murray', 'Abraham', 'M'),
(106, 'Harrison', 'Ford', 'M'),
(107, 'Nicole', 'Kidman', 'F'),
(108, 'Stephen', 'Baldwin', 'M'),
(109, 'Jack', 'Nicholson', 'M'),
(110, 'Mark', 'Wahlberg', 'M'),
(111, 'Woody', 'Allen', 'M'),
(112, 'Claire', 'Danes', 'F'),
(113, 'Tim', 'Robbins', 'M'),
(114, 'Kevin', 'Spacey', 'M'),
(115, 'Kate', 'Winslet', 'F'),
(116, 'Robin', 'Williams', 'M'),
(117, 'Jon', 'Voight', 'M'),
(118, 'Ewan', 'McGregor', 'M'),
(119, 'Christian', 'Bale', 'M'),
(120, 'Maggie', 'Gyllenhaal', 'F'),
(121, 'Dev', 'Patel', 'M'),
(122, 'Sigourney', 'Weaver', 'F'),
(123, 'David', 'Aston', 'M'),
(124, 'Ali', 'Astin', 'F');

CREATE TABLE Director (
    Director_ID int,
    First_Name varchar(30),
    Last_Name varchar(30),
    PRIMARY KEY (Director_ID)
);

INSERT INTO Director VALUES 
(201, 'Alfred', 'Hitchcock'),
(202, 'Jack', 'Clayton'),
(203, 'David', 'Lean'),
(204, 'Michael', 'Cimino'),
(205, 'Milos', 'Forman'),
(206, 'Ridley', 'Scott'),
(207, 'Stanley', 'Kubrick'),
(208, 'Bryan', 'Singer'),
(209, 'Roman', 'Polanski'),
(210, 'Paul Thomas', 'Anderson'),
(211, 'Woody', 'Allen'),
(212, 'Hayao', 'Miyazaki'),
(213, 'Frank', 'Darabont'),
(214, 'Sam', 'Mendes'),
(215, 'James', 'Cameron'),
(216, 'Gus', 'Van Sant'),
(217, 'John', 'Boorman'),
(218, 'Danny', 'Boyle'),
(219, 'Christopher', 'Nolan'),
(220, 'Richard', 'Kelly'),
(221, 'Kevin', 'Spacey'),
(222, 'Andrei', 'Tarkovsky'),
(223, 'Peter', 'Jackson');

CREATE TABLE Genre (
    Genre_ID int,
    Genre_Title varchar(20),
    PRIMARY KEY (Genre_ID)
);

INSERT INTO Genre VALUES 
(1001, 'Action'),
(1002, 'Adventure'),
(1003, 'Animation'),
(1004, 'Biography'),
(1005, 'Comedy'),
(1006, 'Crime'),
(1007, 'Drama'),
(1008, 'Horror'),
(1009, 'Music'),
(1010, 'Mystery'),
(1011, 'Romance'),
(1012, 'Thriller'),
(1013, 'War');

CREATE TABLE Movie_Genres (
    Movie_ID int,
    Genre_ID int,
    PRIMARY KEY (Movie_ID, Genre_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);

INSERT INTO Movie_Genres VALUES 
(922, 1001), (917, 1002), (903, 1002), (912, 1003), (911, 1005), 
(908, 1006), (913, 1006), (926, 1007), (928, 1007), (918, 1007), 
(921, 1007), (902, 1008), (923, 1009), (907, 1010), (927, 1010), 
(901, 1010), (914, 1011), (906, 1012), (904, 1013);

CREATE TABLE Movie_Direction (
    Director_ID int,
    Movie_ID int,
    PRIMARY KEY (Director_ID, Movie_ID),
    FOREIGN KEY (Director_ID) REFERENCES Director(Director_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID)
);

INSERT INTO Movie_Direction VALUES 
(201, 901), (202, 902), (203, 903), (204, 904), (205, 905), 
(206, 906), (207, 907), (208, 908), (209, 909), (210, 910), 
(211, 911), (212, 912), (213, 913), (214, 914), (215, 915), 
(216, 916), (217, 917), (218, 918), (219, 919), (220, 920), 
(218, 921), (215, 922), (221, 923);

CREATE TABLE Reviewer (
    Reviewer_ID int,
    Reviewer_Name varchar(50),
    PRIMARY KEY (Reviewer_ID)
);

INSERT INTO Reviewer VALUES 
(9001, 'Righty Sock'), (9002, 'Jack Malvern'), (9003, 'Flagrant Baronessa'), (9004, 'Alec Shaw'), (9005, NULL),
(9006, 'Victor Woeltjen'), (9007, 'Simon Wright'), (9008, 'Neal Wruck'), (9009, 'Paul Monks'), (9010, 'Mike Salvati'),
(9011, NULL), (9012, 'Wesley S. Walker'), (9013, 'Sasha Goldshtein'), (9014, 'Josh Cates'), (9015, 'Krug Stillo'),
(9016, 'Scott LeBrun'), (9017, 'Hannah Steele'), (9018, 'Vincent Cadena'), (9019, 'Brandt Sponseller'), (9020, 'Richard Adams');

CREATE TABLE Rating (
    Movie_ID int,
    Reviewer_ID int,
    Reviewer_Stars decimal(3,2),
    Number_of_Ratings int,
    PRIMARY KEY (Movie_ID, Reviewer_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID),
    FOREIGN KEY (Reviewer_ID) REFERENCES Reviewer(Reviewer_ID)
);

INSERT INTO Rating VALUES 
(901, 9001, 8.40, 263575), (902, 9002, 7.90, 20207), (903, 9003, 8.30, 202778),
(906, 9005, 8.20, 484746), (924, 9006, 7.30, NULL), (908, 9007, 8.60, 779489),
(909, 9008, NULL, 227235), (910, 9009, 3.00, 195961), (911, 9010, 8.10, 203875),
(912, 9011, 8.40, NULL), (914, 9013, 7.00, 862618), (915, 9001, 7.70, 830095),
(916, 9014, 4.00, 642132), (925, 9015, 7.70, 81328), (918, 9016, NULL, 580301),
(920, 9017, 8.10, 609451), (921, 9018, 8.00, 667758), (922, 9019, 8.40, 511613),
(923, 9020, 6.70, 13091);

CREATE TABLE Movie_Cast (
    Actor_ID int,
    Movie_ID int,
    Role varchar(50),
    PRIMARY KEY (Actor_ID, Movie_ID, Role),
    FOREIGN KEY (Actor_ID) REFERENCES Actor(Actor_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID)
);

INSERT INTO Movie_Cast VALUES 
(101, 901, 'John Scottie Ferguson'), (102, 902, 'Miss Giddens'), (103, 903, 'T.E. Lawrence'),
(104, 904, 'Michael'), (105, 905, 'Antonio Salieri'), (106, 906, 'Rick Deckard'),
(107, 907, 'Alice Harford'), (108, 908, 'McManus'), (110, 910, 'Eddie Adams'),
(111, 911, 'Alvy Singer'), (112, 912, 'San'), (113, 913, 'Andy Dufresne'),
(114, 914, 'Lester Burnham'), (115, 915, 'Rose DeWitt Bukater'), (116, 916, 'Sean Maguire'),
(117, 917, 'Ed'), (118, 918, 'Renton'), (120, 920, 'Elizabeth Darko'),
(121, 921, 'Older Jamal'), (122, 922, 'Ripley'), (114, 923, 'Bobby Darin'),
(109, 909, 'J.J. Gittes'), (119, 919, 'Alfred Borden');

/* Question 10. Edit reviewer stars of movie ID 909 to 8.45. */
-- Correction: Added WHERE clause to target only movie ID 909
UPDATE Rating 
SET Reviewer_Stars = 8.45 
WHERE Movie_ID = 909;

/* Question 11. Find when 'American Beauty' was released. Return release year. */
SELECT m.Movie_Year 
FROM Movie m 
WHERE m.Movie_Title = 'American Beauty';

/* Question 12. Find all reviewers who have rated seven or more stars. Return reviewer name. */
SELECT re.Reviewer_Name  
FROM Reviewer re  
JOIN Rating ra ON re.Reviewer_ID = ra.Reviewer_ID  
WHERE ra.Reviewer_Stars > 7;

/* Question 13. Find movie titles containing 'Boogie Nights', sorted by release year ascending. */
-- Correction: Included Movie_ID, Movie_Title, Movie_Release_Year and ordered by Year
SELECT m.Movie_ID, m.Movie_Title, m.Movie_Year 
FROM Movie m 
WHERE m.Movie_Title LIKE '%Boogie Nights%' 
ORDER BY m.Movie_Year ASC;

/* Question 14. Find who was cast in 'Annie Hall'. Return actor first name, last name, role. */
SELECT a.First_Name, a.Last_Name, mc.Role 
FROM Actor a 
JOIN Movie_Cast mc ON a.Actor_ID = mc.Actor_ID 
JOIN Movie m ON mc.Movie_ID = m.Movie_ID 
WHERE m.Movie_Title = 'Annie Hall';

/* Question 15. Find director for the role in 'Eyes Wide Shut'. Return first name, last name, movie title. */
SELECT d.First_Name, d.Last_Name, m.Movie_Title 
FROM Director d 
JOIN Movie_Direction md ON d.Director_ID = md.Director_ID  
JOIN Movie m ON md.Movie_ID = m.Movie_ID 
WHERE m.Movie_Title = 'Eyes Wide Shut';

/* Question 16. Find actors who have NOT appeared in any movies between 1990 and 2000 inclusive. */
-- Correction: Fixed positive logic error by using NOT IN to exclude the 1990-2000 window
SELECT First_Name, Last_Name 
FROM Actor 
WHERE Actor_ID NOT IN (
    SELECT mc.Actor_ID 
    FROM Movie_Cast mc 
    JOIN Movie m ON mc.Movie_ID = m.Movie_ID 
    WHERE m.Movie_Year BETWEEN 1990 AND 2000
);

/* Question 18. Find movies released before 1st Jan 1989. Sort descending by release date. */
-- Correction: Added director fields, removed invalid group by, and updated order to DESC
SELECT  
    m.Movie_Title, 
    m.Movie_Year, 
    m.Movie_Release_Date,  
    m.Movie_Time,
    d.First_Name AS Director_First_Name,
    d.Last_Name AS Director_Last_Name
FROM Movie m  
LEFT JOIN Movie_Direction md ON m.Movie_ID = md.Movie_ID
LEFT JOIN Director d ON md.Director_ID = d.Director_ID
WHERE m.Movie_Release_Date < '1989-01-01'
ORDER BY m.Movie_Release_Date DESC;

/* Question 19. Find movies that received ratings. Return movie title, director name, and stars. */
-- Correction: Fixed director join condition typo and handled aggregate selection error
SELECT  
    m.Movie_Title,  
    d.First_Name,  
    d.Last_Name,  
    r.Reviewer_Stars  
FROM Rating r  
JOIN Movie m ON r.Movie_ID = m.Movie_ID  
JOIN Movie_Direction md ON m.Movie_ID = md.Movie_ID  
JOIN Director d ON md.Director_ID = d.Director_ID;

/* Question 20. Find movies in which one or more actors have acted in more than one film. */
SELECT  
    m.Movie_Title,  
    a.First_Name,  
    a.Last_Name,  
    mc.Role  
FROM Movie m  
JOIN Movie_Cast mc ON m.Movie_ID = mc.Movie_ID  
JOIN Actor a ON mc.Actor_ID = a.Actor_ID  
WHERE mc.Actor_ID IN (
    SELECT Actor_ID  
    FROM Movie_Cast  
    GROUP BY Actor_ID  
    HAVING COUNT(DISTINCT Movie_ID) > 1
);
