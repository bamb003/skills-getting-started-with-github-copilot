import pytest

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # expect at least the predefined clubs
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_duplicate(client):
    # sign up a new student
    email = "teststudent@mergington.edu"
    resp = client.post("/activities/Chess Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verifying participant was added
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]

    # duplicate attempt should fail
    dup = client.post("/activities/Chess Club/signup", params={"email": email})
    assert dup.status_code == 400
    assert "already" in dup.json().get("detail", "").lower()


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/Nonexistent/signup", params={"email": "foo@bar.com"})
    assert resp.status_code == 404


def test_unregister_flow(client):
    # first sign up
    email = "leave@mergington.edu"
    client.post("/activities/Programming Class/signup", params={"email": email})

    # then unregister
    del_resp = client.delete(f"/activities/Programming Class/signup/{email}")
    assert del_resp.status_code == 200
    assert "Unregistered" in del_resp.json().get("message", "")

    # ensure participant removed
    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_not_signed_up(client):
    resp = client.delete("/activities/Chess Club/signup/not@here.edu")
    assert resp.status_code == 400
    assert "not signed up" in resp.json().get("detail", "").lower()
