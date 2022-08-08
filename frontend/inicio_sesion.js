function inicio_sesion(idToken){

    let email = document.getElementById('email');
    let password = document.getElementById('password');

    console.log('Correo: ' + email.value);
    console.log('Contraseña: ' + password.value);

    let payload = {
        "username" : email.value,
        "password" : password.value
    }

    var request = new XMLHttpRequest();
    request.open("POST","https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us59.gitpod.io/user/login/",true);
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
            window.location.replace("get_clientes.html");
            sessionStorage.setItem("token", json.userData);
            console.log("Response : " + response);
        }       
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};