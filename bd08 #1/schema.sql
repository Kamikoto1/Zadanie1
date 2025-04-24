CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    is_logged_in BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50),
    action_object_id INT,
    action_description TEXT,
    server_response VARCHAR(50),
    action_datetime DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL
);