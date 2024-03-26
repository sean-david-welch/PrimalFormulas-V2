-- Created Schemas
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    image TEXT,
    created TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE stock_information (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL, 
    sku TEXT,
    quantity INTEGER, 
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE about (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    image TEXT,
    created TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE assets (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT now() 
);

-- Update UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

ALTER TABLE products ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE stock_information ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE about ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE assets ALTER COLUMN id SET DEFAULT uuid_generate_v4();
