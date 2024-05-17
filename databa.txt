CREATE TABLE user (
        id INTEGER NOT NULL,
        email STRING(50) NOT NULL UNIQUE,
        password STRING(1000) NOT NULL,
        PRIMARY KEY (id)
);

CREATE TABLE task (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
	title STRING(50) NOT NULL,
	description TEXT,
	deadline DATETIME,
	status STRING(10) DEFAULT 'Not Done',
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES user(id)
);