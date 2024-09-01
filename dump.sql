CREATE DATABASE challenge_agriness_db;

CREATE TABLE batches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    piglet_count INTEGER NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE(),
    updated_at DATE DEFAULT CURRENT_DATE()
);
