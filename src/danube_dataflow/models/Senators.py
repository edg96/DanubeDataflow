from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..scrappers.senators_scraper import scrape_senators_data

Base = declarative_base()


class Senators(Base):
    __tablename__ = "senators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    district_name = Column(String)
    district_number = Column(Integer)
    political_party = Column(String)

    __table_args_ = (UniqueConstraint("name"),)


DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/danube_dataflow"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def save_senators_to_postgres():
    init_db()
    db = SessionLocal()
    senators = scrape_senators_data()

    try:
        for senator in senators:
            exists = db.query(Senators).filter_by(name=senator["name"]).first()
            if not exists:
                new_senator = Senators(
                    name=senator["name"],
                    district_name=senator["electoralDistrictName"],
                    district_number=senator["electoralDistrictNumber"],
                    political_party=senator["politicalParty"],
                )
                db.add(new_senator)

        db.commit()
        print(f"Data ingestion complete for senators. Processed {len(senators)} records.")
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    save_senators_to_postgres()
