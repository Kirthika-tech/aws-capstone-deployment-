from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "bloodbridgekey"

# ---------------- USERS ----------------
users = {"blood": "bridge"}

# ---------------- TABLES ----------------
donor_table = []
request_table = []

# ---------------- HELPER ----------------
def is_logged_in():
    return "username" in session

# ---------------- HOME ----------------
@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            flash("Login Successful", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong credentials! Use blood / bridge", "error")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"],
                           donors=donor_table, requests=request_table)

# ---------------- REGISTER DONOR ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if not is_logged_in():
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        blood_group = request.form.get("blood_group")
        last_donation = request.form.get("last_donation")

        donor_table.append({
            "name": name,
            "email": email,
            "phone": phone,
            "blood_group": blood_group,
            "last_donation": last_donation
        })

        last_date = datetime.strptime(last_donation, "%Y-%m-%d")
        next_date = last_date + timedelta(days=90)

        return render_template(
            "register_success.html",
            name=name,
            blood_group=blood_group,
            next_donation=next_date.strftime("%d %B %Y")
        )

    return render_template("register.html", username=session["username"])

# ---------------- DONOR LIST ----------------
@app.route("/donor_list")
def donor_list():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("donor_list.html", donors=donor_table)

# ---------------- REQUEST BLOOD ----------------
@app.route("/request", methods=["GET", "POST"])
def request_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    if request.method == "POST":
        hospital = request.form.get("hospital")
        patient = request.form.get("patient")
        blood = request.form.get("blood_needed")

        request_table.append({
            "hospital": hospital,
            "patient": patient,
            "blood": blood
        })

        session["hospital"] = hospital
        session["patient"] = patient
        session["blood"] = blood

        return redirect(url_for("request_success"))

    return render_template("request.html")


# ---------------- REQUEST SUCCESS ----------------
@app.route("/request_success")
def request_success():
    return render_template("request_success.html",
                           hospital=session.get("hospital"),
                           patient=session.get("patient"),
                           blood=session.get("blood"))

# ---------------- RESPOND ----------------
@app.route("/respond", methods=["GET", "POST"])
def respond():
    if not is_logged_in():
        return redirect(url_for("login"))

    if request.method == "POST":
        session["hospital"] = request.form.get("hospital")
        session["patient"] = request.form.get("patient")
        session["blood"] = request.form.get("blood_needed")
        session["donor"] = request.form.get("donor_name")
        session["phone"] = request.form.get("donor_phone")
        session["donorblood"] = request.form.get("donor_blood")

        return redirect(url_for("confirmation"))

    return render_template("respond.html")

# ---------------- CONFIRMATION ----------------
@app.route("/confirm")
def confirmation():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("confirmation.html",
                           hospital=session.get("hospital"),
                           patient=session.get("patient"),
                           blood=session.get("blood"),
                           donor=session.get("donor"),
                           phone=session.get("phone"),
                           donorblood=session.get("donorblood"))

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("about.html", username=session["username"])

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out!", "success")
    return redirect(url_for("index"))

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users[username] = password
        flash("Account created!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)