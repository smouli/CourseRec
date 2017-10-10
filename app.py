# ./app.py
from flask import Flask,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
from database_connector import read
from machine_learning_service import ml_train, ml_predict, normalize
from sklearn import neighbors
import psycopg2

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yipgikbasudyog:21d1ee6803375e19da2ed3cfc8c726f036e3e11871d62b65df13134be5c69ec2@ec2-54-163-229-169.compute-1.amazonaws.com:5432/df5g8vla4snv52'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello World1!"

@app.route('/prereg')
def prereg():
      sql = text("SELECT * FROM course")
      result = db.engine.execute(sql)
      results = []
      for row in result:
          obj = {
            'id': row.idcourse,
            'title': row.name,
          }
          results.append(obj)

      response = jsonify(results)
      response.status_code = 200
      return response

@app.route('/showCourse/<int:ID>')
def showCourse(ID):
      sql2 = "SELECT * FROM course where idcourse = %d " % ID
      sql = text(sql2)
      result = db.engine.execute(sql)
      results = []
      for row in result:
          obj = {
            'id': row.idcourse,
            'title': row.name,
          }
          results.append(obj)

      response = jsonify(results)
      response.status_code = 200
      return response

@app.route('/test_html/<user>')
def test_html(user):
    return render_template('hello.html', name = user)

@app.route('/displayAll')
def displayAll():
    sql2 = "select a.username, a.fname, a.lname, a.dob, a.email, a.timecreated, a.major, a.credit_hours, a.degree, b.code, b.name, b.description from student a, course b, student_course c where c.studentid=a.idstudent and c.courseid=b.idcourse"
    sql = text(sql2)
    result = db.engine.execute(sql)
    results = []
    for row in result:
        obj = {
            #'id': row.idstudent_course,
            'studentid': row.username,
            'courseid': row.name,
            #'rank': row.rank,
            #'year': row.year,
            #'semester': row.semester,
        }
        results.append(obj)

    response = jsonify(results)
    response.status_code = 200
    return response

@app.route('/result_list')
def result_list():
    con = None
    try:
        con = psycopg2.connect(host = 'ec2-54-163-229-169.compute-1.amazonaws.com', database = 'df5g8vla4snv52', user = 'yipgikbasudyog', password = '21d1ee6803375e19da2ed3cfc8c726f036e3e11871d62b65df13134be5c69ec2')
        cur = con.cursor()
        cur.execute("SELECT * FROM courseList")
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        temp = []
        for row in rows:
            temp.append(list(row))

        courses = []
        for i in range(0, len(temp)):
            courses.append(temp[i][1])

        n_neighbors = 4
        clf = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
        train_data = read(0)
        pred_data = read(1)
        ml_train(train_data, clf)
        predicts = ml_predict(pred_data, clf)
        fin_pred = []
        for i in range(0, len(predicts)):
            if (predicts[i] == 0):
                string = "Yes: " + courses[i]
                fin_pred.append(string)
            else:
                string = "No: " + courses[i]
                fin_pred.append(string)

        response = jsonify(fin_pred)
        response.status_code = 200
        return response
    finally:
        if con:
            con.close()


if __name__ == '__main__':
          port = 8000 #the custom port you want
          app.run(debug=True)
          #app.run(host='0.0.0.0', port=port)
