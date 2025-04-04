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
        return f"errorValidating: {str(e)}", None

    # Convertir a diccionario limpio y guardar en MongoDB
    validated_appointment_json = appointment.model_dump()
    result = collection.insert_one(validated_appointment_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None
