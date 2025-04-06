from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'healthcare'

mysql = MySQL(app)

# Route for Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['logged_in'] = True
            session['username'] = username
            flash('Login Successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Route to Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect('/login')

# Home Page (Requires Login)
@app.route('/')
def Index():
    if not session.get('logged_in'):
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', appointments=data)

# Insert Appointment
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        patient_name = request.form['patient_name']
        phone = request.form['phone']
        appointment_date = request.form['appointment_date']
        description = request.form['description']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        diabetes = request.form['diabetes']
       

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO appointments (patient_name, phone, appointment_date, description,email,age,gender,diabetes) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)",
                    (patient_name, phone, appointment_date, description,email,age,gender,diabetes))
        mysql.connection.commit()
        flash("Appointment Added Successfully", 'success')
        return redirect('/')

# Delete Appointment
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM appointments WHERE id = %s", (id,))
    mysql.connection.commit()
    flash("Appointment Deleted Successfully", 'danger')
    return redirect('/')

# Update Appointment
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        patient_name = request.form['patient_name']
        phone = request.form['phone']
        appointment_date = request.form['appointment_date']
        description = request.form['description']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        diabetes = request.form['diabetes']
       

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE appointments SET patient_name=%s, phone=%s, appointment_date=%s, description=%s ,email = %s,age = %s,gender = %s ,diabetes= %s WHERE id=%s
        """, (patient_name, phone, appointment_date, description,email,age,gender,diabetes, id))
        mysql.connection.commit()
        flash("Appointment Updated Successfully", 'success')
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
