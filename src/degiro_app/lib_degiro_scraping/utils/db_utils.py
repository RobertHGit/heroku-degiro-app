import os
from sqlalchemy.engine.create import create_engine


def get_db_engine():
    final_db_url = "postgresql+psycopg2://" + os.environ.get("DATABASE_URL").lstrip("postgres://")
    return create_engine(final_db_url)
