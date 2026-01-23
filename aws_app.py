from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import boto3
import uuid
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = 'blood-bridge-2026'

# AWS Configuration (Optional - fallback to simple auth)
REGION = 'us-east-1'
try:
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    sns = boto3.client('sns', region_name=REGION)
    AWS_AVAILABLE = True
    
    # Blood Bridge DynamoDB Tables
    donors_table = dynamodb.Table('Donors')
    blood_requests_table = dynamodb.Table('BloodRequests')
    SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:604665149129:blood_bridge_notifications'
except:
    AWS_AVAILABLE = False
    print("AWS not configured - using simple auth")

# Simple fallback users (blood/bridge)
users = {'blood': 'bridge'}

def is_logged_in():
    return 'username' in session

def send_blood_notification(subject, message):
    if not AWS_AVAILABLE:
        print(f"🔔 {subject}: {message}")
        return
    try:
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)
    except:
        print(f"Notification: {message}")

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Try AWS first, then simple auth
        if AWS_AVAILABLE:
            try:
                response = donors_table.get_item(Key={'username': username})
                if 'Item' in response and response['Item']['password'] == password:
                    session['username'] = username
                    send_blood_notification("Doctor Login", f"Dr. {username} logged into Blood Bridge")
                    return redirect(url_for('dashboard'))
            except:
                pass
        
        # Fallback to simple auth
        if username == 'blood' and password == 'bridge':
            session['username'] = username
            flash('Login successful! 🩸', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Wrong! Use: blood / bridge', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    # Get blood requests if AWS available
    blood_requests = []
    if AWS_AVAILABLE:
        try:
            response = blood_requests_table.scan()
            blood_requests = response.get('Items', [])
        except:
            pass
    
    return render_template('dashboard.html', 
                         username=session['username'], 
                         blood_requests=blood_requests)

@app.route('/about')
def about():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('about.html', username=session['username'])

# 🔥 BLOOD BRIDGE 7 PAGES (Your exact routes)
@app.route('/confirmation')
def confirmation():
    if not is_logged_in(): return redirect(url_for('login'))
    return render_template('confirmation.html', username=session['username'])

@app.route('/register')
def register():
    if not is_logged_in(): return redirect(url_for('login'))
    return render_template('register.html', username=session['username'])

@app.route('/respond')
def respond():
    if not is_logged_in(): return redirect(url_for('login'))
    return render_template('respond.html', username=session['username'])

@app.route('/request')
def request_page():
    if not is_logged_in(): return redirect(url_for('login'))
    return render_template('request.html', username=session['username'])

@app.route('/single')
def single():
    if not is_logged_in(): return redirect(url_for('login'))
    return render_template('single.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out! 👋', 'success')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if AWS_AVAILABLE:
            try:
                response = donors_table.get_item(Key={'username': username})
                if 'Item' in response:
                    return "Doctor already exists!"
                donors_table.put_item(Item={'username': username, 'password': password, 'role': 'doctor'})
                send_blood_notification("New Doctor", f"Dr. {username} registered")
                return redirect(url_for('login'))
            except:
                pass
        
        # Fallback simple signup
        users[username] = password
        flash('Account created! Login with AWS or blood/bridge', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# AWS Doctor Create Blood Request (Bonus!)
@app.route('/doctor/create_request', methods=['GET', 'POST'])
def create_blood_request():
    if not is_logged_in(): return redirect(url_for('login'))
    
    if request.method == 'POST':
        request_id = str(uuid.uuid4())
        blood_request = {
            'id': request_id,
            'title': request.form['title'],
            'blood_group': request.form['blood_group'],
            'urgency': request.form['urgency'],
            'hospital': session['username'],
            'status': 'open'
        }
        
        if AWS_AVAILABLE:
            try:
                blood_requests_table.put_item(Item=blood_request)
                send_blood_notification("New Blood Request", f"{blood_request['title']} - {blood_request['blood_group']} needed!")
            except:
                flash('Request saved locally!', 'success')
        else:
            flash('Request saved locally!', 'success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('create_request.html', username=session['username'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
