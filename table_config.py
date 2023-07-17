from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class DistStyle(str, Enum):
    ALL = "ALL"
    AUTO = "AUTO"
    EVENT = "EVEN"


class Column(BaseModel):
    name: str
    datatype: str
    not_null: bool = True
    sort_key: bool = False
    dist_key: bool = False


class Table(BaseModel):
    name: str
    columns: List[Column]
    dist_style: Optional[DistStyle] = None


TABLES = [
    Table(
        name="staging_songs",
        columns=[
            Column(name='artist_id', datatype='VARCHAR(30)'),
            Column(name='artist_latitude', datatype='DECIMAL', not_null=False),
            Column(name='artist_longitude', datatype='DECIMAL', not_null=False),
            Column(name='artist_location', datatype='VARCHAR(256)', not_null=False),
            Column(name='artist_name', datatype='VARCHAR(256)'),
            Column(name='song_id', datatype='VARCHAR(30)'),
            Column(name='title', datatype='VARCHAR(256)', dist_key=True),
            Column(name='duration', datatype='DECIMAL'),
            Column(name='year', datatype='SMALLINT')
        ]
    ),
    Table(
        name="staging_events",
        columns=[
            Column(name='artist', datatype='VARCHAR(128)', not_null=False),
            Column(name='auth', datatype='VARCHAR(30)'),
            Column(name='firstName', datatype='VARCHAR(64)', not_null=False),
            Column(name='gender', datatype='VARCHAR(1)', not_null=False),
            Column(name='itemInSession', datatype='SMALLINT'),
            Column(name='lastName', datatype='VARCHAR(64)', not_null=False),
            Column(name='length', datatype='DECIMAL', not_null=False),
            Column(name='level', datatype='VARCHAR(10)'),
            Column(name='location', datatype='VARCHAR(256)', not_null=False),
            Column(name='method', datatype='VARCHAR(10)'),
            Column(name='page', datatype='VARCHAR(10)'),
            Column(name='registration', datatype='BIGINT', not_null=False),
            Column(name='sessionId', datatype='INTEGER'),
            Column(name='song', datatype='VARCHAR(256)', not_null=False, dist_key=True),
            Column(name='status', datatype='SMALLINT'),
            Column(name='ts', datatype='BIGINT'),
            Column(name='userAgent', datatype='VARCHAR(128)', not_null=False),
            Column(name='userId', datatype='SMALLINT', not_null=False)
        ]
    ),
    Table(
        name="songplays",
        columns=[
            Column(name='songplay_id', datatype='INTEGER IDENTITY(0,1)'),
            Column(name='start_time', datatype='TIMESTAMP', sort_key=True),
            Column(name='user_id', datatype='INTEGER'),
            Column(name='level', datatype='VARCHAR(10)'),
            Column(name='song_id', datatype='VARCHAR(30)', dist_key=True),
            Column(name='artist_id', datatype='VARCHAR(30)'),
            Column(name='session_id', datatype='INTEGER'),
            Column(name='location', datatype='VARCHAR(256)', not_null=False),
            Column(name='user_agent', datatype='VARCHAR(128)')
        ]
    ),
    Table(
        name="users",
        columns=[
            Column(name='user_id', datatype='INTEGER', sort_key=True),
            Column(name='first_name', datatype='VARCHAR(64)'),
            Column(name='last_name', datatype='VARCHAR(64)'),
            Column(name='gender', datatype='VARCHAR(1)'),
            Column(name='level', datatype='VARCHAR(10)')
        ],
        dist_style=DistStyle.ALL
    ),
    Table(
        name="songs",
        columns=[
            Column(name='song_id', datatype='VARCHAR(30)', dist_key=True, sort_key=True),
            Column(name='title', datatype='VARCHAR(256)'),
            Column(name='artist_id', datatype='VARCHAR(30)'),
            Column(name='year', datatype='SMALLINT'),
            Column(name='duration', datatype='DECIMAL')
        ]
    ),
    Table(
        name="artists",
        columns=[
            Column(name='artist_id', datatype='VARCHAR(30)', sort_key=True),
            Column(name='name', datatype='VARCHAR(256)'),
            Column(name='location', datatype='VARCHAR(256)', not_null=False),
            Column(name='latitude', datatype='DECIMAL', not_null=False),
            Column(name='longitude', datatype='DECIMAL', not_null=False)
        ],
        dist_style=DistStyle.ALL
    ),
    Table(
        name="time",
        columns=[
            Column(name='start_time', datatype='TIMESTAMP', sort_key=True),
            Column(name='hour', datatype='SMALLINT'),
            Column(name='day', datatype='SMALLINT'),
            Column(name='week', datatype='SMALLINT'),
            Column(name='month', datatype='SMALLINT'),
            Column(name='year', datatype='SMALLINT'),
            Column(name='weekday', datatype='BOOL'),
        ]
    )
]


def get_table(table_name: str) -> Table:
    return next((item for item in TABLES if item.name == table_name), None)
