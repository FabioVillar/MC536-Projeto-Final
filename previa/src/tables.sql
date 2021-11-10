DROP TABLE if exists Awards_wc;

DROP TABLE if exists Events_wc;

DROP TABLE if exists Match_wc;

DROP TABLE if exists Player_wc;

DROP TABLE if exists Team_wc;

DROP TABLE if exists Group_wc;

DROP TABLE if exists WorldCup;

-- WC -> Group -> team -> player -> match -> events -> awards 
CREATE TABLE if not exists WorldCup (
    year_wc INTEGER not null,
    host VARCHAR(50) not null,
    PRIMARY KEY(Year_wc)
);


CREATE TABLE if not exists Team_wc(
    team_id integer NOT NULL AUTO_INCREMENT,
    year_wc integer not null,
    team_name VARCHAR(50) not null,
    coach VARCHAR(50) not null,
    group_in_wc VARCHAR(50) not null,
    group_points INTEGER not null,
    ranking_group INTEGER not null,
    goals_scored INTEGER not null,
    goals_suffered INTEGER not null,
    wins INTEGER not null,
    draws INTEGER not null,
    losses INTEGER not null,
    PRIMARY key(team_id),
    FOREIGN key(year_wc) REFERENCES WorldCup(year_wc)
);

CREATE TABLE Player_wc (
    player_id integer NOT NULL AUTO_INCREMENT,
    team_name VARCHAR(50) not null,
    team_id integer not null,
    player_name VARCHAR(50) not null,
    player_number INTEGER not null,
    age INTEGER not null,
    position VARCHAR(50) not null,
    goals INTEGER not null,
    assists INTEGER not NULL,
    yellow_cards INTEGER not null,
    red_cards INTEGER not null,
    PRIMARY key(player_id),
    FOREIGN KEY(team_id) REFERENCES Team_wc(team_id)
);

CREATE TABLE Match_wc (
    match_id INTEGER not null AUTO_INCREMENT,
    penaltys VARCHAR(50),
    phase VARCHAR(50) not null,
    teamA integer NOT null,
    teamB integer not null,
    score VARCHAR(50) not null,
    stadium VARCHAR(50),
    attendance INTEGER,
    referee VARCHAR(50),
    formation_A VARCHAR(50),
    formation_B VARCHAR(50),
    lineupA TEXT,
    lineupB TEXT,
    reservesA TEXT,
    reservesB TEXT,
    possesion VARCHAR(50),
    PRIMARY key(match_id),
    FOREIGN KEY(teamA) REFERENCES Team_wc(team_id),
    FOREIGN KEY(teamB) REFERENCES Team_wc(team_id)
);

CREATE TABLE Events_wc (
    event_id integer not null,
    match_id INTEGER not null,
    event_desc TEXT not null,
    match_time float,
    team integer not null,
    player integer not null,
    PRIMARY key(event_id),
    FOREIGN KEY(player) REFERENCES Player_wc(player_id),
    FOREIGN KEY(team) REFERENCES Team_wc(team_id),
    FOREIGN Key(match_Id) REFERENCES Match_wc(match_id)
);

CREATE TABLE Awards_wc (
    award_type TEXT,
    year_wc INTEGER not null,
    player integer not null,
    team integer not null,
    FOREIGN KEY(year_wc) REFERENCES WorldCup(year_wc),
    FOREIGN Key(player) REFERENCES Player_wc(player_id)
);