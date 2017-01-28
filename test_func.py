from splinter import Browser

def test_homepage():
    browser = Browser('chrome')
    url = "localhost:5000"
    """John was told he should check out the new breakfast app. It would let him organise who is bringing break"""
    browser.visit(url)
    assert browser.is_text_present('Hello World')
