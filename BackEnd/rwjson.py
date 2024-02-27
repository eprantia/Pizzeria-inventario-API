import json

def getInventories():
    pizzeriaSelected = "Pizzeria Este"
    existStore = False
    
    try:
        with open('./files/pizzeria.json') as file:
            # load JSON data from file (as Dict)
            data = json.load(file)	
            #data = data['pizzerias'][0]
            
            for pizzeria in data['pizzerias']:
                if pizzeria['storeName']==pizzeriaSelected:
                    existStore = True
                    print(pizzeria['storeName'])
                    if pizzeria['delivery']:
                        print("Tenemos entregas a domicilio!")
                    else:
                        print("Lamentablemento no contamos con entregas!")
                        
                    for toppings in pizzeria['toppings']:
                        print(toppings)
            
            if existStore == False:
                print("No existe la pizzeria elegida")
            
    except:
        print("Lo sentimos, no fue posible completar la operacion.")
        
    

def postInventories():
    #Var to check if store already exist
    existStore = False
    
    response={
        "storeName": "Pizzeria Sur",
        "delivery": True,
        "toppings":[
            {
                "id":1, #Se actualiza en el futuro
                "nombre":"chorizo",
                "stock":9,
                "supplier":"chorizo",
                "description":"chorizo",
                "dateUpdate":"21/02/2024"
            }
        ]
    }
    
    try:
        with open('./files/pizzeria.json', 'r+') as file:
            # First we load existing data into a dict.
            data = json.load(file)
            
            for pizzerias_old in data['pizzerias']:
                #If already exist that pizzeria
                if pizzerias_old['storeName']==response['storeName']:
                    existStore = True
                    if (len(pizzerias_old['toppings']) == 1) & (pizzerias_old['toppings'][0]['id'] == 0):
                        pizzerias_old['toppings'][0]['id'] = 1
                        pizzerias_old['toppings'][0]['nombre'] = response['toppings'][0]['nombre']
                        pizzerias_old['toppings'][0]['stock'] = response['toppings'][0]['stock']
                        pizzerias_old['toppings'][0]['supplier'] = response['toppings'][0]['supplier']
                        pizzerias_old['toppings'][0]['description'] = response['toppings'][0]['description']
                        pizzerias_old['toppings'][0]['dateUpdate'] = response['toppings'][0]['dateUpdate']
                        
                    else:
                        #Edit id
                        response['toppings'][0]['id'] = len(pizzerias_old['toppings'])+1
                        pizzerias_old["toppings"].append(response['toppings'][0])
                    #print(response['storeName'])
                    #print(pizzerias_old["toppings"][0])
                    #Add toppings
                    
                    #for topping in pizzerias_old['toppings']:
                    #    print(topping)
            #If store did not exist add it
            if existStore == False:
                data["pizzerias"].append(response)
                    
            print(data)
            # Join new_data with file_data inside emp_details
            #data["pizzerias"].append(response)
            # Sets file's current position at offset.
            file.seek(0)
            # load JSON data from file (as Dict)
            json.dump(data, file, indent=4)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")


def putInventories():
    
    response = {
        "storeName": "Pizzeria Sur",
        "delivery": True,
        "toppings": [
            {
                "id": 2,
                "nombre": "jamon",
                "stock": 10,
                "supplier": "ProvJamon",
                "description": "Jamon de pavo",
                "dateUpdate": "21-02-2024"
            }
        ]
    }
   
    try:
        with open('./files/pizzeria.json', 'r+') as file:
            # First we load existing data into a dict.
            data = json.load(file)
            # Join new_data with file_data inside emp_details
            #data["pizzerias"].append(response)
            
            for pizzerias_old in data['pizzerias']:
                if response['storeName']=="Pizzeria Norte":
                    for topping_old in pizzerias_old['toppings']:
                        if topping_old['id'] == response['toppings'][0]['id']:
                            for key in topping_old.keys():
                                if topping_old[key] != response['toppings'][0][key]:
                                    #Update dict values
                                    topping_old[key] = response['toppings'][0][key]
                                    print("Changes: ",key," & ",response['toppings'][0][key])
                                    
            print(data)
             # Sets file's current position at offset.
            file.seek(0)
            # load JSON data from file (as Dict)
            json.dump(data, file, indent=4)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")


# Just need store and id
def deleteInventories(pizzeriaSelected, id):
    
    try:
        with open('./files/pizzeria.json','r+') as file:
            # load JSON data from file (as Dict)
            data = json.load(file)	
            #data = data['pizzerias'][0]
            
            for pizzeria in data['pizzerias']:
                if pizzeria['storeName']==pizzeriaSelected:
                    for toppings in pizzeria['toppings']:
                        if toppings['id'] == id:
                            toppings['id'] = 0
                            toppings['nombre'] = ""
                            toppings['stock'] = 0
                            toppings['supplier'] = ""
                            toppings['description'] = ""
                            toppings['dateUpdate'] = ""
                            #print(toppings)
            
            print(data)
            # Sets file's current position at offset.
            file.seek(0)
            # load JSON data from file (as Dict)
            json.dump(data, file, indent=4)
    except:
        print("Lo sentimos, no fue posible completar la operacion.")

deleteInventories("Pizzeria Sur", 1)