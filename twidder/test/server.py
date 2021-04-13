from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request
import json
#import requests
from flask_mail import Mail, Message
import database_helper

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'twidder12@gmail.com'
app.config['MAIL_PASSWORD'] = 'Y5wQ8iBQTyyBTtV'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#global variable with active sessions
active_sessions = dict()
recover_dict = dict()
@app.route('/', methods=['GET'])
def main():
    db = database_helper.get_db()
    database_helper.init_db()
    #return render_template('static/client.html')
    return app.send_static_file('client.html')

@app.route('/api')
def api():
    print("kommer vi till server api")
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        token = ws.receive()
        token = token.replace('"','')
        email = database_helper.get_data(None,token)[0]
        print(email)
        print(token)
        print(active_sessions)
        if email in active_sessions:
            try:
                print(active_sessions[email][0])
                active_sessions[email][0].send(json.dumps("log out"))
                print("email in active session??")
            except:
                print("if resfresh, session dies")
            del active_sessions[email]
    active_sessions[email] = [ws,token]
    try:
        while True:
            msg = active_sessions[email][0].receive()
            if(msg == "close"):
                print("close connection")
                msg = active_sessions[email][0].close()
                database_helper.remove_user(active_sessions[email][1])
                del active_sessions[email]
                break
    except:
        print("session died while waiting for connection close msg")

    return ""

@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    if database_helper.validate_input(data):
        return jsonify({"success": False,"msg" : "bad input"})

    result = database_helper.add_user(data)
    if result == True:
        return jsonify({"success": True,"msg":"user registrated"})
    else:
        return jsonify({"success": False, "msg" : "user registration failed"})



@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    usr_token = database_helper.sign_in_check(data)
    if usr_token == "":
        return jsonify({"success": False, "msg" : "could not sign in"})

    return jsonify({"success": True,"msg":"logged in", "data" : usr_token})

@app.route('/user_sign_out', methods=['POST'])
def user_sign_out():
    token = get_token()
    email = database_helper.get_data(None,token)[0]
    try:
        active_sessions[email][0].send("close")
        del active_sessions[email]
    except:
        print("log out")
    if not database_helper.validate_user(None,token):
        return jsonify({"success":False,"msg" : "Unauthorized"})
    database_helper.remove_user(token)
    return jsonify({"success":True,"msg" : "user logged out"})


@app.route('/change_password',methods=['POST'])
def change_password():
    data = request.get_json()
    token = get_token()
    if not database_helper.validate_user(None,token):
        return jsonify({"success":False,"msg" : "Unauthorized"})


    if database_helper.change_pw(data,token):
        return jsonify({"success":True,"msg" : "password changed"})
    else:
        return jsonify({"success":False,"msg" : "password did not change"})

@app.route('/get_user_data_by_token',methods=['GET'])
def get_user_data_by_token():
    #recieve token
    token = get_token()
    #display all user for the user with the correct token
    #find the active user with correlating token
    if not database_helper.validate_user(None,token):
        return jsonify({"success":False,"msg" : "Unauthorized"})
    #select data with the correct user
    result = database_helper.get_data(None,token)
    if result == None:
        return jsonify({"success":False,"msg" : "Unable to find user"})

    return jsonify({"success": True,"msg":"found user data","data" : result})

#Returns a full row in user table
@app.route('/get_user_data_by_email',methods=['GET'])
def get_user_data_by_email():
    #recieve email and token
    token = get_token()
    email = request.args.get('email')
    if not database_helper.validate_user(None,token):
        return jsonify({"success":False,"msg":"Unauthorized"})
    #check if the user is active
    result = database_helper.get_data(email,token)
    if result == None:
        return jsonify({"success":False,"msg":"no data found"})
        #get the result from user table
    return jsonify({"success": True,"msg":"found user data","data" : result})


#returns all messages for the current user
@app.route('/get_user_messages_by_token',methods=['GET'])
def get_user_messages_by_token():
    token = get_token()
    if not database_helper.validate_user(None,token):
        return jsonify({"success":False,"msg":"Unauthorized"})
    #retrieve all your own messages
    all_msg = database_helper.get_msg(None,token)
    if all_msg == "":
        return jsonify({"success":False,"msg":"no messages found"})
    #return string as a json object
    return jsonify({"success": True,"msg":"found user messages","data" : all_msg})

@app.route('/get_user_messages_by_email',methods=['GET'])
def get_user_messages_by_email():
    #data = request.get_json()
    email = request.args.get('email')
    token = get_token()
    if not database_helper.validate_user(email,token):
        return jsonify({"success":False,"msg":"Unauthorized"})
    all_msg = database_helper.get_msg(email,token)
    if(all_msg == ""):
        return jsonify({"success":False,"msg":"no messages found"})
    return jsonify({"success": True,"msg":"found user messages","data" : all_msg})

#try to post a message to someoneelse
@app.route('/post_message',methods=['POST'])
def post_message():
    data = request.get_json()
    token = get_token()
    if database_helper.find_user(data["email"]) != data["email"]:
        return jsonify({"success":False,"msg":"could not find user"})
    if not database_helper.validate_user(data["email"],token):
        return jsonify({"success":False,"msg":"Unauthorized"})
    if not database_helper.create_post(data,token):
        return jsonify({"success":False,"msg":"could not send msg"})
    return jsonify({"success":True,"msg":"message sent"})

@app.route('/recover_password',methods=['POST','GET'])
def recover_password():
    if request.method == 'POST':
        #generate id
        recover_id = str(len(recover_dict)+1)
        data = request.get_json()
        email = data["email"]
        if database_helper.find_user(email) != None:
            recover_dict[recover_id] = email
            msg = Message("http://127.0.0.1:5000/recover_password?id="+recover_id,sender = "twidder12@gmail.com",
                          recipients=[email])
            mail.send(msg)
            return jsonify({"success":True,"msg":"message sent","data":recover_id})
        else:
            return jsonify({"success":False,"msg":"not a valid user"})
    else:
        print("GET")
        id = request.args.get('id')
        if id in recover_dict:
            return app.send_static_file('recover_password_view.html')
        else:
            return jsonfify({"success":False,"msg":"wrong id"})

        #return jsonify({"success": True, "msg":"get function"})
    #gene
@app.route('/recover_change_psw',methods=['POST'])
def recover_change_psw():
    data = request.get_json()
    email = recover_dict[data["id"]]
    new_psw = data["new_psw"]
    del recover_dict[data["id"]]

    print(email)
    if database_helper.recover_change_pw(email,new_psw):
        return jsonify({"success":True,"msg":"password changed"})
    else:
        return jsonify({"success":False,"msg":"password did not change"})


def get_token():
    token = request.headers.get('Authorization')
    token = token.split()
    token = token[1]
    return token

if __name__ == "__main__":
    http_server = WSGIServer(('127.0.0.1',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run(debug=True)
