from typing import List

from sqlalchemy.orm import Session
from recording.recording_worker import RecordingConfiguration, RecordingWorker
import os

from settings import RECORDING_FOLDER


class RecordingRunner(object):
    def __init__(self, session: Session):
        self.__session = session
        self.__workers: List[RecordingWorker] = []

    def __fetch_configurations(self):
        query: str = "SELECT st.name, st.region, st.station, st.language, st.uri FROM station_tb AS st"
        results = self.__session.execute(query)
        configurations = [self.__pack_configuration(row=row, folder=self.__prepare_folder(row=row)) for row in results]
        return configurations

    @staticmethod
    def __pack_configuration(row, folder) -> RecordingConfiguration:
        return RecordingConfiguration(
            region=row['region'],
            station=row['station'],
            language=row['language'],
            uri=row['uri'],
            folder=folder
        )

    @staticmethod
    def __prepare_folder(row) -> str:
        folder: str = RECORDING_FOLDER + "/" + row["region"] + "/" + row["station"];
        if not os.path.exists(folder):
            os.mkdir(path=RECORDING_FOLDER + "/" + row["region"], mode=0o600)
            os.mkdir(path=RECORDING_FOLDER + "/" + row["region"] + "/" + row["station"], mode=0o600)
        return folder

    def __run_initiate_recorders(self):
        for configuration in self.__fetch_configurations():
            self.__workers.append(RecordingWorker(
                configuration=configuration,
                session=self.__session
            ))

    def start(self):
        for worker in self.__workers:
            worker.join()
