import requests

from bs4 import BeautifulSoup
from sqlalchemy import select

from utils import initialize_tables
from database import Region, Country, Session


@initialize_tables
class PopulationParser:
    def __init__(self):
        self.url = (
            "https://en.wikipedia.org/w/index.php"
            "?title=List_of_countries_by_population_(United_Nations)"
            "&oldid=1215058959"
        )

    def fetch_data(self) -> list:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table", class_="wikitable")
        rows_data = table.select("tr:has(td > span.datasortkey)")
        location_idx, newest_population_idx, region_idx = [0, 2, 4]
        fetched_data = []

        for row in rows_data:
            columns = row.find_all("td")
            country_name = self._handle_location(
                location_td=columns[location_idx]
            )
            country_population = self._handle_population(
                population_td=columns[newest_population_idx]
            )
            region_name = self._handle_region(
                region_td=columns[region_idx]
            )
            fetched_data.append(
                (
                    country_name,
                    country_population,
                    region_name
                )
            )
        return fetched_data

    def save_data(self, fetched_data) -> None:
        with Session() as session:
            for country_name, country_population, region_name in fetched_data:
                region = session.execute(
                    select(Region).where(Region.name == region_name)
                ).scalar_one_or_none() or Region(name=region_name)

                country = session.execute(
                    select(Country).where(Country.name == country_name)
                ).scalar_one_or_none() or Country(
                    name=country_name,
                    population=country_population
                )

                country.population = country_population
                region.countries.append(country)

                session.add(region)
                session.commit()

    @staticmethod
    def _handle_population(population_td) -> int | None:
        population_data = population_td.text.strip().replace(",", "")

        if population_data.isdigit():
            return int(population_data)
        return None

    @staticmethod
    def _handle_location(location_td) -> str:
        return location_td.span["data-sort-value"].strip()

    @staticmethod
    def _handle_region(region_td) -> str:
        return region_td.a["title"].strip()


if __name__ == "__main__":
    parser = PopulationParser()

    parsed_data = parser.fetch_data()
    parser.save_data(parsed_data)
