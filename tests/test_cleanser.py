from src.scrapper import clean_html
"""Unit tests for html cleanser"""

def test_clean_html_removes_tags():
    raw = "<li>Content</li>"
    assert clean_html(raw) == "Content"

def test_clean_html_handles_nbsp():
    raw = "Hello&nbsp;World"
    assert clean_html(raw) == "Hello World"

def test_clean_html_handles_empty_input():
    assert clean_html("") == ""
    assert clean_html(None) == ""

def test_clean_html_unescapes_ampersand():
    raw = "Hello World&amp;"
    assert clean_html(raw) == "Hello World&"

def test_clean_html_unescapes_quots():
    raw = "Hello &quot;World&quot;"
    assert clean_html(raw) == "Hello \"World\""