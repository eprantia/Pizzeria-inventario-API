
// Variables
let pizzeriaSelected = "";
let pizzeriaDelivery = false;
let id = 1;
let topping = "";
let quantity = 0;
let supplier = "";
let description = "";
// let date = "";
// let result
// let lastRowNumber = 0

// Inicial conditions
document.getElementById('buttonCreate').style.visibility = 'hidden';



//####################################################################################################################
//                                                 GET
//####################################################################################################################
function getInfo(pizzeriaSelected){
    console.log(`Iniciando GET`);
    const urlGet = new URL(`http://127.0.0.1:5000/pizzerias/${pizzeriaSelected}`);
    //fetching API across the network
    var oldState = fetch(urlGet).then(res => res.json())
        .then(data => {
            const list = document.getElementsByClassName("listToppings")[0];
            
            console.log("list.length ", list.length);
            if(data['toppings'].length > 0){
                console.log("Dentro condicion");
                // Clean
                list.deleteRow(0);
            }
            // list.deleteRow(0);
            
            // oldState = data['toppings'].length;
            console.log("Numero de rows: ", data['toppings'].length);
            //Go trough all items
            for (let i = 0; i < data['toppings'].length; i++){
                // Create row with new info
                list.insertRow().innerHTML = `
                    <td>${data['toppings'][i]['id']}</td>
                    <td>${data['toppings'][i]['name']}</td>
                    <td>${data['toppings'][i]['stock']}</td>
                    <td>${data['toppings'][i]["supplier"]}</td>
                    <td>${data['toppings'][i]["description"]}</td>
                    <td>${data['toppings'][i]["dateUpdate"]}</td>
                    <td>
                        <input class="btnEdit" id="buttonEdit${i+1}" type="button" value="Editar"/>
                        <input class="btnDelete" id="buttonDelete${i+1}" type="button" value="Borrar"/>
                    </td>
                `;  
                
                // If receive a non empty name create addEventListener click in "EDIT" and "DELETE" buttons
                if (data['toppings'][i]['name']){
                    // Detect click "EDIT" button ==================================================
                    document.getElementById(`buttonEdit${i+1}`).addEventListener("click", function() {
                        console.log(`button EDIT was clicked`);
                        //id = i+1;
                        // Run [PUT]
                        putInfo(pizzeriaSelected,i+1);
                    });
                    // Detect click "DELETE" button ================================================
                    document.getElementById(`buttonDelete${i+1}`).addEventListener("click", function() {
                        console.log(`button DELETE was clicked`);
                        //id = i+1;
                        // Run [DELETE]
                        deleteInfo(pizzeriaSelected,i+1)
                    });
                }
            }
        })
        return oldState;
}
//####################################################################################################################
//                                                 POST
//####################################################################################################################
function postInfo(pizzeriaSelected){
    console.log(`Iniciando POST`);
    const urlPost = new URL(`http://127.0.0.1:5000/pizzerias`);
    //fetching API across the network
    fetch(urlPost,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "storeName": pizzeriaSelected,
            "delivery": pizzeriaDelivery,
            "toppings": [
                {
                    "name": topping,
                    "stock": quantity,
                    "supplier": supplier,
                    "description": description
                }
            ]
        })
    }).then(res => {
        if(res.ok){
            console.log("SUCCESS");
            document.getElementById('idPizzeriasSelect').selectedIndex = "0";
        }else{
            console.log("Not Successful");
        }
    })
    .then(data => console.log(data))
    .catch(error => console.log("ERROR"));

}
//####################################################################################################################
//                                                 PUT
//####################################################################################################################
function putInfo(pizzeriaSelected,id){
    console.log(`Iniciando PUT`);
    let top = topping;
    let sto = document.getElementById("quantityTopping").value;
    let sup = document.getElementById("supplierTopping").value;
    let des = document.getElementById("descriptionTopping").value;

    //fetching API across the network
    const urlPut = new URL(`http://127.0.0.1:5000/pizzerias/${pizzeriaSelected}/${id}/name,stock,supplier,description/${top},${sto},${sup},${des}`);
    console.log(urlPut);
    fetch(urlPut,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "storeName": pizzeriaSelected,
            "delivery": pizzeriaDelivery,
            "toppings": [
                {
                    "name": topping,
                    "stock": document.getElementById("quantityTopping").value,
                    "supplier": document.getElementById("supplierTopping").value,
                    "description": document.getElementById("descriptionTopping").value
                }
            ]
        })

    }).then(res => {
        if(res.ok){
            console.log("SUCCESS");
            document.getElementById('idPizzeriasSelect').selectedIndex = "0";
        }else{
            console.log("Not Successful");
        }
    })
    .then(data => console.log(data))
    .catch(error => console.log("ERROR"));
    //Clear input fields
    clearPopup();
}
//####################################################################################################################
//                                                 DELETE
//####################################################################################################################
function deleteInfo(pizzeriaSelected,id){
    console.log(`Iniciando DELETE`);
    const urlPut = new URL(`http://127.0.0.1:5000/pizzerias/${pizzeriaSelected}/${id}`);
    //fetching API across the network
    fetch(urlPut,{method: 'DELETE'})
        .then(() => element.innerHTML = 'Delete successful');
    alert("Ingrediente eliminado")
}


//##########################################################################################################
//                                             HEADER
//##########################################################################################################
// Detect if id=idPizzeriasSelect changes ======================================
let myPizzeriaSelect = document.getElementById('idPizzeriasSelect');
myPizzeriaSelect.onchange = (event) => {
     pizzeriaSelected = event.target.value;
     console.log("pizzeria: ",pizzeriaSelected);
     // Run [GET]
     getInfo(pizzeriaSelected);
 }

// Detect state checkbox of delivery ===========================================
let checkbox = document.getElementById("delivery");
checkbox.addEventListener( "change", () => {
    if ( checkbox.checked ) {
        pizzeriaDelivery = true;
        console.log("Delivery ON");
    } else {
        pizzeriaDelivery = false;
        console.log("Delivery OFF");
    }
});

// Detect click "NEW" button ===================================================
document.getElementById('buttonNew').addEventListener("click", function() {
    console.log("button NUEVO was clicked");
    // Show CREATE button if already select a pizzeria
    if (document.getElementById('idPizzeriasSelect').selectedIndex != 0){
        console.log("Se muestra el boton CREATE");
        document.getElementById('buttonCreate').style.visibility = 'visible';
    }else{
        console.log("Selecciona una pizzeria");
    }

});


//##########################################################################################################
//                                             POPUP
//##########################################################################################################

// Detect which topping was selected =============================================================
let myToppingSelect = document.getElementById('idToppingSelect');
myToppingSelect.onchange = (event) => {
    topping = event.target.value;
 }

// Detect click "CREATE" button ==========================================================================
document.getElementById('buttonCreate').addEventListener("click", function() {
    console.log("button CREATE was clicked");

    //Get values
    quantity = document.getElementById("quantityTopping").value; 
    supplier = document.getElementById("supplierTopping").value; 
    description = document.getElementById("descriptionTopping").value; 

    //Condition NO EMPTY fields
    if (topping == "" || quantity == 0 || supplier == ""){
        console.log("Porfavor llena todos los campos");
        alert("Porfavor llena todos los campos")
    }else{
        //Info adding...
        console.log("topping: ",topping);
        console.log("quantityTopping: ", quantity);
        console.log("supplierTopping: ", supplier);
        console.log("descriptionTopping: ", description);
        //Clear input fields
        clearPopup();
        // Run [POST]
        postInfo(pizzeriaSelected);
        // Run [GET]
        getInfo(pizzeriaSelected);
        //Hide CREAR button
        document.getElementById('buttonCreate').style.visibility = 'hidden';
    }

});

//Put all input fields empty or 0
function clearPopup(){
    document.getElementById('idToppingSelect').selectedIndex = 0;
    document.getElementById("quantityTopping").value = ""; 
    document.getElementById("supplierTopping").value = ""; 
    document.getElementById("descriptionTopping").value = ""; 
}



