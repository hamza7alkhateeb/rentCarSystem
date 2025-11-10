import pytest

from tests.conftest import vehicle, admin_client,user_client


@pytest.mark.django_db
def test_list_vehicles(user_client,vehicles):
    response = user_client.get("/api/vehicles/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert "results" in response.data
    results = response.data["results"]
    assert isinstance(results, list)
    assert len(results) == 2

def test_single_vehicle(admin_client, vehicle):
    response = admin_client.get(f"/api/vehicles/{vehicle.id}/")
    assert response.status_code == 200
    assert response.data["brand"] == "Audi"



# Admin Delete Vehicle
@pytest.mark.django_db
def test_admin_delete_vehicle(vehicle,admin_client):
    response = admin_client.delete(f'/api/vehicles/{vehicle.id}/')
    assert response.status_code == 204

#TODO: Admin create,update Vehicle