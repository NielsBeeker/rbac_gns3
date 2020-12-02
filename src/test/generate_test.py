import pytest
from httpx import AsyncClient
from main import app
import string

data_base_user = {
    "alice" : "secret",
    "bob": "secret"
}
username = "alice"


auth_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
def load_response(usernames):
    response = {}
    #with open(f"{usernames}.test") as f:
    with open(f"{username}.test") as f:
        lines = f.readlines()
    lines = [x.strip("\n") for x in lines]
    for line in lines:
        res = line.split(":")
        tuple = res[0].split(",")
        tmp = {(tuple[0], tuple[1]): (int(res[1]))}
        response.update(tmp)
    return response

    #return: { ("/v3/projects/project1234", "POST") : 200}
    #reour: 401 unautorize, 200, ok, 404 not found
username = "alice"


async def create_token():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        token = await ac.post("v3/token2", headers=auth_header, json={"username": f"{username}", "password": "secret"})#TODO a gerer selon le endpoint
    return await token.json()


#token = create_token()
good_response = load_response(username)


def check_result(response, endpoint):
    tmp = good_response[endpoint]
    if response.status_code == 404:
        print(endpoint)
    assert response.status_code == tmp



async def test_request_ok(stringinput):
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        post_token = await ac.post("/v3/token2", headers=auth_header, json={"username": f"{username}", "password": "secret"})
    token = post_token.json()
    header = {'Accept': 'application/json', 'Authorization': f"Bearer {token['access_token']}"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        if stringinput[1] == "GET":
            response = await ac.get(f"{stringinput[0]}", headers=header)
            check_result(response, stringinput)
        elif stringinput[1] == "POST":
            response = await ac.post(f"{stringinput[0]}", headers=header)
            check_result(response, stringinput)
        elif stringinput[1] == "PUT":
            response = await ac.put(f"{stringinput[0]}", headers=header)
            check_result(response, stringinput)
        else:
            response = await ac.delete(f"{stringinput[0]}", headers=header)
            check_result(response, stringinput)
    print(f"endpoint = {stringinput}, User = {username} : OK")



if __name__ == '__main__':
    pytest.main(['-rs -q', 'generate_test.py'])
