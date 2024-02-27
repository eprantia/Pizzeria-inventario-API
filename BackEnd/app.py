from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from datetime import date

app = Flask(__name__)
CORS(app)

class Pizzeria:
    def __init__(self, storeName: str, delivery: bool, name: str, stock: int, supplier: str, description: str):
        self.storeName = storeName
        self.delivery = delivery
        self.name = name
        self.stock = stock
        self.supplier = supplier
        self.description = description
        
    def create_dict(self):
        return {
        "storeName": self.storeName,
        "delivery": self.delivery,
        "toppings":[
            {
                "id":1,
                "name":self.name,
                "stock":self.stock,
                "supplier":self.supplier,
                "description":self.description,
                "dateUpdate":date.today().strftime('%d-%m-%Y')
            }
        ]
    }

@app.route('/')
def home():
    return "Bienvenido a mi primera API con Flask!"


# @app.route('/pizzerias' ,methods=['GET'])
# def get_pizzerias():
#     return jsonify([tarea.a_diccionario() for tarea in tareas])

@app.route('/pizzerias/<store>' ,methods=['GET'])
def get_pizzerias(store):
    try:
        with open('./files/pizzeria.json','r') as file:
            # load JSON data from file (as Dict)
            data = json.load(file)
            
            for pizzeria in data['pizzerias']:
                if pizzeria['storeName']==str(store):
                    output = pizzeria
    except:
        print("Lo sentimos, no fue posible completar la operacion.")
    
    return jsonify(output),200


# @app.route('/tareas', methods=['POST'])
# def agregar_tarea():
#     nueva_tarea = Pizzeria(id=request.json['id'],
#                         tittle=request.json['tittle'],
#                         description=request.json['description'])
#     tareas.append(nueva_tarea)
#     return jsonify(nueva_tarea.a_diccionario()),201

@app.route('/pizzerias', methods=['POST'])
def post_pizzerias():
    
    # Variables #
    existStore = False
    new_topping = Pizzeria(request.json['storeName'], request.json['delivery'], request.json['toppings'][0]['name'], 
                           request.json['toppings'][0]['stock'], request.json['toppings'][0]['supplier'], request.json['toppings'][0]['description'])
    new_topping_dict = new_topping.create_dict()
    
    try:
        with open('./files/pizzeria.json', 'r+') as file:
            # First we load existing data into a dict.
            data = json.load(file)
            
            for pizzerias_old in data['pizzerias']:
                #If already exist that pizzeria
                if pizzerias_old['storeName']==new_topping.storeName:
                    existStore = True
                    new_topping_dict['toppings'][0]['id'] = len(pizzerias_old['toppings'])+1
                    #Add new topping to json
                    pizzerias_old["toppings"].append(new_topping_dict['toppings'][0])
                    print("Se agrego otro nuevo topping")

            #If store did not exist add it
            if existStore == False:
                data["pizzerias"].append(new_topping_dict)
                print("Se creo una pizzeria nueva y se le agrego un nuevo topping")
                    
            # Sets file's current position at offset.
            file.seek(0)
            # load JSON data from file (as Dict)
            json.dump(data, file, indent=4)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")

    return jsonify(new_topping_dict),201


# @app.route('/tareas/<int:id>', methods=['PUT'])
# def actualizar_tarea(id):
#     tarea = next((t for t in tareas if t.id == id), None)
#     if tarea is not None:
#         tarea.tittle = request.json.get('tittle', tarea.tittle)
#         tarea.descripcion = request.json.get('description', tarea.descripcion)
#         return jsonify(tarea.a_diccionario())
#     return jsonify({"error": "Tarea no encontrada"}),404

@app.route('/pizzerias/<store>/<int:id>/<var_list>/<val_list>', methods=['PUT'])
def put_pizzerias(store,id,var_list,val_list):
    print("Entro PUT")
    # Variables #
    variables = str(var_list).split(",")
    values = val_list.split(",")
    varChange = False
    
    #Prepare variable type
    for variable in variables:
        if variable == "stock":
            values[variables.index(variable)]=int(values[variables.index(variable)])
    
    try:
        with open('./files/pizzeria.json', 'r') as read_file:
            # First we load existing data into a dict.
            data = json.load(read_file)
            
            for pizzerias_old in data['pizzerias']:
                #Find the same store where we wanna change data
                if pizzerias_old['storeName']==str(store):
                    print("Se encontro la pizzeria")
                    for topping_old in pizzerias_old['toppings']:
                        # If id founded
                        if topping_old['id'] == int(id):
                            print("Se encontro el id del topping")
                            for variable in variables:
                                print(f"Se encontro la variable {topping_old[variable]} y actualizo su valor a {values[variables.index(variable)]}")
                                topping_old[variable] = values[variables.index(variable)]
                                varChange = True

    except:
        print("Lo sentimos, no fue posible completar la operacion.")
        
    try:
        with open('./files/pizzeria.json', 'w') as write_file:
            json.dump(data, write_file, indent=4) 
    except:
        print("Lo sentimos, no fue posible completar la operacion.")
     
    if varChange:       
        return jsonify(data)
    else:
        return jsonify({"error": "Tarea no encontrada"}),404


# @app.route('/tareas/<int:id>', methods=['DELETE'])
# def eliminar_tarea(id):
#     global tareas
#     tareas = [t for t in tareas if t.id != id]
#     return jsonify({'resultado': True})

@app.route('/pizzerias/<store>/<int:id>', methods=['DELETE'])
def delete_pizzerias(store,id):
    
    try:
        with open('./files/pizzeria.json','r') as read_file:
            # load JSON data from file (as Dict)
            data = json.load(read_file)	
            
            for pizzeria in data['pizzerias']:
                # Find store Name
                if pizzeria['storeName']==str(store):
                    print("Se encontro la pizzeria")
                    #If  id greater than 0
                    if id > 0:
                        for toppings in pizzeria['toppings']:
                            #Find topping with id
                            if toppings["id"] == id:
                                print("Se encontro el topping con id=",id)
                                pizzeria['toppings'].remove(toppings)
                                break
                            else:
                                print(f"El topping con id={id} NO Existe")
                                return jsonify({'resultado': False})
                    else:
                        print("El id NO es valido")
            #print(data)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")
        
    try:
        with open('./files/pizzeria.json','w') as write_file:

            json.dump(data,write_file, indent=4)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")
        
    return jsonify({'resultado': True})


@app.errorhandler(404)
def not_found(error):
    return {"error": "Recurso no encontrado"}, 404

if __name__=='__main__':
    app.run(debug=True)