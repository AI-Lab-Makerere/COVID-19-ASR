from yoyo import get_backend
from yoyo import read_migrations
from os.path import join


class SQLMigrationHandler(object):
    def __init__(self, database_url, migration_folder):
        self.__backend = get_backend(database_url)
        resolved_migration_folder_path = self.full_folder_path(
            database_url=database_url,
            base_migration_folder=migration_folder
        )

        self.__migrations = read_migrations(resolved_migration_folder_path)

    @staticmethod
    def full_folder_path(database_url: str, base_migration_folder: str) -> str:
        if 'sqlite' in database_url:
            return join(base_migration_folder, 'sqlite3')
        if 'postgres' in database_url or 'postgresql' in database_url:
            return join(base_migration_folder, 'postgres')
        raise ValueError("unsupported data type for {}".format(database_url))

    def migrate(self) -> None:
        with self.__backend.lock():
            # Apply any outstanding migrations
            self.__backend.apply_migrations(self.__backend.to_apply(self.__migrations))

    def rollback(self) -> None:
        with self.__backend.lock():
            # Rollback all migrations
            self.__backend.rollback_migrations(self.__backend.to_rollback(self.__migrations))
