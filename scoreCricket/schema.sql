DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS match_info;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE match_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scorer_id TEXT,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- TODO
  -- Find out how to change the date so that it is just the date (without time)
  -- (answer!) use .strftime() method to format date while rendering
  venue TEXT,
  team_a TEXT NOT NULL,
  team_b TEXT NOT NULL,
  team_a_runs INTEGER,
  team_b_runs INTEGER,
  FOREIGN KEY (scorer_id) REFERENCES user (username)
);
