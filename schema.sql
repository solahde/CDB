CREATE TABLE users
(
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE customer 
(
	id SERIAL PRIMARY KEY,
	name TEXT,
	sex_id INTEGER REFERENCES sex,
	language TEXT,
	age_group_id INTEGER REFERENCES age,
    phone VARCHAR,
    email TEXT
);
CREATE TABLE meeting
(
    id SERIAL PRIMARY KEY,
    date DATE,
    service_id INTEGER REFERENCES service,
    user_id INTEGER REFERENCES users, 
    customer_id INTEGER REFERENCES customer,
    customer_path TEXT,
    realization_id INTEGER REFERENCES realization,
    execution_id INTEGER REFERENCES execution,
    notes TEXT
);
CREATE TABLE sex
(
	id SERIAL PRIMARY KEY,
	sex TEXT
);
CREATE TABLE age
(
	id SERIAL PRIMARY KEY,
	age_group TEXT
);
CREATE TABLE service
(
	id SERIAL PRIMARY KEY,
	service TEXT
);
CREATE TABLE realization
(
	id SERIAL PRIMARY KEY,
	realization TEXT
);
CREATE TABLE execution
(
	id SERIAL PRIMARY KEY,
	execution TEXT
);