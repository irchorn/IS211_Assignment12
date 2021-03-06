from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask import g
import sqlite3
import datetime

app = Flask(__name__)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


app.config['SECRET_KEY'] = 'dev'
DATABASE = 'hw12.db'
app.config['DATABASE'] = DATABASE


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['username'] == 'admin':
        cur = g.db.execute("SELECT * FROM Students")
        cur2 = g.db.execute("SELECT * FROM Quizzes")

        res = cur.fetchall()
        res2 = cur2.fetchall()

        students = [dict(student_id=r[0], first_name=r[1], last_name=r[2]) for r in res]
        quizzes = [dict(quiz_id=r[0], subject=r[1], number_of_questions=r[2], date=r[3]) for r in res2]

        return render_template("dashboard.html", students=students, quizzes=quizzes)
    else:
        return redirect(url_for('/login'))


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if session['username'] == 'admin':

        if request.method == 'POST':
            student_name = request.form['last_name']
            g.db = get_db()

            g.db.execute("INSERT INTO Students(last_name) values(?)", (student_name,))
            g.db.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template("add_student.html")
    else:
        return redirect(url_for('/login'))


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if session['username'] == 'admin':

        if request.method == 'POST':
            quiz = request.form['subject']
            g.db = get_db()

            g.db.execute("INSERT INTO Quizzes(subject) values(?)", (quiz,))
            g.db.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template("add_quiz.html")
    else:
        return redirect(url_for('/login'))


@app.route('/add_score', methods=['GET', 'POST'])
def add_score():
    if session['username'] == 'admin':

        if request.method == 'POST':
            score = request.form['score']
            g.db = get_db()

            g.db.execute("INSERT INTO Score(score) values(?,)", (score))
            g.db.commit()

        return render_template("add_score.html")
    else:
        return redirect(url_for('dashboard'))


@app.route('/student/<id>')
def view_results(id):
    cur = g.db.execute(
        "SELECT Quizzes.quiz_id, Score.score, Quizzes.date, Quizzes.subject "
        "FROM Score inner join Quizzes ON Score.quiz_id = Quizzes.quiz_id "
        "inner join Students on Score.student_id = Students.student_id "
        "WHERE Students.student_id = ?", [id]
    )
    res = cur.fetchall()
    student_results = [dict(q_id=r[0], subject=r[1], date=r[2], score=r[3]) for r in res]
    return render_template("score.html", student_results=student_results)


if __name__ == "__main__":
    app.run(debug=True)
