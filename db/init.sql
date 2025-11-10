CREATE TABLE articles (
                        id SERIAL PRIMARY KEY,
                        link TEXT NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created TIMESTAMP NOT NULL,
                        sentiment NUMERIC(4,3) NOT NULL,
                        department TEXT NOT NULL,
                        lang TEXT DEFAULT 'en'
);

CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    department TEXT NOT NULL,
                    hashed_password TEXT NOT NULL,
                    created TIMESTAMP NOT NULL,
                    writeAcess BOOLEAN DEFAULT TRUE
);
