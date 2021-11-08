DROP TABLE if exists Awards_wc;

DROP TABLE if exists Events_wc;

DROP TABLE if exists Match_wc;

DROP TABLE if exists Player_wc;

DROP TABLE if exists Team_wc;

DROP TABLE if exists Group_wc;

DROP TABLE if exists WorldCup;

-- WC -> Group -> team -> player -> match -> events -> awards 
CREATE TABLE if not exists WorldCup (
    Year_wc INTEGER not null,
    Host VARCHAR(50) not null,
    NumberOfParticipants INTEGER not null,
    Winner VARCHAR(50) not null,
    PRIMARY KEY(Year_wc)
);

CREATE TABLE if not exists Group_wc (
    Group_id VARCHAR(50) not null,
    NumberOfTeams INTEGER not null,
    Year_wc INTEGER not null,
    PRIMARY Key(Group_id),
    FOREIGN KEY(Year_wc) REFERENCES WorldCup(Year_wc)
);

CREATE TABLE if not exists Team_wc(
    Team_id integer NOT NULL AUTO_INCREMENT,
    Team_name VARCHAR(50) not null,
    NumberOfPlayers INTEGER not null,
    Coach VARCHAR(50) not null,
    Group_in_wc VARCHAR(50) not null,
    Group_points INTEGER not null,
    Ranking_group INTEGER not null,
    GoalsScored INTEGER not null,
    GoalsSuffered INTEGER not null,
    Wins INTEGER not null,
    Draws INTEGER not null,
    Looses INTEGER not null,
    PRIMARY key(team_id),
    FOREIGN KEY(Group_in_wc) REFERENCES Group_wc(Group_id)
);

CREATE TABLE Player_wc (
    Player_id integer NOT NULL AUTO_INCREMENT,
    Team_name VARCHAR(50) not null,
    Team_id integer not null,
    Player_name VARCHAR(50) not null,
    Player_number INTEGER not null,
    Age INTEGER not null,
    Position VARCHAR(50) not null,
    Goals INTEGER not null,
    YellowCards INTEGER not null,
    RedCards INTEGER not null,
    PRIMARY key(player_id),
    FOREIGN KEY(Team_id) REFERENCES Team_wc(Team_id)
);

CREATE TABLE Match_wc (
    Match_id INTEGER not null AUTO_INCREMENT,
    Penaltys VARCHAR(50),
    Phase VARCHAR(50) not null,
    TeamA integer NOT null,
    TeamB integer not null,
    Score VARCHAR(50) not null,
    Stadium VARCHAR(50),
    Attendance INTEGER,
    Referee VARCHAR(50),
    FormationA VARCHAR(50),
    FormationB VARCHAR(50),
    LineupA TEXT,
    LineupB TEXT,
    ReservesA TEXT,
    ReservesB TEXT,
    Possesion VARCHAR(50),
    PRIMARY key(Match_id),
    FOREIGN KEY(TeamA) REFERENCES Team_wc(Team_id),
    FOREIGN KEY(TeamB) REFERENCES Team_wc(Team_id)
);

CREATE TABLE Events_wc (
    Event_id integer not null,
    Match_id INTEGER not null,
    Event_desc TEXT not null,
    Match_time float,
    Team integer not null,
    Player integer not null,
    PRIMARY key(Event_id),
    FOREIGN KEY(Player) REFERENCES Player_wc(player_id),
    FOREIGN KEY(Team) REFERENCES Team_wc(Team_id),
    FOREIGN Key(Match_Id) REFERENCES Match_wc(Match_id)
);

CREATE TABLE Awards_wc (
    award_type TEXT,
    Year_wc INTEGER not null,
    Player integer not null,
    Team integer not null,
    FOREIGN KEY(Year_wc) REFERENCES WorldCup(Year_wc),
    FOREIGN Key(Player) REFERENCES Player_wc(Player_id)
);