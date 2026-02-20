from src.scrapper import parse_xml
import pytest

def test_parse_xml_dict_structure(minimal_xml):
    res = parse_xml(minimal_xml)
    assert res['title'] == "Test Feed"
    assert res['link'] == "https://test.com"
    assert res['items']

def test_items_payload(google_xml):
    res = parse_xml(google_xml)
    assert res['items']
    items = res['items']
    sample = items[0]
    assert sample['title']
    assert sample['link']
    assert sample['description']
    assert sample['pubDate']

def test_negative_test(error_xml):
    with pytest.raises(Exception):
        res = parse_xml(error_xml)