import requests
from flask import Flask, render_template
from lxml import html

from . import cache

app = Flask(__name__)


@app.route("/")
def index():
    cached_data = cache.get_cache_if_recent()
    if cached_data:
        table_html = cached_data["html"]
        last_updated = cached_data["last_updated"]
    else:
        try:
            page = requests.get("https://www.worldometers.info/coronavirus/")
        except Exception as e:
            cached_data = cache.get_cache()
            table_html = cached_data["html"]
            last_updated = cached_data["last_updated"]
        else:
            tree = html.fromstring(page.content)
            # Last updated: next sibling of the element with id page-top.
            last_updated = tree.get_element_by_id("page-top").getnext().text
            # Table of stats per country.
            table = tree.get_element_by_id("main_table_countries")
            table.attrib["class"] = "{} table-responsive".format(table.attrib["class"])
            table_html = html.tostring(table).decode("utf-8")
            cache.cache_data(html=table_html, last_updated=last_updated)

    return render_template("index.html", content=table_html, last_updated=last_updated)
