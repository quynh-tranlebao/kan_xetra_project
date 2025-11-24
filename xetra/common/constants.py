"""
File to store constants
"""

from enum import Enum

class S3FileTypes(Enum):
    """support file type"""
    CSV = 'csv'
    PARQUET = 'parquet'

class MetaProcessFormat(Enum):
    """formation for meta process class"""
    META_DATE_FORMAT = '%Y-%m-%d'
    META_PROCESS_dATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    META_SOURCE_DATE_COL = 'source_date'
    META_PROCESS_COL = 'datetime_of_processing'
    META_FILE_FORMAT = 'csv'