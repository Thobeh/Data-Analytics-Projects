# 🎬 Movie Database & SQL Query Solutions

A comprehensive T-SQL project containing database schema creation, relational table constraints, sample seed data, and a suite of solved analytical SQL queries (Questions 10 through 20).

## 📊 Database Schema & Entities

The project implements a fully normalized relational schema connected via primary and foreign key constraints across 9 distinct entities:

* **Movie:** Stores core film metadata (ID, title, release year, runtime, language, release date, and country).
* **Actor:** Maintains cast member profiles and gender classifications.
* **Director:** Tracks film director information.
* **Genre:** Categories for cinematic genres.
* **Movie_Genres:** Junction table mapping movies to multiple genres (Many-to-Many).
* **Movie_Direction:** Junction table linking directors to their films.
* **Reviewer:** Manages critic and user profiles.
* **Rating:** Captures user scores (`Reviewer_Stars`) and volume metrics per movie.
* **Movie_Cast:** Detailed bridge table tracking actors, movies, and specific character roles.

## 🛠️ Key Query Operations Covered

The script includes structured solutions for common and advanced database operations:

* **Targeted Updates:** Scoped `UPDATE` statements using proper primary key filtering.
* **Filtering & String Matching:** Utilizing `LIKE` clauses and date range comparisons.
* **Multi-Table Joins:** Inner and left joins combining metadata across directors, cast members, ratings, and titles.
* **Aggregations & Grouping:** Using `GROUP BY` and `HAVING` clauses for conditional group filtering.
* **Subqueries:** Implementing nested subqueries and `NOT IN` logic to isolate complex relational criteria (e.g., actors appearing in multiple films or excluding specific date ranges).

## 🚀 How to Run

1. Open **SQL Server Management Studio (SSMS)** or Azure Data Studio.
2. Open the SQL script file.
3. Execute the script sequentially to create the `movies_db` database, establish tables, insert test data, and review the executed query solutions.
