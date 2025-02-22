async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-01-01",
            "date_to": "2025-01-02",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
