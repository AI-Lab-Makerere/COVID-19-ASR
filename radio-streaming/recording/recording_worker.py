import os.path
import subprocess
import sys
import time
from datetime import datetime
from threading import Thread
from typing import List

from sqlalchemy.orm import Session


class RecordingConfiguration(object):
    def __init__(self, region: str, station: str, language: str, uri: str, folder: str):
        self.folder = folder
        self.uri = uri
        self.language = language
        self.station = station
        self.region = region


class ContentMeta(object):
    def __init__(self, filename: str, filepath: str, started_at: datetime, ended_at: datetime, size: int):
        self.filename = filename
        self.filepath = filepath
        self.started_at = started_at
        self.ended_at = ended_at
        self.size = size


class RecordingWorker(Thread):
    def __init__(self, configuration: RecordingConfiguration, session: Session):
        super().__init__(self)
        self.__session = session
        self.__is_running = True
        self.__configuration = configuration

    def run(self) -> None:
        self.__record_audios(time_limit=300)

    def __record_audios(self, time_limit: int) -> None:
        while self.__is_running:
            start_time = datetime.now()
            generated_contents = self.__record_audio_files(start_time=start_time, time_limit=time_limit)
            for content in generated_contents:
                self.__persist_file_information(information=content)

    def __record_audio_files(self, start_time: datetime, time_limit: int) -> List[ContentMeta]:
        generated_content = []
        time_format = "%d-%m-%Y-T-%H:%M:%S"
        prefix = "{}.{}".format(self.__configuration.station, start_time.strftime(time_format))
        filename = "{}.mp3".format(prefix)
        command = "streamripper {} -u Mozilla/5.0 -d {}/ -a {} -s -A -l {}".format(self.__configuration.uri,
                                                                                   self.__configuration.folder,
                                                                                   filename,
                                                                                   time_limit)
        result = subprocess.run(
            [sys.executable, command], capture_output=True, text=True
        )
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        if result.stderr is None:
            # Get the number of files that match the current file name in this folder
            list_command = "ls -a {}/{}*".format(self.__configuration.folder, prefix)
            result = subprocess.run([sys.executable, list_command], capture_output=True, text=True)

            files = result.stdout.split(" ")
            for file in files:
                absolute_filepath = "{}/{}".format(self.__configuration.folder, file.strip())
                start_timestamp = os.path.getctime(absolute_filepath)
                end_timestamp = os.path.getmtime(absolute_filepath)
                size = os.path.getsize(absolute_filepath)
                generated_content.append(ContentMeta(
                    filename=file,
                    filepath=absolute_filepath,
                    start_time=time.ctime(start_timestamp),
                    end_time=time.ctime(end_timestamp),
                    size=size
                ))
        return generated_content

    def __persist_file_information(self, information: ContentMeta) -> None:
        # Database connection will be made here
        # Call to persist the contents found in regards to the file in question
        statement: str = "INSERT INTO recording_tb(station_id, name, created_at, finished_at, file_size) " \
                         "VALUES(SELECT id FROM station_tb WHERE name=:station_name), :recording_name, :created_at, " \
                         ":finished_at, :file_size)"
        self.__session.execute(statement, params={'station_name': self.__configuration.station,
                                                  'recording_name': information.filename,
                                                  'created_at': information.started_at,
                                                  'finished_at': information.ended_at,
                                                  'file_size': information.size}
                               )
