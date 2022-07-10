function get_clientes(){
    var query = window.location.search.substring(1);
    console.log("Query" + query);
    var request = new XMLHttpRequest();
    var username = "admin";
    var password = "admin";

    request.open('GET', 'https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us53.gitpod.io/clientes/');
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");

    const tabla = document.getElementById("tabla_clientes");
    var tableHead = document.createElement("thead");
    var tableBody = document.createElement("tbody");

    
    tableHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Detalle</th>
            <th>Actualizar</th>
            <th>Eliminar registro</th>
        </tr>
    `;

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response" + response); 
        console.log("JSON" + json);
        for (let i = 0; i < json.length; i++){
            var tr = document.createElement("tr");
            var detalle = document.createElement("td")
            var id_cliente = document.createElement("td");
            var nombre = document.createElement("td");
            var email = document.createElement("td");
            var actualizar = document.createElement("td");
            var eliminar = document.createElement("td");

            id_cliente.innerHTML = json[i].id_cliente;
            nombre.innerHTML = json[i].nombre;
            email.innerHTML = json[i].email;
            detalle.innerHTML = "<a href='/get_cliente.html?"+json[i].id_cliente+"'>Detalle</a>";
            actualizar.innerHTML = "<a href=put_cliente.html?"+json[i].id_cliente+">Actualizar</a>";
            eliminar.innerHTML = "<button onclick=delete_cliente("+json[i].id_cliente+")>Eliminar</button>";



            tr.appendChild(id_cliente);
            tr.appendChild(nombre);
            tr.appendChild(email);
            tr.appendChild(detalle);
            tr.appendChild(actualizar);
            tr.appendChild(eliminar);
    
            tableBody.appendChild(tr);
        }

        tabla.appendChild(tableHead);
        tabla.appendChild(tableBody);

    };
    request.send();
};
function delete_cliente(id_cliente){

    var request = new XMLHttpRequest();

    console.log('Id: ' + id_cliente);

    var username = "admin";
    var password = "admin";

    request.open('DELETE','https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us53.gitpod.io/clientes/' + id_cliente, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON     : " + json);
        console.log("Status   : " + status);

        if (status == 202){
            alert(json.message);
            window.location.replace('get_clientes.html');
        }


    };
    request.send();
};