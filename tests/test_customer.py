import pytest

from tests.conftest import user_client
@pytest.mark.django_db
def test_get_customer_profile(user_client):
    response= user_client.get("/api/customer/profile/")
    assert response.status_code == 200
    assert 'user' in response.data


@pytest.mark.django_db
def test_update_customer_profile(user_client):
    body={
        "phone_number":"0781111111",
        "address":"amman",
        "date_of_birth":"1997-1-1",
    }
    response= user_client.put("/api/customer/profile/update/",body)
    assert response.status_code == 200
    assert "message" in response.data
    assert response.data['message'] == "Profile updated successfully!"