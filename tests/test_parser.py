from src.scrapper import parse_xml
import pytest
import xml.etree.ElementTree as ET

def test_parse_xml_dict_structure(nasa_xml):
    res = parse_xml(nasa_xml)
    assert res['title']
    assert res['link']
    assert isinstance(res['items'], list)

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