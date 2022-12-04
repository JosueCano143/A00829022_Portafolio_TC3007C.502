menu =  {   
    # Postre
    "Arroz con leche":30,
    "Pastel de chocolate":35,
    "Fresas con crema":35,
    "Gelatina":20, 
    "Flan":30,    
    # Bebida
    "Refresco":23,
    "Agua":20,
    "Jamaica":24,
    "Horchata":24,
    "Cerveza en botella":33,
    "Cerveza en barril":33,
    "Cerveza en litro":80,
    "Michelada de litro":90,
    "Michelato de litro":90,
    # Comida
    "Alambre Vegetariano":115,
    "Alambre de Pechuga":120,     
    "Alambre de Bistec":120,                                         
    "Alambre de Chuleta":120,                                         
    "Alambre de Costilla":130,                                         
    "Alambre de Arrachera":145,                                         
    "Costras de Pastor":30,                                         
    "Costras de Pechuga":35,                                         
    "Costras de Bistec":35,                                        
    "Volcanes de Pastor":22,                                         
    "Volcanes de Bistec":28,                                         
    "Tortas de Pastor":50,                                         
    "Tortas de Maciza":50,                                         
    "Tortas de Suadero":50,                                         
    "Tortas de Longaniza":50,                                         
    "Tortas de Pechuga":50,                                         
    "Tortas de Bistec":65,                                         
    "Tortas de Chuleta":65                                    
}

def get_slots(intent_request):
    return intent_request['interpretations']['intent']['slots']


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def order_food(intent_request):
    slots = get_slots(intent_request)
    platillo = slots["platillo"]["interpretedValue"]
    bebida = slots["bebida"]["interpretedValue"]
    postre = slots["postre"]["interpretedValue"]

    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': f"{menu[platillo]+menu[bebida]+menu[postre]}"})


def dispatch(intent_request):
    print(intent_request)
    return order_food(intent_request)


def lambda_handler(event, context):
    return dispatch(event)
