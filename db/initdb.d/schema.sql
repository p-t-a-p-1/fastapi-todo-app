CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    mail VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE task (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content VARCHAR(255) NOT NULL,
    deadline DATETIME default (NONE),
    date DATETIME default (CURRENT_DATE) NOT NULL,
    done BOOLEAN default (FALSE),
    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE
);