CREATE TABLE IF NOT EXISTS Tags (
    tag_id INTEGER PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Movements (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    concept VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    tag_id INT,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
);


INSERT INTO Tags (tag_id, tag_name) VALUES (1, 'TRANSPORT');
INSERT INTO Tags (tag_id, tag_name) VALUES (2,'PAYROLL');
INSERT INTO Tags (tag_id, tag_name) VALUES (3, 'PARTY');
INSERT INTO Tags (tag_id, tag_name) VALUES (4, 'MATERIAL');
INSERT INTO Tags (tag_id, tag_name) VALUES (5,'SUPERMERCAT');
INSERT INTO Tags (tag_id, tag_name) VALUES (6, 'OTHER');
INSERT INTO Tags (tag_id, tag_name) VALUES (7, 'GENERAL');
INSERT INTO Tags (tag_id, tag_name) VALUES (8, 'BAR/REST.');