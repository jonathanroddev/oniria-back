def test_get_bootstrap_data_must_return(client, mocker):
    mocker.patch("oniria.interfaces.cs_routes.check_permissions", return_value=None)
    response = client.get("/oniria/v1/character-sheets/bootstrap")
    assert response.status_code == 200
