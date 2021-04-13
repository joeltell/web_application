//global id for recover passwords
var recover_id;
displayView = function(){
var div = document.getElementById("view");
};
window.onload = function()
{
  var home_script = document.getElementById("home_script");
  var div = document.getElementById("view");
  var profile_script = document.getElementById("profile_script");
  var recover_script = document.getElementById("recover_script");
  //document.getElementById("result").innerHTML = localStorage.getItem("lastname");
  var usr_token = localStorage.getItem("token");

if(usr_token)
{
  connection_socket(null);
  div.innerHTML = profile_script.innerHTML;
  document.getElementById("home_default").click();
  refresh_wall()
}
else {
  div.innerHTML = home_script.innerHTML;
  //div.innerHTML = recover_script.innerHTML;
}


};

function control_signin()
{
  var name = document.getElementById('uname').value;
  var psw = document.getElementById('password').value;
  let object = {
    email : name,
    password : psw
  };
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
        localStorage.setItem("token",response.data);
        connection_socket(null);
        var profile_script = document.getElementById("profile_script");
        var div = document.getElementById("view");
        div.innerHTML = profile_script.innerHTML;
        document.getElementById("home_default").click();
        refresh_wall();

      }
      else {
        document.getElementById ("usermessage").innerHTML = response.msg;
      }
    }
  };
  send_request(xhttp,'POST','/sign_in',object,null)

}

function connection_socket(str){
  var socket = new WebSocket('ws://127.0.0.1:5000/api');

  socket.onopen = function (){
  console.log("onopen");
  socket.send(JSON.stringify(localStorage.getItem("token")));
  };

  socket.onmessage = function (event) {
    if(JSON.parse(event.data) == "log out")
    {
      console.log(event.data);
      localStorage.removeItem("token");
      var home_script = document.getElementById("home_script");
      var div = document.getElementById("view");
      div.innerHTML = home_script.innerHTML;
    }

    if(event.data == "close")
    {
      console.log(event.data);
      socket.send(JSON.stringify("close"));
    }

  };
  socket.onclose = function (){
    console.log("nu dog socket");
  };
  socket.onerror = function ()
  {
    console.log("nu blev det error");
  }

}

function control_signup() {
  var xhttp;
  var psw = document.getElementById('psw').value;
  var rpsw = document.getElementById('rpassword').value;
  var email = document.getElementById('ename').value;
  var gender = document.getElementById('gender').value;
  var fname = document.getElementById('fname').value;
  var faname = document.getElementById('faname').value;
  var city = document.getElementById('city').value;
  var country = document.getElementById('country').value;

  if( psw != rpsw)
  {
    document.getElementById ("message").innerHTML = "passswords doesnt match!";
  }
  else {


  let object = {
    email: email,
    password: psw,
    firstname: fname,
    familyname: faname,
    gender: gender,
    city: city,
    country: country
};

xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {

    var token = JSON.parse(xhttp.responseText);
    if(token.success)
    {
        document.getElementById ("emailmessage").innerHTML ="created user";
    }
    else {
      document.getElementById ("emailmessage").innerHTML ="couldn't create";
    }
  }
}
  send_request(xhttp,'POST','/sign_up',object,null);

    document.getElementById ("message").innerHTML = "";
    }

}

function display_tab(evt, tabname) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabname).style.display = "block";
  evt.currentTarget.className += " active";

  if(tabname == "Home")
  {
    var email = localStorage.getItem("email");
    if (email === null)
    {
      var xhttp = new XMLHttpRequest();
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var response = JSON.parse(xhttp.responseText);
          if(response.success)
          {
            localStorage.setItem("email",response.data[0]);
            localStorage.setItem("firstname",response.data[1]);
            localStorage.setItem("familyname",response.data[2]);
            localStorage.setItem("country",response.data[5]);
            localStorage.setItem("city",response.data[4]);
            localStorage.setItem("gender",response.data[3]);
            document.getElementById("info1").innerHTML = "email: " + response.data[0];
            document.getElementById("info2").innerHTML = "first name: " + response.data[1];
            document.getElementById("info3").innerHTML = "family name: " + response.data[2];
            document.getElementById("info4").innerHTML = "gender: " + response.data[3];
            document.getElementById("info5").innerHTML = "city: " + response.data[4];
            document.getElementById("info6").innerHTML = "country: " + response.data[5];

          }
        }
      }
      send_request(xhttp,'GET','/get_user_data_by_token',null,localStorage.getItem("token"));
    }
      document.getElementById("info1").innerHTML = "email: " + localStorage.getItem("email");
      document.getElementById("info2").innerHTML = "first name: " + localStorage.getItem("firstname");
      document.getElementById("info3").innerHTML = "family name: " + localStorage.getItem("familyname");
      document.getElementById("info4").innerHTML = "gender: " + localStorage.getItem("gender");
      document.getElementById("info5").innerHTML = "city: " + localStorage.getItem("city");
      document.getElementById("info6").innerHTML = "country: " + localStorage.getItem("country");
}

}

function change_psw()
{
var usr_token = localStorage.getItem("token");
var old_psw = document.getElementById('old_password').value;
var new_psw = document.getElementById('new_password').value;
var r_new_psw = document.getElementById('r_new_password').value;

if( new_psw != r_new_psw)
{
  document.getElementById ("change_message").innerHTML = "passwords doesn't match!";
}
else if (old_psw === new_psw)
{
    document.getElementById ("change_message").innerHTML = "bad input";
}
else
  {
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(xhttp.responseText);
        if (response.success){
          document.getElementById ("change_message").innerHTML = response.msg;
        }
        else{
          document.getElementById ("change_message").innerHTML = response.msg;
        }
      }
    }
    let object = {
      oldPassword : old_psw,
      newPassword : new_psw,
    }
    send_request(xhttp,'POST','/change_password',object,usr_token);
}

}

function sign_out()
{
  var usr_token = localStorage.getItem("token");
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {

        localStorage.removeItem("token");
        localStorage.removeItem("email");
        localStorage.removeItem("firstname");
        localStorage.removeItem("familyname");
        localStorage.removeItem("gender");
        localStorage.removeItem("city");
        localStorage.removeItem("country");

          var home_script = document.getElementById("home_script");
          var div = document.getElementById("view");
          div.innerHTML = home_script.innerHTML;
      }
    }
  }
  send_request(xhttp,'POST','/user_sign_out',null,usr_token);


}

function post_texts()
{
  //var list_message = getUserMessagesByToken(localStorage.removeItem("token"));
  var email = localStorage.getItem("email");
  var token = localStorage.getItem("token");
  var text =  document.getElementById('post_text').value;
  let object = {
    email : email,
    message : text
  }
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
          document.getElementById("text_wall").value += email + ':' +text + "\n";
      }
    }
  }

  send_request(xhttp,'POST','/post_message',object,token)


}
function usr_post_texts()
{
  //var list_message = getUserMessagesByToken(localStorage.removeItem("token"));
  //ladda in alla meddelanden direkt bara när man loggar in och refresh.
  var usr_email = localStorage.getItem("usr_email");
  var email = localStorage.getItem("email");
  var token = localStorage.getItem("token");
  var text =  document.getElementById('usr_post_text').value;
  let object = {
    email : usr_email,
    message : text
  }
  //use post även till sig själv
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
          document.getElementById("usr_text_wall").value += email + ':' + text + "\n";
      }
    }
  }

  send_request(xhttp,'POST','/post_message',object,token)

}

function usr_refresh_wall()
{
  var token = localStorage.getItem("token");
  var foreign_mail = localStorage.getItem("usr_email");
  //fixa så att man kan se alla medd
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
        document.getElementById("usr_text_wall").value = "";
        for (var i = 0; i < response.data.length; ++i)
        {
          document.getElementById("usr_text_wall").value += response.data[i][0] +':' + response.data[i][1]+ "\n";
        }
      }
    }
  }
  var url = '/get_user_messages_by_email?email=' + foreign_mail;
  send_request(xhttp,'GET',url,null,localStorage.getItem("token"));


}

function refresh_wall()
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
        document.getElementById("text_wall").value = "";
        for (var i = 0; i < response.data.length; ++i)
        {
          document.getElementById("text_wall").value += response.data[i][0] +':' + response.data[i][1]+ "\n";
        }
      }
    }
  }
send_request(xhttp,'GET','/get_user_messages_by_token',null,localStorage.getItem("token"));

}

function view_userhome(user_data)
{
    document.getElementById("usr_info1").innerHTML = "email: " + user_data[0];
    document.getElementById("usr_info2").innerHTML = "first name: " +  user_data[1];
    document.getElementById("usr_info3").innerHTML = "family name: " +  user_data[2];
    document.getElementById("usr_info4").innerHTML = "gender: " +  user_data[3];
    document.getElementById("usr_info5").innerHTML = "city: " +  user_data[4];
    document.getElementById("usr_info6").innerHTML = "country: " +  user_data[5];


}

function togglefunc() {

  var email = document.getElementById("email_text").value;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
        localStorage.setItem("usr_email",email);
        var x = document.getElementById("usrhome");
        var y = document.getElementById("searchdiv");
        if (x.style.display === "none" && y.style.display === "block" ) {
          x.style.display = "block";
          y.style.display = "none";
          view_userhome(response.data);
          usr_refresh_wall();
        } else {
            x.style.display = "none";
            y.style.display = "block";
            localStorage.removeItem("usr_email");
        }
      }
      else {
        document.getElementById("usr_warning").innerHTML = "user does not exist!";
      }

    }
  }

  var url = '/get_user_data_by_email?email=' + email;
  send_request(xhttp,'GET',url,null,localStorage.getItem("token"));
}

function send_request(xhttp,method,url,usr_data,token)
{
  xhttp.open(method,url,true);
  if(token != null)
  {
      xhttp.setRequestHeader('Authorization','Bearer ' + token)
  }

  if(method === "POST")
  {
    xhttp.setRequestHeader("Content-type","application/json; charset=utf-8");
    xhttp.send(JSON.stringify(usr_data));
  }
  else {
      xhttp.send();
  }
}

function recover()
{
  var email = document.getElementById('re_ename').value;
  console.log(email);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
          document.getElementById("recover_msg").innerHTML = response.msg;
      }
      else
      {
        document.getElementById("recover_msg").innerHTML = response.msg;
      }
    }

};
let object = {
  email: email
}
send_request(xhttp,'POST','/recover_password',object,null)
}
