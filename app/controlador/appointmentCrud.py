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

    start_time = appointment_dict.get("start")

    # Verificar si ya existe una cita con el mismo horario
    existing = collection.find_one({"start": start_time})
    if existing:
        return "duplicate", None

    # Insertar si no hay conflicto
    validated_appointment_json = appointment.model_dump()
    result = collection.insert_one(validated_appointment_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None
# appointmentCrud.py
def GetAppointmentsByStart(start: str):
    citas = list(collection.find({"start": start}))
    return citas
