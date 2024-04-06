from sqlalchemy import func, select

from database import Session, Country, Region


if __name__ == "__main__":
    with Session() as session:
        query = select(
            Region.name.label("region_name"),
            func.sum(Country.population).label("total_population"),
            func.max(Country.population).label("max_country_population"),
            func.min(Country.population).label("min_country_population"),
            select(
                Country.name
            ).where(
                Country.region_id == Region.id
            ).order_by(
                Country.population.asc()
            ).limit(
                1
            ).correlate(
                Region
            ).scalar_subquery().label("name_min_country_population"),
            select(
                Country.name
            ).where(
                Country.region_id == Region.id
            ).order_by(
                Country.population.desc()
            ).limit(
                1
            ).correlate(
                Region
            ).scalar_subquery().label("name_max_country_population")

        ).join(
            Country
        ).group_by(Region.name, Region.id).order_by("total_population")

        result = session.execute(query).fetchall()

        for row in result:
            print(
                "Name of the region: ",
                row.region_name
            )
            print(
                "Total population of the region: ",
                row.total_population
            )
            print(
                "Name of the largest country in the region (by population): ",
                row.name_max_country_population
            )
            print(
                "Population of the largest country in the region: ",
                row.max_country_population
            )
            print(
                "Name of the smallest country in the region",
                row.name_min_country_population
            )
            print(
                "Population of the smallest country in the region: ",
                row.min_country_population
            )
