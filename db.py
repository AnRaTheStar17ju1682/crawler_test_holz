import aiosqlite
from typing import Sequence
from pandas import DataFrame


class DB:
    def __init__(self, name):
        self.name = name
    
       
    async def init_db(self):
        async with aiosqlite.connect(self.name) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS sites (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   url TEXT NOT NULL,
                   xpath TEXT NOT NULL)"""
                )
            await db.commit()
    

    async def insert_new_sites(self, excel_data: DataFrame):    
        async with aiosqlite.connect(self.name) as db:
            await db.executemany(
                """INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)""",
                excel_data[['title', 'url', 'xpath']].itertuples(index=False)
            )
            await db.commit()
    
    
    async def get_sites_data(self) -> Sequence[tuple[str, str, str]]:
        async with aiosqlite.connect(self.name) as db:
            async with db.execute('SELECT title, url, xpath FROM sites') as cursor:
                rows = await cursor.fetchall()
                return tuple(rows) 