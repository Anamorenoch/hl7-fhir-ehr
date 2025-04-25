from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.encounter import Encounter
import json

# Conectar a la colección de encounters en MongoDB
collection = connect_to_mongodb("Encounter", "Consulta")

def WriteEncounter(encounter_dict: dict):
    try:
        # Validar el Encounter con el modelo de FHIR
        enc = Encounter.model_validate(encounter_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    # Asegurarse de que 'class' sea una lista
    if not isinstance(encounter_dict.get('class'), list):
        encounter_dict['class'] = [encounter_dict['class']]

    # Asegurarse de que 'period' tenga el formato adecuado
    if 'period' in encounter_dict:
        encounter_dict['period'] = {
            'start': encounter_dict['period'].get('start'),
            'end': encounter_dict['period'].get('end')
        }

    # Convertir el encounter validado a JSON
    validated_encounter_json = encounter_dict  # No es necesario volver a validar si ya pasaron las validaciones

    try:
        # Insertar el encounter en MongoDB
        result = collection.insert_one(validated_encounter_json)
        if result:
            inserted_id = str(result.inserted_id)  # Obtener el ID insertado
            return "success", inserted_id
        else:
            return "errorInserting", None
    except Exception as e:
        return f"errorInserting: {str(e)}", None
