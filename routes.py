from app import app
from flask import render_template, request, redirect, url_for
import messages
import users

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html") 
    if request.method == "POST":
        username = request.form["username"] 
        password = request.form["password"]
        if users.old_user_login(username, password):
            return redirect("/") 
        else:
            return render_template("error_info.html", message="Either your username is wrong, or your password is wrong. Try again")

@app.route("/")
def index():
    try:
        customers, number = messages.front_page_view()
        return render_template("frontpage.html", customers=customers, number=number)
    except ValueError as e:
        print(f"Error: {e}")
        return redirect("/login")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password_1"]
        password2 = request.form["password_2"]
        if password1 != password2:
            return render_template("error_info.html", message="There is a difference between your first and second password. Try again")
        if password1 == password2:
            users.new_user_registration(username, password1)
            print(f"Username: {username} ja Password: {password1}")
            return redirect("/")
        else:
            return render_template("error_info.html", message="Something went wrong.. Sorry! Try again") 
        
@app.route("/newcustomer", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        return render_template("newcustomer.html") 
    if request.method == "POST":
        name = request.form["name"]
        sex = request.form["sex"]
        language = request.form["language"]
        age_group = request.form["age_group"]
        phone = request.form["phone"]
        email = request.form["email"]
        if messages.new_customer_registration(name, sex, language, age_group, phone, email):
            return redirect("/")
        else:
            return render_template("error_info.html", message="Adding a new customer to the database failed")
        
@app.route("/newmeeting/<int:id>", methods=["GET", "POST"])
def new_meeting(id):
    id, name = messages.customer_name(id) 
    if request.method == "GET":
        return render_template("newmeeting.html", id=id, name=name)
    if request.method == "POST":
        date = request.form["date"]
        service_id = request.form["service_id"]
        customer_id = request.form["customer_id"]
        customer_path = request.form["customer_path"]
        realization_id = request.form["realization_id"]
        execution_id = request.form["execution_id"]
        notes = request.form["notes"]
        if messages.new_meeting_registration(date,service_id,customer_id,customer_path,realization_id,execution_id,notes):
            return redirect("/")
        else:
            return render_template("error_info.html", message="Adding a new meeting to the database failed")

@app.route("/seenotes/<int:id>", methods=["GET"])
def seenotes(id):
    id, name = messages.customer_name(id) 
    notes, number = messages.see_notes(id)
    return render_template("seenotes.html", id=id, notes=notes, name=name, number=number)

@app.route("/modifycustomer/<int:id>", methods=["GET", "POST"])
def modify_customer(id):
    id, name = messages.customer_name(id) 
    if request.method == "GET":
        return render_template("customermodification.html", id=id, name=name)
    if request.method == "POST":
        name = request.form["name"]
        sex = request.form["sex"]
        language = request.form["language"]
        age_group = request.form["age_group"]
        phone = request.form["phone"]
        email = request.form["email"]
        if messages.customer_modification(id, name, sex, language, age_group, phone, email):
            return redirect("/")
        else:
            return render_template("error_info.html", message="Modifying the customer information failed")
        
@app.route('/stats', methods=["GET", "POST"])
def plots():
    called_count, canceled_count = messages.meeting_numbers()
    if request.method == "GET":
        return render_template("stats_template.html", called_count=called_count, canceled_count=canceled_count)
    if request.method == "POST":
        realization = request.form.get('realization')
        service = request.form.get('service')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        execution_style = request.form.get('execution_style')
        
        pic_0, pic_1, pic_2 = messages.plots(realization,service,start_date,end_date,execution_style)
        called_count, canceled_count = messages.meeting_numbers()

        return render_template("stats_template.html", pic_0=pic_0, pic_1=pic_1, pic_2=pic_2, called_count=called_count, canceled_count=canceled_count)
