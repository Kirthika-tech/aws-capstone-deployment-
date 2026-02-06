
 **Blood Bridge: optimizing Lifesaving resources using AWS Services**    
🔴 1. index.html – Landing Page (Home)

What you see:

Clean white card in the center
🩸 Blood Bridge title
Subtitle: Blood Donation Management System

Two buttons:
Login
Sign Up

Flow:
👉 Click Login → goes to /login
👉 Click Sign Up → goes to /signup

🔐 2. login.html – Doctor Login Page

Look & Feel:
Full screen red–purple gradient background
Center white card with shadow

Logo: 🩸 BLOOD BRIDGE

Subtitle: Doctor Login Portal

Inputs:
Username
Password

Button:
🚨 ACCESS SYSTEM
Extra:
Flash messages (green = success, red = error)

Quick login shown:
blood / bridge

✅ On correct login → redirects to Dashboard

📝 3. signup.html – Doctor Registration

Look & Feel:
Red gradient background
White signup card

Title: New Doctor Registration
Inputs:
Doctor Username
Password

Button:
CREATE ACCOUNT 🩺

Extras:
Flash success/error message
Link back to login
Shows default login credentials
🏥 4. dashboard.html – Main Dashboard (After Login)
🔝 Top Navbar (only after login)

Red navbar showing:
👋 Dr. BLOOD |
Dashboard | Confirmation | Register | Respond |
Request | Single | About | Logout

📊 Dashboard Content

Centered white panel:
Stats Cards:
🩸 247 Units Available

Button: Request Blood
⚡ 12 Emergency Alerts

Button: Respond Now
✅ 89% Success Rate
Button: View Confirmations

If not logged in, it shows:
Blood Bridge Hospital
Emergency Login button

ℹ️ 5. about.html – About Blood Bridge

Very premium looking page 🔥

Sections:
Big title: 🩸 Blood Bridge
Mission statement (red gradient card)
📊 Impact stats (500+ donors, 98% success)

✨ Features grid:
Live Inventory
AI Matching
Alerts
Hospital Portal
Security
Analytics
🔄 Workflow (step-by-step ordered list)
✅ Why choose us

Buttons:
🏠 Back to Dashboard
🚪 Logout
💯 Interview-ready page.

✅ 6. confirmation.html – Blood Request Confirmation

Look & Feel:
Green success theme

Card showing:
Request #BB-247
O-Negative | 3 Units
Status: DELIVERED


Clickable card:
👉 Opens a modal popup with:
Patient name
Hospital
Doctor
Date & Time
SUCCESS status

Button:
← Dashboard

🚨 7. request.html – Emergency Blood Request

Theme:
Red / emergency colors

Main Card:
🩸 EMERGENCY #REQ-589
A+ | STAT
Trauma case
Click → Modal opens

Shows:
Patient
Blood type
Units
Priority
ETA

📋 8. respond.html – Emergency Alerts

Theme:
Orange / warning colors

Alert Card:
⚡ Alert #ALRT-456
B+ | URGENT
Click → Modal

Shows:
Hospital
Patient
Distance
Remaining response time

👤 9. single.html – Single Patient View

Theme:
Blue / medical

Patient Card:
🩸 Anjali R.

Status: CRITICAL
Click → Modal Table

Shows:
Patient ID
Age
Blood Type
Condition
Doctor
Hospital

👥 10. register.html – Donor Registration View

Theme:
Purple gradient

Shows donor cards:
Name + ID
Blood group

Status:
✅ AVAILABLE (green)
⏳ PENDING (orange)

Buttons:
🏥 Dashboard
✅ Confirmations


**APP.PY**

🏠 First Screen (Home)
You see:
🩸 Blood Bridge
Text: Blood Donation Management System

Two buttons:
Login
Sign Up

👉 This page is shown only if you are NOT logged in.

🔐 Login Screen
After clicking Login:
Stylish red/purple background
Center white card

Title: BLOOD BRIDGE
Subtitle: Doctor Login Portal
Username box
Password box

Button: 🚨 ACCESS SYSTEM

If login is:
✅ Correct → goes to Dashboard
❌ Wrong → red error message shown

🏥 Dashboard (Main Page)
After login, this is the main screen.
Top Red Navigation Bar

Shows:
Dashboard | Confirmation | Register | Respond |
Request | Single | About | Logout

Dashboard Content
Big title: Blood Bridge Dashboard

3 cards:
🩸 Units Available
⚡ Emergency Alerts

✅ Success Rate
Each card has a button to open related pages.

ℹ️ About Page
Looks very premium and professional.

Shows:
Project name & mission
Impact numbers (donors, success rate)
Features (AI matching, alerts, security, etc.)
Step-by-step workflow

Buttons:
Back to Dashboard
Logout

✅ Confirmation Page
Green success theme
Shows completed blood request
Clicking the card opens a popup

Popup shows:
Patient name
Hospital
Blood group

Status: SUCCESS

👥 Register Page (Donors)
Purple theme
Cards showing donors

Each card shows:
Name
Blood group
Status (Available / Pending)

Buttons at bottom:
Dashboard
Confirmations

📋 Respond Page
Orange warning theme
Emergency alert card

Clicking opens popup with:
Hospital
Blood type
Distance
Time remaining

🚨 Request Page
Red emergency theme
Shows urgent blood request

Popup shows:
Patient
Blood group
Units required
Priority & ETA

👤 Single Patient Page
Blue medical theme
Patient card with CRITICAL label
Popup shows full patient details in table format

🚪 Logout
Takes you back to Home page
Dashboard & other pages are no longer accessible


**PROJECT FLOW(AWS-app.py)
**
🔐 LOGIN SYSTEM (Session)
User Login
   │
   ▼
session['username']
   │
   ▼
Access Pages

☁️ AWS CONNECTION
App Start
   │
   ▼
AWS Available?
   │
   ├─ YES ─► DynamoDB + SNS
   │
   └─ NO  ─► Simple Login (blood/bridge)

🗄️ DYNAMODB TABLES
Donors Table
 ├─ username
 └─ password

BloodRequests Table
 ├─ id
 ├─ title
 ├─ blood_group
 ├─ urgency
 ├─ hospital
 └─ status

🔔 SNS NOTIFICATION
Event
   │
   ▼
SNS Topic
   │
   ▼
Notification Sent

🌐 ROUTES FLOW
/  → Home
│
├─ /login
│
├─ /signup
│
├─ /dashboard
│
├─ /about
│
├─ /confirmation
│
├─ /register
│
├─ /request
│
├─ /respond
│
├─ /single
│
└─ /logout

🆕 CREATE BLOOD REQUEST
Doctor Form
   │
   ▼
uuid generated
   │
   ▼
Saved in DynamoDB
   │
   ▼
SNS Alert



