
function new_password(){
  var  id = window.location.href;
  var pos = id.search("id");
  var id = id.substr(pos+3,id.length);
  var new_psw = document.getElementById('new_recover_password').value;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(xhttp.responseText);
      if(response.success)
      {
        document.getElementById ("psw_msg").innerHTML = response.msg;
      }
    }

};
let object = {
  id : id,
  new_psw : new_psw
}
  send_request(xhttp,'POST','/recover_change_psw',object,null);
}
// function home(){
//   console.log("kommer vi till home");
//   var xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//       var response = JSON.parse(xhttp.responseText);
//       if(response.success)
//       {
//
//       }
//     }
// send_request(xhttp,'GET','/',null,null);
// };
// 
// }
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
