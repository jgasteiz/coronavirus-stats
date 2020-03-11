import requests

from flask import Flask, render_template
from lxml import html

app = Flask(__name__)


@app.route("/")
def index():
    page = requests.get("https://www.worldometers.info/coronavirus/")
    tree = html.fromstring(page.content)
    # Last updated: next sibling of the element with id page-top.
    last_updated = tree.get_element_by_id("page-top").getnext().text
    # Table of stats per country.
    table = tree.get_element_by_id("main_table_countries")
    table.attrib["class"] = "{} table-responsive".format(table.attrib["class"])
    table_html = html.tostring(table).decode("utf-8")
    return render_template("index.html", content=table_html, last_updated=last_updated)
