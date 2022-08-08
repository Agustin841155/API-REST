function new_user(){

    let email = document.getElementById('email');
    let password = document.getElementById('password');

    console.log('Correo: ' + email.value);
    console.log('Contraseña: ' + password.value);

    let payload = {
        "username" : email.value,
        "password" : password.value,
    }
    var request = new XMLHttpRequest();
    request.open("POST","https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us54.gitpod.io/user/insert/",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON    : " + json);
        console.log("Status   : " + status);

        if (status == 202){
            alert("Usuario creado");
            window.location.replace("index.html");
        }
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};