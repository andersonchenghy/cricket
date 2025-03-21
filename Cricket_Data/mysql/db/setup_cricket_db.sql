CREATE DATABASE IF NOT EXISTS cricket_data;
USE cricket_data;

CREATE TABLE venues (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255)
);

CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(255)
);

CREATE TABLE simulations (
    team_id INT,
    team VARCHAR(255),
    simulation_run INT,
    results INT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE games (
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    date DATE,
    venue_id INT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

-- First, insert the teams
INSERT INTO teams (team_id, team_name) VALUES
    (0, 'Peterborough Strikers'),
    (1, 'Huddersfield Heat'),
    (2, 'Rochdale Hurricanes'),
    (3, 'Doncaster Renegades'),
    (4, 'Hull Stars'),
    (5, 'Rotherham Scorchers'),
    (6, 'Blackpool Sixers'),
    (7, 'Castleford Thunder'),
    (8, 'Oldham Super Kings'),
    (9, 'Blackburn Knight Riders');

-- Then load venues and games data
LOAD DATA INFILE '/var/lib/mysql-files/test_data/venues.csv'
INTO TABLE venues
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/test_data/games.csv'
INTO TABLE games
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Finally load simulations data
LOAD DATA INFILE '/var/lib/mysql-files/test_data/simulations.csv'
INTO TABLE simulations
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

