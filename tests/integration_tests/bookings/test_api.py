import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-02", "2025-01-11", 200),
        (1, "2025-01-03", "2025-01-12", 200),
        (1, "2025-01-04", "2025-01-13", 200),
        (1, "2025-01-05", "2025-01-14", 200),
        (1, "2025-01-06", "2025-01-15", 500),
        (1, "2025-01-16", "2025-01-17", 200),  # Данная дата уже не накладывается на другие
    ],
)  # Параметризация ф-ии (по множеству входных параметров с указанием исхода выполнения кода)
async def test_post_booking(room_id, date_from, date_to, status_code, db, authentificated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authentificated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings(db_module):
    await db_module.bookings.delete()
    await db_module.commit()

    bookings = await db_module.bookings.get_all()
    assert not bookings


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2025-01-01", "2025-01-10", 1),
        (1, "2025-01-02", "2025-01-11", 2),
        (1, "2025-01-03", "2025-01-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    authentificated_ac,
    delete_all_bookings,
):
    response = await authentificated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res

    response_my_bookings = await authentificated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    res = response_my_bookings.json()
    assert isinstance(res, list)
    assert len(res) == booked_rooms
