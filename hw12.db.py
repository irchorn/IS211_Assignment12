import sqlite3 as lite


def insert_data():
    con = lite.connect('hw12.db')

    with con:
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS Students(student_id INT, first_name TEXT, last_name TEXT)")
        cur.execute("INSERT INTO Students VALUES(1,'John','Smith')")

        cur.execute(
            "CREATE TABLE IF NOT EXISTS Quizzes(quiz_id INT, subject TEXT, number_of_questions INT, date TEXT )")
        cur.execute("INSERT INTO Quizzes VALUES(1,'Python Basics', 5, 'Feb 5 2015')")

        cur.execute("CREATE TABLE IF NOT EXISTS Score(score_id, student_id INT, quiz_id INT, score INT)")
        cur.execute("INSERT INTO Score VALUES(1, 1, 1, 85)")


def students_data():
    con = lite.connect('hw12.db')
    with con:
        con.row_factory = lite.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM Students")
        rows = cur.fetchall()
        for row in rows:
            print("{} {} {}".format(row["student_id"],row["last_name"], row["first_name"] ))


def quiz_data():
    con = lite.connect('hw12.db')
    with con:
        con.row_factory = lite.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM Quizzes")
        rows = cur.fetchall()
        for row in rows:
            print("{} {} {}".format(row["quiz_id"], row["subject"], row["number_of_questions"], row["date"] ))


if __name__ == "__main__":
    insert_data()
    students_data()
    quiz_data()
