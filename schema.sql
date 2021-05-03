DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quizzes;
DROP TABLE IF EXISTS Score;

CREATE TABLE IF NOT EXISTS Students(student_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT);
CREATE TABLE IF NOT EXISTS Quizzes(quiz_id INTEGER PRIMARY KEY, subject TEXT, number_of_questions INTEGER, date TEXT );
CREATE TABLE IF NOT EXISTS Score(score_id INTEGER PRIMARY KEY, student_id INTEGER, quiz_id INTEGER, score INTEGER)

INSERT INTO Students VALUES(1,'John','Smith');
INSERT INTO Quizzes VALUES(1,'Python Basics', 5, 'Feb 5 2015');
INSERT INTO Score VALUES(1,1,85);

SELECT first_name, last_name, subject, date, score FROM Score sc
INNER JOIN Students st ON st.student_id = sc.student_id
INNER JOIN Quizzes q ON q.quiz_id = sc.quiz_id
WHERE student_id = 1;
