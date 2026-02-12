import re

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from ..config.urls import SENATORS_URL
from ..utils.helpers import find_required_element, find_required_elements


def capitalize_names(names):
    return re.sub(
        r"[^\s-]+", lambda m: m.group()[0].upper() + m.group()[1:].lower(), names
    )


def scrape_senators_data() -> list[dict[str, str]]:
    session = requests.Session()
    response = session.get(SENATORS_URL)
    soup = BeautifulSoup(response.text, "lxml")

    container = find_required_element(soup, "div", id="ctl00_B_Center_updGrupuri")
    tab_content_div = find_required_element(container, "div", class_="tab-content")
    row_div = find_required_element(tab_content_div, "div", class_="row")
    cards = find_required_elements(row_div, "div", class_=["col-md-6", "col-lg-4"])
    circumscriptii = find_required_elements(
        container, "p", string=lambda text: text and "Circumscripţia electorală" in text
    )

    senators: list[dict[str, str]] = []
    for card, circumscriptie in zip(cards, circumscriptii):
        extracted_name = find_required_element(card, "a").get_text(strip=True)
        formatted_name = capitalize_names(extracted_name)

        text = circumscriptie.get_text()
        number = re.findall(r"\d+", text)[0]
        district = text.split()[-1]

        senator = {
            "name": unidecode(formatted_name),
            "electoralDistrictNumber": number,
            "electoralDistrictName": district,
            "politicalParty": "PSD",
        }

        senators.append(senator)

    return senators


if __name__ == "__main__":
    scrape_senators_data()
