BEGIN TRANSACTION;CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            login TEXT NOT NULL UNIQUE ,
            password_hash TEXT,
            is_admin INTEGER NOT NULL DEFAULT 0,
            is_block INTEGER NOT NULL DEFAULT 0,
            is_new INTEGER NOT NULL DEFAULT 1,
            is_pwd_rules INTEGER NOT NULL DEFAULT 0,
            re_pwd TEXT,
            text_pwd_rules TEXT
        );INSERT INTO "users" VALUES(1,'ADMIN',NULL,1,0,1,0,NULL,NULL);COMMIT;
