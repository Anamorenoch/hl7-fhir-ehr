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

    # Convertir la hora 'start' a datetime en UTC
    start_time_str = appointment_dict.get("start")
    start_time = parser.isoparse(start_time_str).astimezone(timezone.utc)

    # Verificar si ya existe una cita exactamente en esa hora UTC
    existing = collection.find_one({"start": start_time})
    if existing:
        return "duplicate", None

    # Insertar si no hay conflicto
    validated_appointment_json = appointment.model_dump()

    # Reescribimos el campo start como UTC
    validated_appointment_json["start"] = start_time

    result = collection.insert_one(validated_appointment_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None

def GetAppointmentsByStart(start: str):
    # Convertir a UTC antes de buscar
    try:
        start_time = parser.isoparse(start).astimezone(timezone.utc)
    except Exception as e:
        print("Error parsing start time:", e)
        return []

    citas = list(collection.find({"start": start_time}))
    return citas
