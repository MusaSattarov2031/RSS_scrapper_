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
def nasa_xml():
    with open("data_samples/nasa_news.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def verge_xml():
    with open("data_samples/the_verge.xml", "r") as f:
        return f.read()

@pytest.fixture
def mock_parsed_data():
    return {
        "title": "Engineering Daily",
        "link": "https://eng-daily.test",
        "items": [
            {
                "title": "First Article",
                "link": "https://eng-daily.test/article-1",
                "description": "Clean description.",
                "pubDate": "Wed, 18 Feb 2026 12:00:00 GMT"
            },
            {
                "title": "First Article (Updated Title)",
                "link": "https://eng-daily.test/article-1",
                "description": "Same link, so this is a duplicate!",
                "pubDate": "Wed, 18 Feb 2026 13:00:00 GMT"
            },
            {
                "title": "Second Article",
                "link": "https://eng-daily.test/article-2",
                "description": "Another description.",
                "pubDate": "Thu, 19 Feb 2026 09:30:00 GMT"
            }
        ]
    }