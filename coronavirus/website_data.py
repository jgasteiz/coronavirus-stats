import requests
from lxml import html

from coronavirus import cache

SOURCE_URL = "https://www.worldometers.info/coronavirus/"


def get_website_data():
    if not cache.is_cache_recent():
        _cache_website_data()
    return _get_cached_website_data()


def _cache_website_data():
    """
    Try to get and cache website data.
    """
    try:
        page = requests.get(SOURCE_URL)
    except Exception:
        # If we can't get a page, we won't be updating any cache.
        pass
    else:
        tree = html.fromstring(page.content)
        # Last updated: next sibling of the element with id page-top.
        last_updated = tree.get_element_by_id("page-top").getnext().text
        # Table of stats per country.
        table = tree.get_element_by_id("main_table_countries_today")
        # Add a bootstrap table-responsive class to the table.
        table.attrib["class"] = "{} table-responsive".format(table.attrib["class"])
        html_table = html.tostring(table).decode("utf-8")
        # Prepend the absolute url to all relative country links in the table.
        html_table = html_table.replace('href="country/', f'href="{SOURCE_URL}country/')
        cache.cache_data(html_table=html_table, last_updated=last_updated)


def _get_cached_website_data():
    cached_website_data = cache.get_cache()
    return {
        "html_table": cached_website_data["html_table"],
        "last_updated": cached_website_data["last_updated"],
    }
