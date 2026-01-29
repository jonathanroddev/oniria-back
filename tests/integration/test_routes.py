def test_get_user_data_must_return(client):
    response = client.get("/oniria/v1/users/me")
    endpoint_response = response.json()
    assert response.status_code == 200
    assert endpoint_response["uuid"] == "internal_user_123"


def test_get_plans_must_return(client):
    response = client.get("/oniria/v1/public/plans")
    endpoint_response = response.json()
    assert response.status_code == 200
    assert endpoint_response[0]["name"] == "free"
