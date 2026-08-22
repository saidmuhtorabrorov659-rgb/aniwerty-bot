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
        
        # Bazaga boshlang'ich animelarni qo'shish (agar bo'sh bo'lsa)
        async with db.execute("SELECT COUNT(*) FROM anime") as cursor:
            count = (await cursor.fetchone())[0]
            
        if count == 0:
            # 1. Zombi 100
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (1, "Zombi 100", "Komediya, Ekshn"))
            zombi_eps = [
                "BAACAgIAAxkDAAO_aoMrWJrqEhmS6FrmDMmdP1UgeWAAAtkuAAIh-oBJoEzm5rYLpyg9BA",
                "BAACAgIAAxkDAAPAaoMrWNwYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA",
                "BAACAgIAAxkDAAPBaoMrWKpeL_TdQ8fPnOSfDkJjWRAAAoItAAJ0qFhKPF6o7oaFIiA9BA",
                "BAACAgIAAxkDAAPCaoMrWPDNS-fiJhh3ZCDZOEWz74UAAts7AALTfeBKDD-6jImythI9BA",
                "BAACAgIAAxkDAAPDaoMrWDIAAVyYCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ",
                "BAACAgIAAxkDAAPEaoMrWC494xPJnJ4mFunfszXBOOMAAp43AAKeybhLOjn6sYqZE0Q9BA",
                "BAACAgIAAxkDAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnlIQA1xqWBJPG09BA",
                "BAACAgIAAxkDAAPGaoMrWDPq0re9FfptyQRwOqHUx1AAArE0AALxLnlI3fXJzO3flk49BA",
                "BAACAgIAAxkDAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtqGPUpNbuA9BA",
                "BAACAgIAAxkDAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA",
                "BAACAgIAAxkDAAPJaoMrWKqmMuZLE02W7t5IlCz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA",
                "BAACAgIAAxkDAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ"
            ]
            for ep in zombi_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (1, ep))

            # 2. Akademiyaning birinchi raqamli boy qizi
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (2, "Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan boʻldim", "Romantika"))
            akad_eps = [
                "BAACAgIAAxkDAAIBVmqG6uCIBQx6ZzcPotiUSZN-lPxCAAIapgAC51hoSjssBuD_2phrPQQ",
                "BAACAgIAAxkDAAIBV2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAjItoEoaVkHC4Zv7ED0E",
                "BAACAgIAAxkDAAIBWGqG6vZ3dtf7S9YdFLKmpjop49mDAAIErwAC38noSp0cgRXrYWllPQQ",
                "BAACAgIAAxkDAAIBWWqG6vuVr1X0Ygr3Wt2TmcXZAAEa0QACBKgAAhhdQUuGwUSkz1vu0z0E",
                "BAACAgIAAxkDAAIBWmqG6wSOq_hvZuPVA3c3oX2FjyE7AALoqgAC3C2AS5COMOI9-bHyPQQ",
                "BAACQAAxkBAAIBW2qG6wtI9O-ZDH0YTWDBTW0iTo3_AAJZHgACF6LoUz3imBALBhDOPQQ"
            ]
            for ep in akad_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (2, ep))

            # 3. Arra Odam (Chainsaw Man)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (3, "Arra Odam (Chainsaw Man)", "Ekshn, Qorong'u Fentezi, Shounen"))
            chainsaw_eps = [
                "BAACAgIAAxkDAAIB7mqJQdvtq0_8TqJX0MkL7PFL7zsYAAIDHwACXKNZs8JjwrjcGI_PQQ",
                "BAACAgIAAxkDAAIB72qJYXtAaYpxoqtecyI5JwAB7MdPpAgACfYMAA1t1YEu81jQzi6--ID0E",
                "BAACAgIAAxkDAAICWqJnunHnWC6RxmqAWiWyEX33asAAIEIgACLYgQSzoDERkp59oHPQQ",
                "BAACAgIAAxkDAAIC2qJnuzCir_Tqcc603qAQcskk95caAJyIgAcQNGgS0hxS1xKQdYVPQQ",
                "BAACAgIAAxkDAAICWqJnxH6rmNIQfsoB9qR0cN-vmhnAAK0IQACPaWBSwqr39AAAbW05D0E",
                "BAACAgIAAxkDAAICJ2qJnxcmlwXLARgTveGY0410YP2hAaAMEAAJE8flLmyi689aRjA9BA",
                "BAACAgIAAxkDAAICKWqJnxtfJgLeUKV61WTLuAAB_Oxx8wACgyMAAj50IEg_kp_3DD3dLTr0E",
                "BAACAgIAAxkDAAICK2qJnx9mUp34Qbk_z_RuJQyg1m2wAAIZKQAC3DaSvDSAiWvPGdPQQA",
                "BAACAgIAAxkDAAICLWqJnybZ6pEyCdqEerk32_y-WRyPAAiSNQAC3BAoSH26CMRr7plEPQQ",
                "BAACAgIAAxkDAAICL2qJnyo5a94Y0t4JJmBrp86hmIBTAAI2NQAC3BAoSFFJQNyPhI3PQQ",
                "BAACAgIAAxkDAAICMWqJny2ahrLKVfRkEP57reNZuDFIAAJENQAC3BAoS0AuMh1NiQxRPQQ",
                "BAACAgIAAxkDAAICWqJnYQJYUTipI3bcvscSBvCB_zVtnlAAAJWNQAIC3BAoSMnTmeaus90GPQQ",
                "BAACAgIAAxkDAAICNWqJnzcvGn80UUZCG9nm6_pLkxV-AAILkgAC80rRSegEI-Ds64PMPQQ"
            ]
            for ep in chainsaw_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (3, ep))

            await db.commit()

async def get_anime(anime_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT title, description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            return await cursor.fetchone()
