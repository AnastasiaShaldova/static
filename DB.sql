CREATE TABLE IF NOT EXISTS images(
id SERIAL PRIMARY KEY,
static_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS type_images(
id SERIAL PRIMARY KEY,
type_images VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
id SERIAL PRIMARY KEY,
last_name VARCHAR(80) NOT NULL,
first_name VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS users_images(
image_id int NOT NULL REFERENCES images(id),
user_id int NOT NULL REFERENCES users(id),
type_images_id int NOT NULL REFERENCES type_images(id)
);

