import xml.etree.ElementTree as ET
import re
import requests

def clean_html(content: str)->str:
    if not content:
        return ""
    content = re.sub(r"<[^>]+>", "", content)
    content = " ".join(content.split())
    content = content.replace("&nbsp;", '\n').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", "\"")
def parse_xml(xml: str)->dict:
    """
    Docstring for parse_xml
    
    :param xml: Description
    :type xml: str
    :return: Description
    :rtype: dict
    """
    root = ET.fromstring(xml)
    channel = root.find('channel')

    data = {
        "title": channel.findtext('title'),
        "link": channel.findtext("link"),
        "items": []
    }
    for item in channel.findall('item'):
        entry = {
            'title': item.findtext('title'),
            'link': item.findtext('link'),
            'description': clean_html(item.findtext('description', "")),
            'pubDate': item.findtext('pubDate')
        }
        data['items'].append(entry)
    return data

def print_output(data: dict, limit = None):
    try:
        i = 0
        print(f"Page Title: {data['title']}\nLink: {data['link']}")
        for item in data["items"]:
            if limit and limit>0:
                if i == limit:
                    break
                i+=1
            print(f"\t{item['title']}\n{item['pubDate']}\n{item['description']}\n{item['link']}")
            print("==================================================================")
            
    except:
        print("Not valid data")
    


if __name__ =="__main__":
    content = requests.get("https://news.google.com/rss").text
    data = parse_xml(content)
    print_output(data, 5)