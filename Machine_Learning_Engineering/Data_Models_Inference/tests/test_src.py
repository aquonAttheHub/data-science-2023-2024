from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_hello():
    response = client.get("/hello?name=anson")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello anson"}
    
    response = client.get("/hello?name=bryan")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello bryan"}

def test_hello_empty():
    response = client.get("/hello?name= ")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello  "}
    
    response = client.get("/hello")
    assert response.status_code == 422

def test_hello_integer():
    response = client.get("/hello?name=1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello 1"}

def test_hello_double():
    response = client.get("/hello?name=2.5")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello 2.5"}

def test_hello_rand_char():
    response = client.get("/hello?name=$")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello $"}

    response = client.get("/hello?name=.")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello ."}

    response = client.get("/hello?name=_")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello _"}

    response = client.get("/hello?name=~")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello ~"}


def test_root():
    response = client.get("/")
    assert response.status_code == 404

def test_non_existing_resource():
    response = client.get("/randomresource")
    assert response.status_code == 404

def test_predict():
    response = client.post("/predict",
        json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveRooms' : 6.98412698, 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 37.88, 'Longitude' : -122.23}
    )
    assert response.status_code == 200

def test_bad_predict():
    response = client.post("/predict",
    json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveRooms' : 6.98412698, 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 95.88, 'Longitude' : -122.23}
    )
    assert response.status_code == 422
    response = client.post("/predict",
    json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveRooms' : 6.98412698, 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 55.88, 'Longitude' : -192.23}
    )
    response = client.post("/predict",
    json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveRooms' : 'six', 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 55.88, 'Longitude' : -192.23}
    )
    assert response.status_code == 422


def test_extra_features_predict():
    response = client.post("/predict",
    json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveRooms' : 6.98412698, 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 95.88, 'Longitude' : -122.23, 'ExtraFeature': 20.0}
    )
    assert response.status_code == 422

def test_missing_features_predict():
    response = client.post("/predict",
    json={'MedInc' : 8.3252, 'HouseAge' : 41.0, 'AveBedrms' : 1.02380952, 'Population' : 322.0, 'AveOccup' : 2.55555556, 'Latitude' : 75.88, 'Longitude' : -122.23}
    )
    assert response.status_code == 422

