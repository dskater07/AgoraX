CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'propietario',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150),
    start_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendiente'
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    meeting_id INT REFERENCES meetings(id),
    user_id INT REFERENCES users(id),
    vote_option VARCHAR(10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    UNIQUE(meeting_id, user_id)
);
