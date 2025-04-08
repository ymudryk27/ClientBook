DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO clients (name, email, phone) VALUES ('Yaroslav Mudryk', 'ymudrik2005@gmail.com', '731165362');
INSERT INTO clients (name, email, phone) VALUES ('Anna Kowalska', 'annak@gmail.com', '731165001');
INSERT INTO clients (name, email, phone) VALUES ('Jan Nowak', 'jann@gmail.com', '731165002');
INSERT INTO clients (name, email, phone) VALUES ('Kamil Zielinski', 'kamilz@gmail.com', '731165003');
INSERT INTO clients (name, email, phone) VALUES ('Ola Maj', 'olamaj@gmail.com', '731165004');
INSERT INTO clients (name, email, phone) VALUES ('Piotr Lewandowski', 'piotrl@gmail.com', '731165005');
INSERT INTO clients (name, email, phone) VALUES ('Marta Wisniewska', 'martaw@gmail.com', '731165006');
INSERT INTO clients (name, email, phone) VALUES ('Tomasz Wójcik', 'tomaszw@gmail.com', '731165007');
INSERT INTO clients (name, email, phone) VALUES ('Kasia Nowicka', 'kasian@gmail.com', '731165008');
INSERT INTO clients (name, email, phone) VALUES ('Bartek Kaczmarek', 'bartekk@gmail.com', '731165009');