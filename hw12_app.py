#!/usr/bin/env python
# coding: utf-8

# In[49]:


from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask import g
import sqlite3
import datetime

app = Flask(__name__)


# In[45]:


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# In[46]:


app.config['SECRET_KEY']='dev'

DATABASE = 'hw12.db'

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


# In[47]:


@app.before_request
def before_request():
    g.db = connect_db()


# In[48]:


@app.route('/')
def index():
    return rederect('/login')


# In[59]:


@app.route('/login', method =['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        session['username']= request.form['username']
        username = request.form['username']
        password = rquest.form['password']
        
        if username == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            return render_template('login.html')
   


# In[60]:


@app.route('/dashboard/')
def dashboard():
    if session['username']=='admin':
        cur = g.db.execute("SELECT * FROM Students")
        cur2 = g.db.execute("SELECT * FROM Quizzes")
        
        result = cur.fetchall()
        result2 = cur2.fetchall()
        
        students = [dict(student_id = r[0], first_name = r[1], last_name =r[2]) for r in result]
        quizzes = [dict(quiz_id = r[0], subject = r[1], number_of_questions=r[2], date=r[3]) for r in result2]
        
        return render_template("dashboard.html", students=students, quizzes=quizzes)
    else:
        return redirect('/login')


# In[61]:


@app.route('/add_student', method =['GET', 'POST'])
def add_student():
    if session ['user_name'] == 'admin':
    
        if request.metod == 'POST':
            student_name = request.form['last_name']
            g.db=get.db()
      
            g.db.execute("INSERT INTO Students(last_name) values(?,)",(student_name))
        return redirect(url_for('dashboard'))
    


# In[66]:


@app.route('/add_quiz', method =['POST'])
def add_quiz():
    if session ['user_name'] == 'admin':
    
        if request.metod == 'POST':
            quiz = request.form['subject']
            g.db=get.db()
      
            g.db.execute("INSERT INTO Quizzes(subject) values(?,)",(subject))
        return redirect(url_for('dashboard'))


# In[ ]:



