from oniria.domain.models import User, UserStatus, Plan


def test_signup_must_return(client, mocker):
    mocker.patch(
        "oniria.interfaces.routes.UserService.sign_up",
        return_value=User(
            uuid="internal_user_123",
            external_uuid="user_test_123",
            dreamer_tag="TestDreamer#1234",
            user_status=UserStatus(name="active"),
            plan=Plan(name="free", permissions=[]),
            character_sheets=[],
            masters_workshops=[],
        ),
    )
    response = client.post(
        "/oniria/v1/signup", json={"email": "test@test.com", "password": "passwordtest"}
    )
    endpoint_response = response.json()
    assert response.status_code == 200
    assert endpoint_response["uuid"] == "internal_user_123"
