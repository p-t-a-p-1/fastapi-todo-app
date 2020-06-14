DROP DATABASE IF EXISTS sample_db;
CREATE DATABASE sample_db;
USE sample_db;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    mail VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE task (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content VARCHAR(255) NOT NULL,
    deadline DATETIME,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    done BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE
);

INSERT INTO user (username, password, mail) VALUES ('test1', 'pass', 'aaa@aaa.com');
INSERT INTO user (username, password, mail) VALUES ('test2', 'pass2', 'bbb@bbb.com');
INSERT INTO task (user_id, content, deadline, date, done) VALUES (1, 'testTODO', '2021-01-01 00:00:00', '2020-01-01 00:00:00', 1);
