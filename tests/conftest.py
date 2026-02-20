import pytest

@pytest.fixture
def google_xml():
    with open("data_samples/google_news.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def empty_xml():
    with open("data_samples/empty_feed.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def error_xml():
    with open("data_samples/invalid/error_page.xml", "r") as f:
        return f.read()

@pytest.fixture  
def minimal_xml():
    with open("data_samples/minimal.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def nasa_xml():
    with open("data_samples/nasa_news.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def verge_xml():
    with open("data_samples/the_verge.xml", "r") as f:
        return f.read()