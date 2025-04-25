from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'students.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('Task4_1.html')

@app.route('/records')
def records():
    conn = get_db_connection()
    query = '''
        SELECT 
            Student.Name, 
            Student.Gender, 
            StudentHealthRecord.Weight, 
            StudentHealthRecord.Height
        FROM 
            Student
        LEFT JOIN 
            StudentHealthRecord ON Student.StudentID = StudentHealthRecord.StudentID
        ORDER BY 
            Student.Gender ASC, 
            Student.Name DESC;
    '''
    records = conn.execute(query).fetchall()
    conn.close()
    return render_template('Task4_2.html', records=records)


@app.route('/statistics')
def statistics():
    conn = get_db_connection()
    query = '''
        SELECT 
            Student.Gender,
            COUNT(Student.StudentID) AS TotalStudents,
            AVG(StudentHealthRecord.Weight) AS AverageWeight,
            AVG(StudentHealthRecord.Height) AS AverageHeight
        FROM 
            Student
        LEFT JOIN 
            StudentHealthRecord ON Student.StudentID = StudentHealthRecord.StudentID
        GROUP BY 
            Student.Gender;
    '''
    statistics = conn.execute(query).fetchall()
    conn.close()
    return render_template('Task4_3.html', statistics=statistics)


@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        conn = get_db_connection()
        try:
            cursor = conn.execute('INSERT INTO Student (Name, Gender) VALUES (?, ?)', 
                                (name, gender))
            student_id = cursor.lastrowid
            conn.execute('INSERT INTO StudentHealthRecord (StudentID, Weight, Height) VALUES (?, ?, ?)', 
                      (student_id, weight, height))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()
        return redirect('/records')
    
    return render_template('Task4_4.html')


if __name__ == '__main__':
    app.run(debug=True)