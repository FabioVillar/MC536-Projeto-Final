DROP TABLE if exists Awards_wc;

DROP TABLE if exists Events_wc;

DROP TABLE if exists Match_wc;

DROP TABLE if exists Player_wc;

DROP TABLE if exists Team_wc;

DROP TABLE if exists Group_wc;

DROP TABLE if exists WorldCup;

-- WC -> Group -> team -> player -> match -> events -> awards 
CREATE TABLE  WorldCup (
    id INTEGER not null AUTO_INCREMENT,
    host VARCHAR(50) not null,
    PRIMARY KEY(id)
);


CREATE TABLE  Team_wc(
    id VARCHAR(256) NOT NULL,
    year_wc integer not null,
    team_name VARCHAR(50) not null,
    coach VARCHAR(50) not null,
    group_in_wc VARCHAR(50) not null,
    group_points INTEGER not null,
    goals_scored INTEGER not null,
    overall_points integer not null,
    goals_conceded INTEGER not null,
    wins INTEGER not null,
    draws INTEGER not null,
    losses INTEGER not null,
    PRIMARY key(id),
    FOREIGN key(year_wc) REFERENCES WorldCup(id)
);

CREATE TABLE Player_wc (
    id VARCHAR(256) NOT NULL,
    team_id VARCHAR(256) not null,
    player_name VARCHAR(50) not null,
    age INTEGER not null,
    position VARCHAR(50) not null,
    goals INTEGER not null,
    assists INTEGER not NULL,
    yellow_cards INTEGER not null,
    red_cards INTEGER not null,
    year_wc integer not null,
    PRIMARY key(id),
    FOREIGN key(year_wc) REFERENCES WorldCup(id),
    FOREIGN KEY(team_id) REFERENCES Team_wc(id)
);

CREATE TABLE Match_wc (
    id VARCHAR(256) not null,
    penalties VARCHAR(50),
    phase VARCHAR(50) not null,
    teamA VARCHAR(256) null,
    teamB VARCHAR(256) not null,
    score VARCHAR(50) not null,
    stadium VARCHAR(200),
    attendance text,
    referee VARCHAR(200),
    formation_A TEXT,
    formation_B text,
    lineupA TEXT,
    lineupB TEXT,
    reservesA TEXT,
    reservesB TEXT,
    possesion VARCHAR(50),
    year_wc integer not null,
    PRIMARY key(id),
    FOREIGN KEY(year_wc) REFERENCES WorldCup(id),
    FOREIGN KEY(teamA) REFERENCES Team_wc(id),
    FOREIGN KEY(teamB) REFERENCES Team_wc(id)
);

CREATE TABLE Events_wc (
    id VARCHAR(256) not null,
    match_id VARCHAR(256) not null,
    event_desc TEXT not null,
    match_time text,
    team VARCHAR(256) not null,
    player VARCHAR(256) not null,
    PRIMARY key(id),
    FOREIGN KEY(player) REFERENCES Player_wc(id),
    FOREIGN KEY(team) REFERENCES Team_wc(id),
    FOREIGN Key(match_Id) REFERENCES Match_wc(id)
);

CREATE TABLE Awards_wc (
    award_type TEXT,
    year_wc INTEGER not null,
    player_id VARCHAR(256) not null,
    team VARCHAR(256) not null,
    FOREIGN KEY(year_wc) REFERENCES WorldCup(id),
    FOREIGN Key(player_id) REFERENCES Player_wc(id)
);