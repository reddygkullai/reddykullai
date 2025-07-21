from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import sqlite3
import random

# =============== APP INITIALIZATION ===============
app = Flask(__name__)
app.secret_key = 'secret'

UPLOAD_FOLDER = 'static/uploads'
STUDENT_UPLOAD_FOLDER = 'static/uploads_students'
STAFF_UPLOAD_FOLDER = 'static/uploads_staff'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STUDENT_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STAFF_UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STUDENT_UPLOAD_FOLDER'] = STUDENT_UPLOAD_FOLDER
app.config['STAFF_UPLOAD_FOLDER'] = STAFF_UPLOAD_FOLDER

# =============== MAIL CONFIG ===============
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gangireddykullaireddy646@gmail.com'  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'ram@12345G'  # Replace with your App Password
mail = Mail(app)

# =============== DATABASE INITIALIZATION ===============
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            hallticket TEXT UNIQUE,
            department TEXT,
            mobile TEXT,
            join_date TEXT,
            address TEXT,
            email TEXT UNIQUE,
            photo TEXT,
            username TEXT UNIQUE,
            password TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            personal_email TEXT,
            alt_email TEXT,
            years_exp INTEGER,
            username TEXT UNIQUE,
            password TEXT,
            photo_url TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            department TEXT,
            experience INTEGER,
            mobile TEXT,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            password TEXT,
            photo_url TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_code TEXT,
            subject_name TEXT,
            internal_marks INTEGER,
            external_marks INTEGER,
            total_marks INTEGER,
            credits INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )''')
        conn.commit()
        print("✅ Database initialized.")

# =============== SEND OTP FUNCTION ===============
def send_otp_email(recipient_email, otp):
    msg = Message('BET e-Portal OTP Verification',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient_email])
    msg.body = f"Your OTP for verification is: {otp}\nPlease use it to reset your password."
    mail.send(msg)

# =============== ROUTES ===============

@app.route('/', endpoint='home')
def index():
    return render_template('index.html')

# =============== STUDENT SIGNUP ===============
@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            hallticket = request.form['hallticket']
            department = request.form['department']
            mobile = request.form['mobile']
            join_date = request.form['join_date']
            address = request.form['address']
            email = request.form['email']
            photo = request.files['photo']

            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['STUDENT_UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            photo_url = f'uploads_students/{filename}'  # relative path for template url_for

            username = hallticket
            password = hallticket

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO students (name, hallticket, department, mobile, join_date, address, email, photo, username, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, hallticket, department, mobile, join_date, address, email, photo_url, username, password))
                conn.commit()
            flash('✅ Registration successful. Please log in.', 'success')
            return redirect(url_for('student_login'))

        except sqlite3.IntegrityError:
            flash('❌ Hallticket or email already registered. Please login.', 'error')
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
    return render_template('student_signup.html')

# =============== STUDENT LOGIN ===============
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['student_username']
        password = request.form['student_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE username=? AND password=?', (username, password))
            student = cursor.fetchone()
            if student:
                session['student_username'] = student[9]  # username column index
                flash('✅ Login successful.', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('❌ Invalid credentials.', 'error')
    return render_template('student_login.html')

# =============== STUDENT DASHBOARD ===============
@app.route('/student_dashboard')
def student_dashboard():
    if 'student_username' not in session:
        flash('❌ Please login first.', 'error')
        return redirect(url_for('student_login'))

    username = session['student_username']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, hallticket, department, photo FROM students WHERE username=?', (username,))
        student = cursor.fetchone()

        if student is None:
            flash('❌ Student not found.', 'error')
            session.pop('student_username', None)
            return redirect(url_for('student_login'))

        student_id = student[0]
        cursor.execute('SELECT subject_code, subject_name, internal_marks, external_marks, total_marks, credits FROM marks WHERE student_id=?', (student_id,))
        marks = cursor.fetchall()
    return render_template('student_dashboard.html', student=student, marks=marks)

# =============== STUDENT FORGOT PASSWORD (OTP FLOW) ===============
@app.route('/student_forgot_password', methods=['GET', 'POST'])
def student_forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE email=?', (email,))
            student = cursor.fetchone()
            if student:
                otp = str(random.randint(100000, 999999))
                session['student_forgot_email'] = email
                session['student_forgot_otp'] = otp
                send_otp_email(email, otp)
                flash(f'✅ OTP sent to {email}.', 'success')
                return redirect(url_for('student_forgot_otp_verify'))
            else:
                flash('❌ Email not registered.', 'error')
    return render_template('student_forgot_password.html')

@app.route('/student_forgot_otp_verify', methods=['GET', 'POST'])
def student_forgot_otp_verify():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('student_forgot_otp'):
            flash('✅ OTP verified. Set your new password.', 'success')
            return redirect(url_for('student_reset_password'))
        else:
            flash('❌ Incorrect OTP.', 'error')
    return render_template('student_forgot_otp_verify.html')

@app.route('/student_reset_password', methods=['GET', 'POST'])
def student_reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('❌ Passwords do not match.', 'error')
            return redirect(url_for('student_reset_password'))

        email = session.get('student_forgot_email')
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE students SET password=? WHERE email=?', (new_password, email))
            conn.commit()

        session.pop('student_forgot_email', None)
        session.pop('student_forgot_otp', None)

        flash('✅ Password updated successfully. Please login.', 'success')
        return redirect(url_for('student_login'))
    return render_template('student_reset_password.html')

# =============== LOGOUT ===============
@app.route('/logout')
def logout():
    session.clear()
    flash('✅ Logged out.', 'success')
    return redirect(url_for('home'))

# ===== ADMIN SIGNUP =====
@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            dob = request.form['dob']
            personal_email = request.form['personal_email']
            alt_email = request.form['alt_email']
            years_exp = request.form['years_exp']
            username = request.form['username']
            password = request.form['password']
            photo = request.files['photo']

            photo_url = ""
            if photo and photo.filename:
                photo_filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)
                photo_url = f'uploads/{photo_filename}'

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO admin (name, dob, personal_email, alt_email, years_exp, username, password, photo_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, dob, personal_email, alt_email, years_exp, username, password, photo_url))
                conn.commit()
            flash('✅ Admin signup successful!', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
            return redirect(url_for('admin_signup'))
    return render_template('admin_signup.html')

# ===== ADMIN LOGIN =====
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['admin_username']
        password = request.form['admin_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, password))
            admin = cursor.fetchone()
            if admin:
                session['admin_name'] = admin[1]
                flash('✅ Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('❌ Invalid admin credentials.', 'error')
                return redirect(url_for('admin_login'))
    return render_template('admin.html')

# ===== ADMIN DASHBOARD =====
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_name' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('admin_login'))
    admin_name = session['admin_name']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM staff')
        staff_list = cursor.fetchall()
    return render_template('admin_dashboard.html', admin_name=admin_name, staff_list=staff_list)

# ===== STAFF SIGNUP =====
@app.route('/staff_signup', methods=['GET', 'POST'])
def staff_signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            dob = request.form['dob']
            department = request.form['department']
            experience = request.form['experience']
            mobile = request.form['mobile']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            photo = request.files['photo']

            photo_url = ""
            if photo and photo.filename:
                photo_filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)
                photo_url = f'uploads/{photo_filename}'

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO staff (name, dob, department, experience, mobile, email, username, password, photo_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, dob, department, experience, mobile, email, username, password, photo_url))
                conn.commit()
            flash('✅ Staff signup successful!', 'success')
            return redirect(url_for('staff_login'))
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
            return redirect(url_for('staff_signup'))
    return render_template('staff_signup.html')

# ===== STAFF LOGIN =====
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['staff_username']
        password = request.form['staff_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM staff WHERE username=? AND password=?', (username, password))
            staff = cursor.fetchone()
            if staff:
                session['staff_username'] = staff[6]  # username index (0-based)
                session['staff_id'] = staff[0]  # staff id
                flash('✅ Staff login successful!', 'success')
                return redirect(url_for('staff_dashboard'))
            else:
                flash('❌ Invalid staff credentials.', 'error')
                return redirect(url_for('staff_login'))
    return render_template('staff_login.html')

# ===== STAFF DASHBOARD =====
@app.route('/staff_dashboard')
def staff_dashboard():
    if 'staff_username' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('staff_login'))
    username = session['staff_username']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, photo_url FROM staff WHERE username=?', (username,))
        staff_details = cursor.fetchone()
        cursor.execute('SELECT id, name, hallticket, department, photo FROM students')
        students_list = cursor.fetchall()
    return render_template('staff_dashboard.html', staff=staff_details, students=students_list)

# ===== PHOTO EDITS =====
@app.route('/edit_staff_photo', methods=['POST'])
def edit_staff_photo():
    if 'staff_id' not in session:
        return jsonify(success=False, error='Not logged in')

    staff_id = session['staff_id']
    photo = request.files.get('photo')

    if not photo:
        return jsonify(success=False, error='No photo uploaded')

    filename = secure_filename(photo.filename)
    filepath = os.path.join('static/uploads_staff', filename)
    photo.save(filepath)

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE staff SET photo_url = ? WHERE id = ?", (f'uploads_staff/{filename}', staff_id))
        conn.commit()

    new_url = url_for('static', filename='uploads_staff/' + filename)
    return jsonify(success=True, new_url=new_url)

@app.route('/edit_student_photo', methods=['POST'])
def edit_student_photo():
    if 'student_username' not in session:
        return jsonify(success=False, error='Not logged in.')

    username = session['student_username']
    photo = request.files.get('photo')

    if photo and photo.filename:
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['STUDENT_UPLOAD_FOLDER'], filename)
        photo_url = f'uploads_students/{filename}'

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT photo FROM students WHERE username = ?', (username,))
            result = cursor.fetchone()
            current_photo = result[0] if result else None

            if current_photo and current_photo != 'uploads_students/kullai.jpg':
                try:
                    old_photo_path = os.path.join('static', current_photo)
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                except Exception as e:
                    print(f"Warning: could not remove old photo: {e}")

            photo.save(photo_path)
            cursor.execute('UPDATE students SET photo = ? WHERE username = ?', (photo_url, username))
            conn.commit()

        return jsonify(success=True, new_url=url_for('static', filename=photo_url))

    return jsonify(success=False, error='No file received.')

# ===== PASSWORD RESET FOR ADMIN AND STAFF =====
@app.route('/admin_forgot_password', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE admin SET password=? WHERE personal_email=? OR alt_email=?', (new_password, email, email))
            if cursor.rowcount == 0:
                flash('❌ Email not found.', 'error')
            else:
                conn.commit()
                flash('✅ Password updated successfully. Please login.', 'success')
        return redirect(url_for('admin_login'))
    return render_template('admin_forgot_password.html')

@app.route('/staff_forgot_password', methods=['GET', 'POST'])
def staff_forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE staff SET password=? WHERE email=?', (new_password, email))
            if cursor.rowcount == 0:
                flash('❌ Email not found.', 'error')
            else:
                conn.commit()
                flash('✅ Password updated successfully. Please login.', 'success')
        return redirect(url_for('staff_login'))
    return render_template('staff_forgot_password.html')

# ===== ENTER MARKS (STAFF ONLY) =====
@app.route('/enter_marks/<int:student_id>', methods=['GET', 'POST'])
def enter_marks(student_id):
    if 'staff_username' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('staff_login'))

    if request.method == 'POST':
        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']
        internal_marks = int(request.form['internal_marks'])
        external_marks = int(request.form['external_marks'])
        total_marks = internal_marks + external_marks
        credits = int(request.form['credits'])

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO marks (student_id, subject_code, subject_name, internal_marks, external_marks, total_marks, credits)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, subject_code, subject_name, internal_marks, external_marks, total_marks, credits))
            conn.commit()
        flash('✅ Marks entered successfully.', 'success')
        return redirect(url_for('staff_dashboard'))

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM students WHERE id=?', (student_id,))
        student = cursor.fetchone()
    return render_template('enter_marks.html', student=student, student_id=student_id)

# ===== STATIC PAGES =====
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admissions')
def admissions():
    return render_template('admissions.html')

@app.route('/departments')
def departments():
    return render_template('departments.html')

@app.route('/amenities')
def amenities():
    return render_template('amenities.html')

@app.route('/placements')
def placements():
    return render_template('placements.html')

@app.route('/committees')
def committees():
    return render_template('committees.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/staff_profile')
def staff_profile():
    if 'staff_id' not in session:
        flash("Please login to access the profile.")
        return redirect(url_for('staff_login'))

    staff_id = session['staff_id']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
        staff_details = cursor.fetchone()

    return render_template('staff_profile.html', staff=staff_details)

@app.route('/edit_staff_profile', methods=['GET', 'POST'])
def edit_staff_profile():
    if 'staff_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('staff_login'))

    staff_id = session['staff_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']

        cursor.execute("UPDATE staff SET name=?, email=?, department=? WHERE id=?",
                       (name, email, department, staff_id))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('staff_profile'))

    # Fetch current staff details to pre-fill the form
    cursor.execute("SELECT name, email, department FROM staff WHERE id=?", (staff_id,))
    staff = cursor.fetchone()
    conn.close()

    return render_template('edit_staff_profile.html', staff=staff)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
