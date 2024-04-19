CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(id),
    name TEXT,
    time INTEGER,
    ingredients TEXT,
    instructions TEXT,
    created_at TIMESTAMP,
    category_id INTEGER REFERENCES categories(id),
    visible INTEGER
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id),
    visible INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id),
    stars INTEGER,
    comment TEXT
);

INSERT INTO categories (name, visible) VALUES ('Kasvisruoat', 1);
INSERT INTO categories (name, visible) VALUES ('Vegaaniset ruoat', 1);
INSERT INTO categories (name, visible) VALUES ('Alle 30 min valmistusaika', 1);