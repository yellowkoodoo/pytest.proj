def test_navigate_to_google(page):
    page.goto("https://www.google.com")    

    assert page.title() == "Google1"