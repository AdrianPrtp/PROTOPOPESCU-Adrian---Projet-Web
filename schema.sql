DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS emergency_profile;
DROP TABLE IF EXISTS instructions;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE emergency_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    condition_name TEXT NOT NULL, 
    emergency_contact TEXT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    symptom TEXT NOT NULL, 
    action TEXT NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES emergency_profile (id)
);