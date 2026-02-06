-- Create products table

    CREATE TABLE IF NOT EXISTS products (
        name TEXT NOT NULL PRIMARY KEY,
        symbol TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        expiration TEXT NOT NULL
    );

INSERT INTO products (name, symbol, quantity, expiration) VALUES ('Mario', 'Ma', 21, '10-10-2003');
