from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret'

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =============== DATABASE INITIALIZATION ===============
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                dob TEXT,
                personal_email TEXT,
                alt_email TEXT,
                years_exp INTEGER,
                username TEXT UNIQUE,
                password TEXT,
                photo_url TEXT
            )
        ''')
        # Staff table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
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
            )
        ''')
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hallticket TEXT UNIQUE,
                department TEXT,
                mobile TEXT,
                join_date TEXT,
                address TEXT,
                photo TEXT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        # Marks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_code TEXT,
                subject_name TEXT,
                internal_marks INTEGER,
                external_marks INTEGER,
                total_marks INTEGER,
                credits INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')
        conn.commit()
    print("✅ Database initialized.")

# =============== ROUTES ===============

@app.route('/')
def index():
    return render_template('index.html')

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
                photo_url = photo_path

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
                photo_url = photo_path

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
                session['staff_username'] = staff[7]
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
        # Staff details for header
        cursor.execute('SELECT name, photo_url FROM staff WHERE username=?', (username,))
        staff_details = cursor.fetchone()
        # Fetch all student details for display
        cursor.execute('SELECT id, name, hallticket, department, photo FROM students')
        students_list = cursor.fetchall()
    return render_template('staff_dashboard.html', staff=staff_details, students=students_list)


# ===== STUDENT SIGNUP =====
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
            photo = request.files['photo']

            photo_filename = ""
            if photo and photo.filename:
                photo_filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)

            username = hallticket  # using hallticket as username
            password = hallticket  # using hallticket as default password

            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO students (name, hallticket, department, mobile, join_date, address, photo, username, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, hallticket, department, mobile, join_date, address, photo_filename, username, password))
                conn.commit()

            flash('✅ Student signup successful! You can now log in.', 'success')
            return redirect(url_for('student_login'))

        except sqlite3.IntegrityError:
            flash('❌ Hall Ticket already registered. Use a different one.', 'error')
            return redirect(url_for('student_signup'))
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
            return redirect(url_for('student_signup'))

    return render_template('student_signup.html')

# ===== STUDENT LOGIN (Placeholder for future student routes) =====
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
                session['student_username'] = student[8]
                flash('✅ Student login successful!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('❌ Invalid student credentials.', 'error')
                return redirect(url_for('student_login'))
    return render_template('student_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'student_username' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('student_login'))
    username = session['student_username']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Get student details
        cursor.execute('SELECT id, name, hallticket, department, photo FROM students WHERE username=?', (username,))
        student_details = cursor.fetchone()
        student_id = student_details[0]
        # Get marks
        cursor.execute('''
            SELECT subject_code, subject_name, internal_marks, external_marks, total_marks, credits
            FROM marks WHERE student_id=?
        ''', (student_id,))
        marks_list = cursor.fetchall()
    return render_template('student_dashboard.html', student=student_details, marks=marks_list)

@app.route('/student_forgot_password', methods=['GET', 'POST'])
def student_forgot_password():
    if request.method == 'POST':
        hallticket = request.form['hallticket']
        new_password = request.form['new_password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE students SET password=? WHERE hallticket=?', (new_password, hallticket))
            if cursor.rowcount == 0:
                flash('❌ Hall Ticket not found.', 'error')
            else:
                conn.commit()
                flash('✅ Password updated successfully. Please login.', 'success')
        return redirect(url_for('student_login'))
    return render_template('student_forgot_password.html')

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

# ===== LOGOUT =====
@app.route('/logout')
def logout():
    session.clear()
    flash('✅ You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/enter_marks/<int:student_id>', methods=['GET', 'POST'])
def enter_marks(student_id):
    if 'staff_username' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('staff_login'))
    if request.method == 'POST':
        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']
        internal_marks = request.form['internal_marks']
        external_marks = request.form['external_marks']
        total_marks = int(internal_marks) + int(external_marks)
        credits = request.form['credits']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO marks (student_id, subject_code, subject_name, internal_marks, external_marks, total_marks, credits)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, subject_code, subject_name, internal_marks, external_marks, total_marks, credits))
            conn.commit()
        flash('✅ Marks entered successfully.', 'success')
        return redirect(url_for('staff_dashboard'))
    # Get student details for display
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, hallticket FROM students WHERE id=?', (student_id,))
        student = cursor.fetchone()
    return render_template('enter_marks.html', student=student, student_id=student_id)

@app.route('/staff_profile')
def staff_profile():
    if 'staff_username' not in session:
        flash('❌ Please log in first.', 'error')
        return redirect(url_for('staff_login'))

    username = session['staff_username']
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM staff WHERE username = ?', (username,))
        staff = cursor.fetchone()
    return render_template('staff_profile.html', staff=staff)

@app.route('/edit_staff_profile', methods=['GET', 'POST'])
def edit_staff_profile():
    if 'staff_id' not in session:
        flash("Session expired. Please login again.")
        return redirect(url_for('staff_login'))

    staff_id = session['staff_id']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            department = request.form['department']
            password = request.form['password']
            photo = request.files.get('photo')

            # Update photo if provided
            if photo and photo.filename != '':
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
                cursor.execute('UPDATE staff SET photo = ? WHERE id = ?', (photo_path, staff_id))

            # Update password if provided
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute('UPDATE staff SET password = ? WHERE id = ?', (hashed_password, staff_id))

            # Update other fields
            cursor.execute('UPDATE staff SET name = ?, email = ?, department = ? WHERE id = ?',
                           (name, email, department, staff_id))
            conn.commit()

            flash('Profile updated successfully.')
            return redirect(url_for('staff_dashboard'))  # back to dashboard to see updated profile

        # For GET, fetch current details to prefill
        cursor.execute('SELECT * FROM staff WHERE id = ?', (staff_id,))
        staff = cursor.fetchone()

    return render_template('edit_staff_profile.html', staff=staff)


# =============== RUN APP ===============
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
