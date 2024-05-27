from prefect_sqlalchemy import SqlAlchemyConnector
from prefect import task, flow
database_block = SqlAlchemyConnector.load("postgresql")

@task(retries=2)
def create_user_table():
    with database_block as database:
        database.execute("CREATE TABLE IF NOT EXISTS customers (name varchar, address varchar);")
        database.execute_many(
            "INSERT INTO customers (name, address) VALUES (:name, :address);",
            seq_of_parameters=[
                {"name": "Ford", "address": "Highway 42"},
                {"name": "Unknown", "address": "Space"},
                {"name": "Me", "address": "Myway 88"},
            ],
        )


@flow(log_prints=True)
def create_tables():
    create_user_table()