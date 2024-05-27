from prefect_sqlalchemy import SyncDriver, SqlAlchemyConnector

from prefect_sqlalchemy import (
    SqlAlchemyConnector, ConnectionComponents
)

block = SqlAlchemyConnector(
    connection_info=ConnectionComponents(
        driver=SyncDriver.POSTGRESQL_PSYCOPG2,
        host="postgresql.playground.svc.cluster.local",
        username="admin",
        password="password",
        database="postgres"
    )
) 
block.save("postgresql", overwrite=True)