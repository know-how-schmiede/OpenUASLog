from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_template_drone_flight_workflow(client: TestClient, auth_headers: dict[str, str]):
    drone_type_response = client.post(
        "/api/drone-types",
        headers=auth_headers,
        json={
            "manufacturer": "DJI",
            "model": "Mavic 3",
            "variant": "Classic",
            "weight_g": 895,
            "max_flight_time_min": 46,
        },
    )
    assert drone_type_response.status_code == 201
    drone_type_id = drone_type_response.json()["id"]

    drone_response = client.post(
        "/api/drones/from-template",
        headers=auth_headers,
        json={
            "drone_type_id": drone_type_id,
            "name": "Mavic 3 - Test",
            "custom_max_flight_time_min": 38,
        },
    )
    assert drone_response.status_code == 201
    drone_id = drone_response.json()["id"]

    resolved_response = client.get(f"/api/drones/{drone_id}/resolved", headers=auth_headers)
    assert resolved_response.status_code == 200
    assert resolved_response.json()["weight_g"] == {"value": 895, "source": "template"}
    assert resolved_response.json()["max_flight_time_min"] == {
        "value": 38,
        "source": "custom",
    }

    flight_response = client.post(
        "/api/flights",
        headers=auth_headers,
        json={
            "drone_id": drone_id,
            "date": "2026-06-18",
            "start_time": "10:00",
            "end_time": "10:25",
            "location_name": "Testgelände",
            "flight_type": "Training",
            "status": "completed",
        },
    )
    assert flight_response.status_code == 201
    assert flight_response.json()["duration_minutes"] == 25

    dashboard_response = client.get("/api/reports/dashboard", headers=auth_headers)
    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["flights_total"] == 1
    assert dashboard_response.json()["total_flight_minutes"] == 25

    export_response = client.get("/api/export/flights.csv", headers=auth_headers)
    assert export_response.status_code == 200
    assert "Testgelände" in export_response.text


def test_pilot_permissions(client: TestClient, auth_headers: dict[str, str]):
    user_response = client.post(
        "/api/users",
        headers=auth_headers,
        json={
            "username": "pilot",
            "email": "pilot@example.com",
            "full_name": "Test Pilot",
            "role": "pilot",
            "password": "secure-password",
        },
    )
    assert user_response.status_code == 201

    type_response = client.post(
        "/api/drone-types",
        headers=auth_headers,
        json={"manufacturer": "Test", "model": "Admin Drone"},
    )
    drone_response = client.post(
        "/api/drones",
        headers=auth_headers,
        json={"drone_type_id": type_response.json()["id"], "name": "Admin-Drohne"},
    )

    login_response = client.post(
        "/api/auth/login",
        json={"username": "pilot", "password": "secure-password"},
    )
    pilot_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    forbidden_type = client.post(
        "/api/drone-types",
        headers=pilot_headers,
        json={"manufacturer": "Nicht", "model": "Erlaubt"},
    )
    forbidden_drone = client.get(
        f"/api/drones/{drone_response.json()['id']}",
        headers=pilot_headers,
    )
    assert forbidden_type.status_code == 403
    assert forbidden_drone.status_code == 403
