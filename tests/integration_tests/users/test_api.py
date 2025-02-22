import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("api_test_user1@gmail.com", "12345", 200),
        ("api_test_user1@gmail.com", "54321", 400),
        ("api_test_user2@gmail.com", "12345", 200),
        ("api_test_user3", "12345", 422),
        ("api_test_user3@gmail", "12345", 422),
    ],
)
async def test_user_flow(email: str, password: str, status_code: int, ac):
    # /register
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    # /me
    response_get_me = await ac.get("/auth/me")
    assert response_get_me.status_code == 200
    res = response_get_me.json()
    assert res["email"] == email
    assert "id" in res
    assert "password" not in res
    assert "hashed_password" not in res

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200
    assert "access_token" not in ac.cookies

    # /me after logout
    response_get_unauthenticated_user_error = await ac.get("/auth/me")
    assert response_get_unauthenticated_user_error.status_code == 401
    res = response_get_unauthenticated_user_error.json()
    assert "detail" in res
