import pytest
from httpx import AsyncClient
from main import app


data_base_user = {
    "alice" : "secret",
    "bob": "secret"
}
username = "alice"


auth_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
def load_response(usernames):
    response = {}
    with open(f"response_{usernames}.test") as f:
        line = f.readlines()
        for elt in line:
            res = elt.split(",")
            response[(elt[0], elt[1])] == elt[3]
    return response

    #return: { ("/v3/projects/project1234", "POST") : ("200", {"ok"})}
    #reour: 401 unautorize, 200, ok, 404 not found
username = "alice"

async def create_token():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        token = await ac.post("v3/token2", headers=auth_header, json={"username": f"{username}", "password": "secret"})#TODO a gerer selon le endpoint
        return token.json()


token = create_token()
good_response = load_response(username)


def check_result(response, endpoint, request):
    tmp = good_response[(endpoint, request)]
    assert response.status_code == tmp[0]
    assert response.json() == tmp[1]



async def test_request_ok(endpoint, username):
    print(f"endpoint = {endpoint}), User = {username}")
    header = {'Accept': 'application/json', 'Authorization': f"Bearer {token['access_token']}"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        if endpoint[1] == "GET":
            response = await ac.get(f"{endpoint}", headers=header)
            check_result(response, username, endpoint, "GET")
        elif endpoint[1] == "POST":
            response = await ac.post(f"{endpoint}", headers=header)
            check_result(response, username, endpoint, "POST")
        elif endpoint[1] == "PUT":
            response = await ac.put(f"{endpoint}", headers=header)
            check_result(response, username, endpoint, "PUT")
        else:
            response = await ac.delete(f"{endpoint}", headers=header)
            check_result(response, username, endpoint, "DELETE")

