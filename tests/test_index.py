import pytest


def test_main_page_works(app):
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    with app.app_context():
        tpl = app.jinja_env.get_template('main.html')
        assert tpl.render() == rsp.get_data(as_text=True)


def test_error_page_works(app):
    client = app.test_client()
    rsp = client.get("/this_doesnt_exist")
    assert rsp.status == '404 NOT FOUND'
    html = rsp.get_data(as_text=True)
    assert "404" in html


def test_signup_page_works(app):
    client = app.test_client()
    rsp = client.get('/signup')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert "<form" in html
    assert "<button" in html
    assert "Registrer" in html


def test_login_page_works(app):
    client = app.test_client()
    rsp = client.get('/login')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert "<form" in html
    assert "<button" in html
    assert "Registrer" in html
