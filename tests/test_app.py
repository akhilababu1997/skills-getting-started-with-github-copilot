from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def reset_activities():
    # to avoid mutation across tests, reinitialize participants from expected fixture values
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Basketball"]["participants"] = ["james@mergington.edu"]
    activities["Tennis"]["participants"] = ["lucas@mergington.edu"]
    activities["Art Club"]["participants"] = ["isabella@mergington.edu", "ava@mergington.edu"]
    activities["Drama Club"]["participants"] = ["noah@mergington.edu", "mia@mergington.edu"]


def setup_function(function):
    reset_activities()


def test_get_activities_returns_all_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_new_user_success():
    reset_activities()
    payload = {"email": "newstudent@mergington.edu"}
    r = client.post("/activities/Chess%20Club/signup?email=newstudent%40mergington.edu")
    assert r.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in r.json()["message"]
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_user_fails():
    reset_activities()
    r = client.post("/activities/Chess%20Club/signup?email=michael%40mergington.edu")
    assert r.status_code == 400
    assert r.json()["detail"] == "Student already signed up"


def test_unregister_existing_user_success():
    reset_activities()
    r = client.post("/activities/Chess%20Club/unregister?email=michael%40mergington.edu")
    assert r.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" in r.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_participant_fails():
    reset_activities()
    r = client.post("/activities/Chess%20Club/unregister?email=notfound%40mergington.edu")
    assert r.status_code == 400
    assert r.json()["detail"] == "Participant not found for this activity"


def test_unregister_unknown_activity_fails():
    reset_activities()
    r = client.post("/activities/Unknown%20Club/unregister?email=someone%40mergington.edu")
    assert r.status_code == 404
    assert r.json()["detail"] == "Activity not found"
