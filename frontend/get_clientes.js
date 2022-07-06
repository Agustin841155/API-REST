function get_clientes(){
    var query = window.location.search.substring(1);
    console.log("Query" + query);
    var request = new XMLHttpRequest();
    var username = "admin";
    var password = "admin";

    request.open('GET', 'https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us51.gitpod.io/clientes/');
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
        </tr>
    `;

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response" + response); 
        console.log("JSON" + json);
        for (let i = 0; i < json.length; i++){
            var tr = document.createElement("tr");
            var id_cliente = document.createElement("td");
            var nombre = document.createElement("td");
            var email = document.createElement("td");

            id_cliente.innerHTML = json[i].id_cliente;
            nombre.innerHTML = json[i].nombre;
            email.innerHTML = json[i].email;

            tr.appendChild(id_cliente);
            tr.appendChild(nombre);
            tr.appendChild(email);
    
            tableBody.appendChild(tr);
        }

        tabla.appendChild(tableHead);
        tabla.appendChild(tableBody);

    };
    request.send();
};