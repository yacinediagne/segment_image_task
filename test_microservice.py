from fastapi.testclient import TestClient

from microservice import app

client = TestClient(app)


def test_segment_everything():
    # Open the image file in binary mode
    with open("resources/dog.jpg", "rb") as image:
        response = client.post("/segment-image", files={"file": ("resources/dog.jpg", image)})
    assert response.status_code == 200
    