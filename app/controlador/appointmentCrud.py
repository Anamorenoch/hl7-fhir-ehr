from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.appointment import Appointment

# Conexión a la colección de citas
collection = connect_to_mongodb("CODIGOAPPOINTMENT", "PEDIR CITA")

def WriteAppointment(appointment_dict: dict):
    try:
        # Validar que cumple el formato FHIR
        appointment = Appointment.model_validate(appointment_dict)
    except Exception as e:
        print("Error validando appointment:", e)
        return f"errorValidating: {str(e)}", None

    # Extraer la hora de inicio
    try:
        appointment_start = appointment.start
    except Exception as e:
        print("Error extrayendo hora de la cita:", e)
        return f"errorExtractingStart: {str(e)}", None

    # Verificar si ya hay una cita a esa hora
    existing_appointment = collection.find_one({
        "start": appointment_start
    })

    if existing_appointment:
        return "appointmentTimeTaken", None

    # Guardar cita nueva
    validated_appointment_json = appointment.model_dump()
    result = collection.insert_one(validated_appointment_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None
