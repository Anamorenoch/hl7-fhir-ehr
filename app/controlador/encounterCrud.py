from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.encounter import Encounter

# Conectarse a la colección "encounters"
encounter_collection = connect_to_mongodb("Encounter", "Consulta")

def GetEncounterById(encounter_id: str):
    try:
        encounter = encounter_collection.find_one({"_id": ObjectId(encounter_id)})
        if encounter:
            encounter["_id"] = str(encounter["_id"])
            return "success", encounter
        return "notFound", None
    except Exception as e:
        return "notFound", None

def WriteEncounter(encounter_dict: dict):
    try:
        # Validar el recurso HL7 FHIR tipo Encounter
        enc = Encounter.model_validate(encounter_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    validated_encounter_json = enc.model_dump()
    result = encounter_collection.insert_one(validated_encounter_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None
