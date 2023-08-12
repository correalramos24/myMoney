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


INSERT INTO Tags (tag_id, tag_name) VALUES
    (1, 'TRANSPORT'),(2,'PAYROLL'),(3, 'PARTY'),
    (4, 'MATERIAL'),(5,'SUPERMERCAT'),(6, 'OTHER'),
    (7, 'GENERAL');