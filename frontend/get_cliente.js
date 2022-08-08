function get_cliente(){
    var id_cliente = window.location.search.substring(1);
    console.log("id_cliente" + id_cliente);

    var request = new XMLHttpRequest();
    token = sessionStorage.getItem("token");

    request.open('GET', 'https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us59.gitpod.io/clientes/'+id_cliente);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token);
    
    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status

        console.log("Response" + response); 
        console.log("JSON" + json);
        console.log("Status" + status);
    
        if(status==202){
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");

            nombre.value = json.nombre;
            email.value = json.email;
        }
        else if(status==404){
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");
            nombre.value = "None";
            email.value = "None";
            alert("Cliente no encontrado");
        }
    };
    request.send();
};