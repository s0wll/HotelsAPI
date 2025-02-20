async def test_post_booking(db, authentificated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authentificated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-01-01",
            "date_to": "2025-01-02",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
