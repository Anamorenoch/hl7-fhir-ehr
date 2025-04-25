from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.encounter import Encounter
import json

# Conectar a la colección de encounters en MongoDB
collection = connect_to_mongodb("Encounter", "Consulta")

# Función para obtener un Encounter por su ID
def GetEncounterById(encounter_id: str):
    try:
        encounter = collection.find_one({"_id": ObjectId(encounter_id)})
        if encounter:
            encounter["_id"] = str(encounter["_id"])  # Convertir ObjectId a string
            return "success", encounter
        return "notFound", None
    except Exception as e:
        return f"error encontrado: {str(e)}", None

# Función para insertar un Encounter en MongoDB
def WriteEncounter(encounter_dict: dict):
    try:
        # Validar el Encounter con el modelo de FHIR
        enc = Encounter.model_validate(encounter_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    # Convertir el encounter validado a JSON
    validated_encounter_json = enc.model_dump()

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

# Función para obtener un Encounter por identificador (opcional)
def GetEncounterByIdentifier(encounterSystem, encounterValue):
    try:
        encounter = collection.find_one({"identifier.system": encounterSystem, "identifier.value": encounterValue})
        if encounter:
            encounter["_id"] = str(encounter["_id"])  # Convertir ObjectId a string
            return "success", encounter
        return "notFound", None
    except Exception as e:
        return f"error encontrado: {str(e)}", None
