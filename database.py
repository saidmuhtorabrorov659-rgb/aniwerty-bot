import aiosqlite

DB_NAME = "aniwerty.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anime_id INTEGER,
                video_file_id TEXT,
                FOREIGN KEY (anime_id) REFERENCES anime (id)
            )
        """)
        await db.commit()

async def get_anime(anime_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT title, description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            return await cursor.fetchone()

async def add_anime(anime_id: int, title: str, description: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO anime (id, title, description) VALUES (?, ?, ?)", (anime_id, title, description))
        await db.commit()