function deleteCliente(){

    var request = new XMLHttpRequest();

    
    let id_cliente = window.location.search.substring(1);
    console.log('Id : ' + id_cliente);

    token = sessionStorage.getItem("token");

    let payload = {
        "id_cliente" : id_cliente.value
    }

    request.open('DELETE','https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us59.gitpod.io/clientes/' + id_cliente, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("content-type", "application/json");
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON     : " + json);
        console.log("Status   : " + status);


    };
    request.send(JSON.stringify(payload));
};