from app.models import Drone
from app.schemas.drone import ResolvedDrone, ResolvedValue

RESOLVED_FIELDS = (
    "manufacturer",
    "model",
    "variant",
    "category",
    "drone_class",
    "weight_g",
    "max_flight_time_min",
    "max_speed_kmh",
    "battery_type",
    "camera_info",
    "sensor_info",
    "remote_controller",
)


def resolve_drone(drone: Drone) -> ResolvedDrone:
    values: dict[str, ResolvedValue] = {}
    for field in RESOLVED_FIELDS:
        custom_value = getattr(drone, f"custom_{field}")
        template_value = getattr(drone.drone_type, field)
        if custom_value is not None:
            values[field] = ResolvedValue(value=custom_value, source="custom")
        elif template_value is not None:
            values[field] = ResolvedValue(value=template_value, source="template")
        else:
            values[field] = ResolvedValue(value=None, source="unset")
    return ResolvedDrone(
        id=drone.id,
        owner_user_id=drone.owner_user_id,
        drone_type_id=drone.drone_type_id,
        name=drone.name,
        status=drone.status,
        **values,
    )
