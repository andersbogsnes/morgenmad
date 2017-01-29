from splinter import Browser


def test_homepage():
    browser = Browser('chrome')
    url = "localhost:5000"
    """John was told he should check out the new breakfast app. It would let him organise who is bringing break"""
    browser.visit(url)
    assert browser.is_text_present('Velkommen til KSM morgenmadsliste')
    """When he logs in, he's greeted with a list showing whose turn it is to bring breakfast"""
    assert browser.is_text_present("Det er Anders sin tur på fredag den 13. Januar")
    browser.quit()
