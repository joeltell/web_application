import sqlite3
from flask import g,Flask, request
from uuid import uuid4

app = Flask(__name__)

DATABASE_URI = "database.db"

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)
    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_user(data):
    if find_user(data["email"]) != None:
        return False
    else:
        get_db().execute("INSERT INTO user VALUES(?,?,?,?,?,?,?)",[data["email"],data["password"],data["firstname"],data["familyname"],data["gender"],data["city"],data["country"]])
        get_db().commit()
        return True


def find_user(email):
    cursor = get_db().execute("SELECT email FROM user WHERE email = ? ", [email])
    result = cursor.fetchone()
    if (result == None):
        cursor.close()
        return None
    else:
        cursor.close()
        return result[0]

def validate_user(email,token):
    if email != None:
        cursor = get_db().execute("SELECT * FROM user WHERE email = ?",[email])
        result = cursor.fetchone()
        if result == None:
            cursor.close()
            return False
    cursor = get_db().execute("SELECT * FROM active_users WHERE token = ?",[token])
    result = cursor.fetchone()
    if result == None:
        cursor.close()
        return False
    return True

def create_post(data,token):
    try:
        cursor = get_db().execute("SELECT email FROM active_users WHERE token = ?", [token])
        result = cursor.fetchone()
        sender = result[0]
        cursor = get_db().execute("INSERT INTO user_messages(reciever,message,sender) VALUES(?,?,?)",[data["email"],data["message"],sender])
        get_db().commit()
        cursor.close()
        return True
    except:
        return False

def get_msg(email,token):
    if email == None:
        cursor = get_db().execute("SELECT email FROM active_users WHERE token = ?", [token])
        result = cursor.fetchone()
        if result == None:
            cursor.close()
            return ""
        email = result[0]

    cursor = get_db().execute("SELECT sender, message FROM user_messages WHERE reciever = ?", [email])
    result = cursor.fetchall()
    if (result == None):
        cursor.close()
        return ""
    all_msg = ""
    all_msg = [x[0:2] for x in result]
    cursor.close()
    return all_msg;



def validate_input(data):
    if data["email"] == "":
        return True
    if len(data["password"]) < 5:
        return True
    if data["password"] == "":
        return True
    if data["firstname"] == "":
        return True
    if data["familyname"] == "":
        return True
    if data["gender"] == "":
        return True
    if data["city"] == "":
        return True
    if data["country"] == "":
        return True

def get_data(email,token):
    try:
        if email == None:
            cursor = get_db().execute("SELECT email FROM active_users WHERE token = ?",[token])
            result = cursor.fetchone()
            if result == None:
                cursor.close()
                return None
            email = result[0]
        cursor = get_db().execute("SELECT email, firtname, familyname, gender, city, country FROM user where email = ?",[email])
        result = cursor.fetchone()
        cursor.close()
    except:
        print("active_user already deleted")
    return result

def change_pw(data,token):
    cursor = get_db().execute("SELECT email FROM active_users WHERE token = ?",[token])
    result = cursor.fetchone()
    email = result[0]
    cursor = get_db().execute("SELECT password FROM user WHERE password = ? AND email = ?",[data["oldPassword"],email])
    result = cursor.fetchone()
    if result == None:
        cursor.close()
        return False
    cursor = get_db().execute("UPDATE user SET password = ? WHERE password = ? AND email = ?",[data["newPassword"],data["oldPassword"],email])
    get_db().commit()
    cursor.close()
    return True

def recover_change_pw(email,password):
    cursor = get_db().execute("UPDATE user SET password = ? WHERE email = ?",[password,email])
    get_db().commit()
    cursor.close()
    return True

def remove_user(token):
        cursor = get_db().execute("DELETE FROM active_users WHERE token = ?",[token])
        get_db().commit()
        cursor.close()

def sign_in_check(data):
    if data["email"] == find_user(data["email"]):
        cursor = get_db().execute("SELECT password FROM user WHERE email = ?",[data["email"]])
        result = cursor.fetchone()
        if(result == None):
            cursor.close()
            return ""
        result = result[0]
        cursor.close()
        if(data["password"] == result):
            usr_token = uuid4()
            cursor = get_db().execute("SELECT * FROM active_users WHERE token = ?",[str(usr_token)])
            result = cursor.fetchone()
            if(result != None):
                #recursive call for already existing token
                cursor.close()
                sign_in_check()
            try:
                cursor = get_db().execute("INSERT INTO active_users VALUES(?,?)",[data["email"],str(usr_token)])
                get_db().commit()
            except sqlite3.IntegrityError as e:
                cursor = get_db().execute("INSERT OR REPLACE INTO active_users VALUES(?,?)",[data["email"],str(usr_token)])
                get_db().commit()


            cursor.close()
            return usr_token
    return ""
