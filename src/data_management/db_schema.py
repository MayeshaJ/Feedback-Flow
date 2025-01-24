
# Table creation statements
USER_TABLE = """
CREATE TABLE IF NOT EXISTS user (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
"""

TOPIC_TABLE = """
CREATE TABLE IF NOT EXISTS topic (
    id TEXT PRIMARY KEY,
    user_id INTEGER,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);
"""

REVIEW_TABLE = """
CREATE TABLE IF NOT EXISTS review (
    id TEXT PRIMARY KEY,
    user_id INTEGER,
    topic_id INTEGER,
    review_text TEXT,
    status TEXT,
    review_ratings TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topic (id) ON DELETE CASCADE
);
"""

SESSION_TABLE = """
CREATE TABLE IF NOT EXISTS session (
    id TEXT PRIMARY KEY,
    user_id INTEGER,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    last_activity_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);
"""

