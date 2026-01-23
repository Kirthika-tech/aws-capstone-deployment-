from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)
app.secret_key = 'blood-bridge-2026'

users = {'blood': 'bridge'}

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))  # Logged in → Dashboard
    return render_template('index.html')     # Not logged in → Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'blood' and password == 'bridge':
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # → DASHBOARD
        else:
            flash('Wrong! Use: blood / bridge', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/about')  
def about():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('about.html', username=session['username'])

# 🔥 5 NEW PAGES ADDED HERE
@app.route('/confirmation')
def confirmation():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('confirmation.html', username=session['username'])

@app.route('/register')
def register():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('register.html', username=session['username'])

@app.route('/respond')
def respond():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('respond.html', username=session['username'])

@app.route('/request')
def request_page():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('request.html', username=session['username'])

@app.route('/single')
def single():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('single.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        users[username] = request.form['password']
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)











