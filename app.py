from flask import Flask, render_template, url_for, redirect, session, json, request, redirect
import requests
import json

with open('config.json', 'r') as config:
    data = config.read()

org = json.loads(data)
url = org['url']
api_key = org['api_key']

app = Flask(__name__)


@app.route("/")
def index():
    return "Hej!"


@app.route("/register")
def register():
    return render_template("register.html", org=url.replace("https://", ""))


@app.route("/verifysms", methods=["POST"])
def verifysms():
    payload = json.loads(request.data)
    request_url = url + \
        f"/api/v1/users/{payload['id']}/factors/{payload['factorId']}/lifecycle/activate"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'SSWS ' + api_key,
    }
    session = requests.Session()
    session.headers.update(headers)
    body = {
        "passCode": payload['passCode']
    }
    r = session.post(request_url, json=body)

    req_url = url + \
        f"/api/v1/users/{payload['id']}/lifecycle/activate?sendEmail=false"
    r = session.post(req_url)

    req_url = url + f"/api/v1/users/{payload['id']}/factors?activate=true"
    data = {
        "factorType": "call",
        "provider": "OKTA",
        "profile": {
            "phoneNumber": payload['phone']
        }
    }
    r = session.post(req_url, json=data)
    return '', 204


@app.route("/user", methods=["POST"])
def user():
    payload = json.loads(request.data)
    request_url = url + "/api/v1/users?activate=false"
    data = {
        "profile": {
            "firstName": "Update",
            "lastName": "User",
            "email": payload['login'],
            "login": payload['login']
        },
        "credentials": {
            "password": {
                "value": payload['password']
            }
        }
    }


    headers = {
        'Accept': 'application/json',
        'Authorization': 'SSWS ' + api_key,
    }
    session = requests.Session()
    session.headers.update(headers)
    res = session.post(request_url, json=data)
    if int(res.status_code) == 200:
        id = res.json()['id']
        request_url = url + f"/api/v1/users/{id}/factors"
        data = {
            "factorType": "sms",
            "provider": "OKTA",
            "profile": {
                "phoneNumber": str(payload['phone'])
            }
        }
        res = session.post(request_url, json=data)

    return json.dumps({"id": str(id), "factorId": res.json()['id']}), 200


if __name__ == "__main__":
    app.run(port=80, debug=True)
