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

def test_batch_predict_one():
    data = {
        "houses": [
            {
                'MedInc' : 8.3252, 
                'HouseAge' : 41.0, 
                'AveRooms' : 6.98412698,
                'AveBedrms' : 1.02380952, 
                'Population' : 322.0, 
                'AveOccup' : 2.55555556, 
                'Latitude' : 75.88, 
                'Longitude' : -122.23
            }
        ]
    }
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200


def test_batch_predict_two():
    data = {
        "houses": [
            {
                'MedInc' : 8.3252, 
                'HouseAge' : 41.0, 
                'AveRooms' : 6.98412698,
                'AveBedrms' : 1.02380952, 
                'Population' : 322.0, 
                'AveOccup' : 2.55555556, 
                'Latitude' : 75.88, 
                'Longitude' : -122.23
            },
            {
                'MedInc' : 9.5, 
                'HouseAge' : 25.0,
                'AveRooms' : 6.98412698, 
                'AveBedrms' : 5.0, 
                'Population' : 242.0, 
                'AveOccup' : 1.55555556, 
                'Latitude' : 45.88, 
                'Longitude' : -110.23
            }
        ]
    }
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200

def test_batch_predict_three():
    data = {
        "houses": [
            {
                'MedInc' : 8.3252, 
                'HouseAge' : 41.0, 
                'AveRooms' : 6.98412698,
                'AveBedrms' : 1.02380952, 
                'Population' : 322.0, 
                'AveOccup' : 2.55555556, 
                'Latitude' : 75.88, 
                'Longitude' : -122.23
            },
            {
                'MedInc' : 9.5, 
                'HouseAge' : 25.0,
                'AveRooms' : 6.98412698, 
                'AveBedrms' : 5.0, 
                'Population' : 242.0, 
                'AveOccup' : 1.55555556, 
                'Latitude' : 45.88, 
                'Longitude' : -110.23
            },
            {
                'MedInc' : 8.75, 
                'HouseAge' : 10.0,
                'AveRooms' : 9.2698, 
                'AveBedrms' : 3.0, 
                'Population' : 242.0, 
                'AveOccup' : 6.55555556, 
                'Latitude' : 45.88, 
                'Longitude' : 110.23
            }
        ]
    }
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200

def test_bad_bulk_predict():
    data = {
        "houses": [
            {
                'MedInc' : 8.3252, 
                'HouseAge' : 41.0, 
                'AveBedrms' : 1.02380952, 
                'Population' : 322.0, 
                'AveOccup' : 2.55555556, 
                'Latitude' : 75.88, 
                'Longitude' : -122.23
            },
            {
                'MedInc' : 9.5, 
                'HouseAge' : 25.0,
                'AveBedrms' : 5.0, 
                'Population' : 242.0, 
                'AveOccup' : 1.55555556, 
                'Latitude' : 45.88, 
                'Longitude' : -110.23
            }
        ]
    }
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 422

    data = {
        "houses": [
            {
                'MedInc' : 8.3252, 
                'HouseAge' : 41.0, 
                'AveBedrms' : 1.02380952, 
                'Population' : 322.0, 
                'AveOccup' : 2.55555556, 
                'Latitude' : 200.88, 
                'Longitude' : -122.23
            },
            {
                'MedInc' : 9.5, 
                'HouseAge' : 25.0,
                'AveBedrms' : 5.0, 
                'Population' : 242.0, 
                'AveOccup' : 1.55555556, 
                'Latitude' : 45.88, 
                'Longitude' : -110.23
            }
        ]
    }
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 422

def test_bulk_predict_invalid():
    with TestClient(app) as lifespanned_client:
        data =  {
            "houses": [
                {
                    "MedInc": 1,
                    "HouseAge": 2,
                    "AveRooms": 2,
                    "AveBedrooms": 2,
                    "Population": 1,
                    "AveOccup": 8,
                    "Latitude": 2,
                    "Longitude": 2,
                },
                {
                    "MedInc": 0,
                    "HouseAge": 2,
                    "AveRooms": 4,
                    "AveBedrooms": 4,
                    "Population": 2,
                    "AveOccup": 4,
                    "Latitude": 1,
                    "Longitude": 190,
                }

            ]
        }
        response = client.post(
            "/bulk-predict",
            json=data
        )
        assert response.status_code == 422
        


    


