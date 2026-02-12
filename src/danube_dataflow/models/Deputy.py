from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..scrappers.deputies_scraper import scrape_deputies_data

Base = declarative_base()


class Deputy(Base):
    __tablename__ = "deputies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    district_name = Column(String)
    district_number = Column(Integer)
    political_party = Column(String)

    __table_args__ = (UniqueConstraint("name"),)


DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/danube_dataflow"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def save_deputies_to_postgres():
    init_db()
    db = SessionLocal()
    deputies = scrape_deputies_data()

    try:
        for deputy in deputies:
            exists = db.query(Deputy).filter_by(name=deputy["name"]).first()
            if not exists:
                new_deputy = Deputy(
                    name=deputy["name"],
                    district_name=deputy["electoralDistrictName"],
                    district_number=deputy["electoralDistrictNumber"],
                    political_party=deputy["politicalParty"],
                )
                db.add(new_deputy)

        db.commit()
        print(f"Data ingestion complete for deputies. Processed {len(deputies)} records.")
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    save_deputies_to_postgres()
