import os
from decouple import config

DEBUG = config('DEBUG', cast=bool, default=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = config('DATABASE_URL', default='sqlite:///sample.db')
RECORDING_HOURS_RANGE = config('RECORDING_HOURS_RANGE', default='3-18')
UPLOADING_HOURS_RANGE = config('UPLOADING_HOURS_RANGE', default='18-6')
MIGRATIONS_FOLDER = os.path.join(BASE_DIR, "migrations")
BUCKET_NAME = config('AWS_BUCKET', default='')
S3_KEY = config('AWS_S3_KEY', default='')
S3_SECRET = config('AWS_S3_SECRET', default='')
S3_REGION = config('AWS_REGION', default='')
RECORDING_FOLDER = config('RECORDING_FOLDER', default='$HOME/recordings')
