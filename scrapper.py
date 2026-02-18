import re
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import json as js


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout
        or written to file as a separate lines.

    Examples:
        #>>> xml = '
            <rss>
                <channel>
                    <title>
                        Some RSS Channel
                    </title>
                    <link>
                        https://some.rss.com
                    </link>
                    <description>
                        Some RSS Channel
                    </description>
                </channel>
            </rss>'
        #>>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        #>>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """
    # Your code goes here
    def unescape(text):
        """
        Replace RSS special character's aliasses by actual characters
        
        :param text: RSS text
        """
        if not text:
            return text
        return (text
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&quot;", '"')
                .replace("&apos;", "'")
                .replace("&#x27;", "'")
                .replace("&#39;", "'")
                .replace("&amp;", "&"))

    class ThisXML:
        def __init__(self, xml: str):
            self.xml = xml
            self.Channel = self._parse_channel()

        def _extract_all_tags(self, text: str, tag: str) -> List[str]:
            """Extract all content of all examples of a given tag from rss, returns a list of contents

                param text: rss content
                param tag: tag to seatch 
            
            """
            result = []
            start_tag = f"<{tag}>"
            end_tag = f"</{tag}>"

            if start_tag not in text:
                return []

            current_text = text

            while start_tag in current_text:
                try:
                    after_start = current_text.split(start_tag, 1)[1]
                    content = after_start.split(end_tag, 1)[0]
                    result.append(unescape(content))

                    current_text = after_start

                except IndexError:
                    break
            return result

        def _extract_tag(self, text: str, tag: str):
            start_tag = f"<{tag}>"
            end_tag = f"</{tag}>"

            if start_tag not in text:
                return None

            try:
                after_start = text.split(start_tag, 1)[1]
                content = after_start.split(end_tag, 1)[0]
                return unescape(content)
            except IndexError:
                return None

        def _parse_channel(self):
            """
            Return dictionary containing:
            title of channel;
            link;
            last modifying date;
            publication date;
            language;
            editor;
            list of categories;
            items;

            from rss file
            """
            channel_content = self._extract_tag(self.xml, "channel")
            if not channel_content:
                return {}

            channel_categories = self._extract_all_tags(channel_content, "category")

            data = {
                "title": self._extract_tag(channel_content, "title"),
                "link": self._extract_tag(channel_content, "link"),
                "description": self._extract_tag(channel_content, "description"),
                "lastBuildDate": self._extract_tag(channel_content, "lastBuildDate"),
                "pubDate": self._extract_tag(channel_content, "pubDate"),
                "language": self._extract_tag(channel_content, "language"),
                "managinEditor": self._extract_tag(channel_content, "managinEditor"),
                "category": channel_categories if channel_categories else None,
                "items": []
            }

            if "<item>" in channel_content:
                raw_items = channel_content.split("<item>")[1:]
                for raw_item in raw_items:
                    clean_item_text = raw_item.split("</item>")[0]
                    item_categories = self._extract_all_tags(clean_item_text, "category")
                    item_data = {
                        "title": self._extract_tag(clean_item_text, "title"),
                        "author": self._extract_tag(clean_item_text, "author"),
                        "pubDate": self._extract_tag(clean_item_text, "pubDate"),
                        "link": self._extract_tag(clean_item_text, "link"),
                        "category": item_categories if item_categories else None,
                        "description": self._extract_tag(clean_item_text, "description")
                    }
                    data["items"].append(item_data)

            return data
        
    def clean_html(text):
        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        return (" ".join(clean.split())).replace("&nbsp;", "\n")

    parser = ThisXML(xml)
    channel_data = parser.Channel
    items = channel_data.get("items", [])

    if limit is not None:
        items = items[:limit]
        channel_data["items"] = items

    if json:
        json_dict = {
            key: value
            for key, value in channel_data.items()
            if value is not None and value != []
        }
        return [js.dumps(json_dict, indent=2)]

    output_lines = []

    def add(label, value):
        if value:
            if isinstance(value, list):
                value = ", ".join(value)
            output_lines.append(f"{label}: {value}")

    add("Feed", channel_data.get("title"))
    add("Link", channel_data.get("link"))
    add("Last Build Date", channel_data.get("lastBuildDate"))
    add("Publish Date", channel_data.get("pubDate"))
    add("Language", channel_data.get("language"))

    if channel_data.get("category"):
        add("Categories", channel_data.get("category"))

    add("Editor", channel_data.get("managinEditor"))
    add("Description", channel_data.get("description"))

    output_lines.append("")

    for item in items:
        add("Title", item.get("title"))
        add("Author", item.get("author"))
        add("Published", item.get("pubDate"))
        add("Link", item.get("link"))

        if item.get("category"):
            output_lines.append(f"Category: {item.get('category')}")

        desc = item.get("description")
        if desc:
            output_lines.append("")
            output_lines.append(clean_html(desc))

        output_lines.append("")
        output_lines.append("")

    return output_lines


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
