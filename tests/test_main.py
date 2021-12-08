import sys
from pathlib import Path
sys.path.insert(1, str((Path(__file__).parent / '../src').resolve()))

from main import app
from fastapi.testclient import TestClient
import random

client = TestClient(app)
frames = Path(__file__).parent / '../data/frames'
scans = Path(__file__).parent / '../data/prepared/scans'
avail_frames = list(frames.glob('*/*.png'))
avail_scans = list(scans.glob('*.nii'))

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict():
    response = client.get('/predict')
    assert response.status_code == 405
    
    with open(random.choice(avail_frames), 'rb') as f:
        response = client.post('/predict', files={'image': f})
        assert response.status_code == 200
        json = response.json()
        assert "probability" in json
        assert type(json["probability"]) == float

def test_report():
    response = client.get('/report')
    assert response.status_code == 405

    with open(random.choice(avail_scans), 'rb') as f:
        response = client.post('/report', files={'scan': f})
        assert response.status_code == 200
        json = response.json()
        assert "probabilities" in json
        assert "final_probability" in json
        assert type(json['probabilities']) == list
        assert all(type(x) == float for x in json['probabilities'])
        assert type(json['final_probability']) == float