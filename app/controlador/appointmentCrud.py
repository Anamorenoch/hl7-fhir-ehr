from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.appointment import Appointment
from dateutil import parser
from datetime import datetime, timezone, timedelta

# Conexión a la colección de citas
collection = connect_to_mongodb("CODIGOAPPOINTMENT", "PEDIR CITA")

def WriteAppointment(appointment_dict: dict):
    try:
        # Validar que cumple el formato FHIR
        appointment = Appointment.model_validate(appointment_dict)
    except Exception as e:
        print("Error validando appointment:", e)
        return f"errorValidating: {str(e)}", None

    # Convertir 'start' a datetime en UTC
    start_time_str = appointment_dict.get("start")
    start_time = parser.isoparse(start_time_str).astimezone(timezone.utc)
    end_time = start_time + timedelta(minutes=30) 

    #Verificar si ya existe una cita en ese rango
    conflict = collection.find_one({
        "start": {"$lt": end_time},
        "end": {"$gt": start_time}
    })
 
    if conflict:
        return "duplicate", None

    # Insertar si no hay conflicto
    validated_appointment_json = appointment.model_dump()
    validated_appointment_json["start"] = start_time
    validated_appointment_json["end"] = end_time


    result = collection.insert_one(validated_appointment_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None

