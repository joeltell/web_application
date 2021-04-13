from flask import Flask, jsonify, request
import requests
import database_helper

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    db = database_helper.get_db()
    database_helper.init_db()
    return app.send_static_file('client.html')



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

def get_token():
    token = request.headers.get('Authorization')
    token = token.split()
    token = token[1]
    return token

if __name__ == "__main__":
   app.run(debug=True)
