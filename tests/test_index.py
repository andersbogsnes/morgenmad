from app.morgenmad import create_app
from app.config import TestConfig
import pytest


@pytest.fixture()
def instance_app():
    app = create_app(TestConfig)
    return app


def test_main_page_works(instance_app):
    client = instance_app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert "<title>KSM Morgenmadsliste</title>" in html
    assert "<h1>Velkommen til KSM morgenmadslisten</h1>" in html

def test_error_page_works(instance_app):
    client = instance_app.test_client()
    rsp = client.get("/this_doesnt_exist")
    assert rsp.status == '404 NOT FOUND'
    html = rsp.get_data(as_text=True)
    assert "404" in html