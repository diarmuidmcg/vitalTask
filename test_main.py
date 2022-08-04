from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# ---------------------------------- GLUCOSE TESTS -----------------------------------
def test_get_glucose_valid():
    response = client.get("/glucose?start_date=2022-4-25&end_date=2022-4-26")
    assert response.status_code == 200
    assert response.json() == {
    "data": [
        {
            "timestamp": 1650876892,
            "value": 5.6,
            "id": 537,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650877792,
            "value": 5.4,
            "id": 538,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650878692,
            "value": 5.6,
            "id": 539,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650879592,
            "value": 6.1,
            "id": 540,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650880492,
            "value": 6.6,
            "id": 541,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650881392,
            "value": 6.3,
            "id": 542,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650882292,
            "value": 5.9,
            "id": 543,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650883192,
            "value": 5.9,
            "id": 544,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650884092,
            "value": 5.7,
            "id": 545,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650884992,
            "value": 5.9,
            "id": 546,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650885892,
            "value": 6.4,
            "id": 547,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650886792,
            "value": 6.4,
            "id": 548,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650887692,
            "value": 6.3,
            "id": 549,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650888592,
            "value": 6.3,
            "id": 550,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650889492,
            "value": 6.3,
            "id": 551,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650890392,
            "value": 6.3,
            "id": 552,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650891292,
            "value": 6.2,
            "id": 553,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650892192,
            "value": 6.3,
            "id": 554,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650893092,
            "value": 6.3,
            "id": 555,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650893992,
            "value": 6.2,
            "id": 556,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650894892,
            "value": 6.2,
            "id": 557,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650895792,
            "value": 6.2,
            "id": 558,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650896692,
            "value": 6.2,
            "id": 559,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650897592,
            "value": 6.2,
            "id": 560,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650898492,
            "value": 6.1,
            "id": 561,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650899392,
            "value": 5.7,
            "id": 562,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650900292,
            "value": 5.6,
            "id": 563,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650901192,
            "value": 5.7,
            "id": 564,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650902092,
            "value": 6.0,
            "id": 565,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650902992,
            "value": 6.1,
            "id": 566,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650903892,
            "value": 5.9,
            "id": 567,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650876892,
            "value": 5.6,
            "id": 1104,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650877792,
            "value": 5.4,
            "id": 1105,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650878692,
            "value": 5.6,
            "id": 1106,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650879592,
            "value": 6.1,
            "id": 1107,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650880492,
            "value": 6.6,
            "id": 1108,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650881392,
            "value": 6.3,
            "id": 1109,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650882292,
            "value": 5.9,
            "id": 1110,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650883192,
            "value": 5.9,
            "id": 1111,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650884092,
            "value": 5.7,
            "id": 1112,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650884992,
            "value": 5.9,
            "id": 1113,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650885892,
            "value": 6.4,
            "id": 1114,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650886792,
            "value": 6.4,
            "id": 1115,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650887692,
            "value": 6.3,
            "id": 1116,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650888592,
            "value": 6.3,
            "id": 1117,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650889492,
            "value": 6.3,
            "id": 1118,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650890392,
            "value": 6.3,
            "id": 1119,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650891292,
            "value": 6.2,
            "id": 1120,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650892192,
            "value": 6.3,
            "id": 1121,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650893092,
            "value": 6.3,
            "id": 1122,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650893992,
            "value": 6.2,
            "id": 1123,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650894892,
            "value": 6.2,
            "id": 1124,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650895792,
            "value": 6.2,
            "id": 1125,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650896692,
            "value": 6.2,
            "id": 1126,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650897592,
            "value": 6.2,
            "id": 1127,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650898492,
            "value": 6.1,
            "id": 1128,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650899392,
            "value": 5.7,
            "id": 1129,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650900292,
            "value": 5.6,
            "id": 1130,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650901192,
            "value": 5.7,
            "id": 1131,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650902092,
            "value": 6.0,
            "id": 1132,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650902992,
            "value": 6.1,
            "id": 1133,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        },
        {
            "timestamp": 1650903892,
            "value": 5.9,
            "id": 1134,
            "patientId": "3f5e19e1-d667-11ea-a179-0242ac110007"
        }
    ]
}

def test_get_glucose_out_of_bounds():
    response = client.get("/glucose?start_date=2021-10-12&end_date=2021-10-17")
    assert response.status_code == 200
    assert response.json() == {'data': 'No data was returned, try changing your parameters'}
    
def test_get_glucose_wrong_start_date():
    response = client.get("/glucose?start_date=10-12-2021&end_date=2021-10-17")
    assert response.status_code == 200
    assert response.json() == {"error": "state date should be YYYY-MM-DD & a query parameter"}

def test_get_glucose_wrong_end_date():
    response = client.get("/glucose?start_date=2021-10-12&end_date=202110-17")
    assert response.status_code == 200
    assert response.json() == {"error": "end date should be YYYY-MM-DD & a query parameter"}
    
# ---------------------------------- Sign in TESTS -----------------------------------
def test_get_Sign_in_wrong_creds():
    response = client.post(
        "/signin",
        headers = {"Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"},
        json={
            "Country":"GB",
            "email": "email@email.com",
            "password": "notARealPw"
            },
    )
    assert response.status_code == 200
    assert response.json() == {
        "error": "Error response b'{\"status\":2,\"error\":{\"message\":\"notAuthenticated\"}}\\n' while requesting https://api-eu.libreview.io/auth/login."
    }
    
def test_get_Sign_in_no_creds():
    response = client.post(
        "/signin",
        headers = {"Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"},
        json={
            "Country":"GB",
            },
    )
    assert response.status_code == 422
    assert response.json() == {
    {'detail': [{'loc': ['body', 'email'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]} != {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}
    }