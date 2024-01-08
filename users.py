from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

def old_user_login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False, None  # Return a tuple indicating login failure
    
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id  # Set user_id in the session
            session["username"] = username # Set username in the session
            return True, user.id  # Return a tuple indicating login success
        else:
            return False, None  # Return a tuple indicating login failure

def logout(): 
    del session["user_id"]

def new_user_registration(username, password): 
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return old_user_login(username, password)

def user_id():
    return session.get("user_id",0) # If the user is not in the database, user_id is set to zero. And user_id = 0 raises errors
