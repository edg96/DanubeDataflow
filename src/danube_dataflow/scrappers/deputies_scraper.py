from bs4 import BeautifulSoup
from unidecode import unidecode

from ..config.urls import DEPUTIES_URL
from ..utils.helpers import (
    find_required_element,
    find_required_elements,
    receive_custom_session,
)


def scrape_deputies_data() -> list[dict[str, str]]:
    """
    Scrape data from the official website of the Romanian Government where all the details about Chamber of Deputies
        is presented, including the list of deputies in the form of a table.

    Returns:
        A list of objects representing the deputies, each deputy containing its name, district and political party.
    """
    session = receive_custom_session()
    response = session.get(DEPUTIES_URL)
    soup = BeautifulSoup(response.text, "lxml")

    deputies: list[dict[str, str]] = []

    try:
        elements = find_required_element(
            soup,
            "div",
            class_=["grup-parlamentar-list", "grupuri-parlamentare-list"],
        )

        table = find_required_elements(elements, "tr")

        for row in table:
            cells = find_required_elements(row, "td")

            if len(cells) < 4:
                continue

            electoralDistrict = cells[2].get_text(strip=True)

            electoralDistrictNumber = (
                electoralDistrict.split("/")[0].strip()
                if len(electoralDistrict) > 0
                else None
            )

            electoralDistrictName = (
                unidecode(electoralDistrict.split("/")[1].strip().capitalize())
                if len(electoralDistrict) > 0
                else None
            )

            deputy = {
                "name": unidecode(cells[1].get_text(strip=True)),
                "electoralDistrictNumber": electoralDistrictNumber,
                "electoralDistrictName": electoralDistrictName,
                "politicalParty": unidecode(cells[3].get_text(strip=False).strip()),
            }

            deputies.append(deputy)
    except Exception as e:
        print(e)

    return deputies
