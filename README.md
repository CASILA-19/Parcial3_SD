
(Realmente ni la alcance a probar completamente, la arquitectura esta bien pero tuve un monton de errores con docker que que me quitaron demasiado tiempo y ps paaaila, quiza tambien baste mucho tiempo eligiendo y justificando la arquitectura a utilizarr y bueno... :/tampoco alcance a hacer la otra parte de la simulacion de rabbitMQ)





Clínica Online – Gestión de Citas Médicas
Este proyecto implementa una solución distribuida para la gestión de reservas de citas médicas en una clínica en línea. Utiliza Flask para la API REST, RabbitMQ para procesamiento asíncrono con colas de trabajo y publicación/suscripción, y Docker Compose para la orquestación de servicios.
Funcionalidades

    Crear una cita médica a través de la API REST.

    Procesamiento asíncrono de confirmación o rechazo de citas.

    Notificación del resultado mediante sistema de suscripción.

    Consulta del estado actual de una cita.

    Arquitectura tolerante a fallos y escalable horizontalmente.

Endpoints

    POST /book: Crea una nueva cita. Requiere datos del paciente y franja horaria.

    GET /booking/{id}: Consulta el estado de una cita (pending, confirmed, rejected).

Arquitectura

Servicios involucrados:

    flask-api: API principal.

    rabbitmq: Broker de mensajes.

    booking-processor: Encola solicitudes de citas.

    confirmer: Simula confirmación médica con retraso aleatorio.

    rejector: Simula rechazo en caso de indisponibilidad.

    notifier: Publica notificaciones a un exchange.
Tecnologías:

    Flask

    RabbitMQ

    Docker & Docker Compose

    Python 3.9
    SQlite
Diseño de Mensajes

    Los mensajes que viajan en RabbitMQ usan formato JSON y contienen:

    {
      "booking_id": "uuid",
      "patient": "Nombre",
      "slot": "2024-05-14 14:00",
      "status": "pending"
    }

Reintentos y Tolerancia a Fallos

    Se aplican hasta 3 reintentos en la simulación de disponibilidad médica.

    Si un worker falla, RabbitMQ reenviará el mensaje automáticamente gracias al ack manual.

    Las notificaciones se enrutan mediante un exchange tipo direct.

    Los mensajes que superan los reintentos se redirigen a una Dead Letter Queue (DLQ) para monitoreo.
