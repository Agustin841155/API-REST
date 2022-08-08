function post_cliente(){
    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");

    let payload = {
        "nombre" : nombre.value ,
        "email" : email.value
    }


    console.log ("Nombre : " + nombre.value);
    console.log ("Email : " + email.value);

    var request = new XMLHttpRequest();

    token = sessionStorage.getItem("token");

    request.open('POST',"https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us59.gitpod.io/clientes/",true)
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("content-type", "application/json");

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON    : " + json);
        console.log("Status  : " + status);

        if (status == 202){
            alert(json.message);
            window.location.replace('get_clientes.html');
        }

    };
    request.send(JSON.stringify(payload));
};