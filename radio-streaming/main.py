import os

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app import App
from commands.migrate import SQLMigrationHandler
from settings import DATABASE_URL, MIGRATIONS_FOLDER, DEBUG
from storage.base import BaseModel


def initialize() -> App:
    engine = create_engine(
        DATABASE_URL,
        echo=DEBUG
    )

    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    BaseModel.set_session(session=session)
    BaseModel.prepare(engine, reflect=True)  # BaseModel.metadata.create_all(engine)
    app = App(session=session)
    return app


@click.command()
def run() -> None:
    app = initialize()
    app.run()


@click.command(help='run sql migrations on database')
def migrate():
    click.echo("DATABASE URL: {}\n".format(DATABASE_URL))
    click.echo("MIGRATIONS FOLDER: {}\n".format(MIGRATIONS_FOLDER))
    handler = SQLMigrationHandler(
        database_url=str(DATABASE_URL),
        migration_folder=MIGRATIONS_FOLDER
    )
    handler.migrate()


@click.command(help='rollback sql migrations on database')
def rollback():
    handler = SQLMigrationHandler(
        database_url=DATABASE_URL,
        migration_folder=MIGRATIONS_FOLDER
    )
    handler.rollback()


@click.command()
@click.option('--name', required=True, type=str, help='Name of the station')
@click.option('--language', required=True, type=str, help='Language the station broadcast in')
@click.option('--region', required=True, type=str, help='Region in the country')
@click.option('--url', required=True, type=str, help='URL to pick the recording from')
def add_station(name, language, region, url):
    app = initialize()
    app.add_station(
        name=name,
        language=language,
        region=region,
        url=url
    )


@click.command()
@click.option('--identifier', required=True, type=int, help='Integer ID for the Radio Station')
def remove_station(identifier: int) -> None:
    app = initialize()
    app.remove_station(identifier=identifier)


@click.command()
def list_stations():
    click.echo("STATIONS LIST")
    app = initialize()
    app.list_station()


@click.group()
def cli() -> None:
    pass


cli.add_command(rollback)
cli.add_command(migrate)
cli.add_command(add_station)
cli.add_command(remove_station)
cli.add_command(list_stations)
cli.add_command(run)

if __name__ == "__main__":
    cli()
