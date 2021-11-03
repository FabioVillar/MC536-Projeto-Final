CREATE TABLE WorldCup (
  Year INTEGER,
  Host VARCHAR(50),
  NumberOfParticipants INTEGER,
  Winner VARCHAR(50),
  PRIMARY KEY(Year)
)

CREATE TABLE Awards (
  GoldenGlove VARCHAR(50),
  GoldenShoe VARCHAR(50),
  Year INTEGER,
  FOREIGN KEY(Year)
    REFERENCES WorldCup(Year)
)

CREATE TABLE Phase (
  Type VARCHAR(50),
  Year INTEGER,
  FOREIGN KEY(Year)
    REFERENCES WorldCup(Year)
)

CREATE TABLE Group (
  Id VARCHAR(50),
  NumberOfTeams INTEGER,
  FOREIGN KEY(Year)
    REFERENCES Phase(Year)
)

CREATE TABLE Team (
  GroupId VARCHAR(50),
  Name VARCHAR(50),
  NumberOfPlayers INTEGER,
  Coach VARCHAR(50),
  NumberOfPoints INTEGER,
  Rank INTEGER,
  GoalsScored INTEGER,
  GoalsSuffered INTEGER,
  Wins INTEGER,
  Draws INTEGER,
  Looses INTEGER,
  FOREIGN KEY(GroupId)
    REFERENCES Group(Id)
)

CREATE TABLE Player (
  Team VARCHAR(50),
  Name VARCHAR(50),
  Number INTEGER,
  Age INTEGER,
  Position VARCHAR(50),
  Goals INTEGER,
  YellowCards INTEGER,
  RedCards INTEGER,
  FOREIGN KEY(Team)
    REFERENCES Team(Name)
)

CREATE TABLE Match (
  Id INTEGER,
  Phase VARCHAR(50),
  TeamA VARCHAR(50),
  TeamB VARCHAR(50),
  GoalsA INTEGER,
  GoalsB INTEGER,
  Stadium VARCHAR(50),
  Attendance INTEGER,
  Referee VARCHAR(50),
  FormationA VARCHAR(50),
  FormationB VARCHAR(50),
  LineupA VARCHAR(200),
  LineupB VARCHAR(200),
  ReservesA VARCHAR(200),
  ReservesB VARCHAR(200),
  BallPossessionA INTEGER,
  BallPossessionB INTEGER,
  FOREIGN KEY(TeamA)
    REFERENCES Team(Name)
  FOREIGN KEY(TeamB)
    REFERENCES Team(Name)
  FOREIGN KEY(Phase)
    REFERENCES Phase(Type)
)

CREATE TABLE Event (
  MatchId INTEGER,
  PlayerName VARCHAR(50),
  TeamName VARCHAR(50),
  YellowCard VARCHAR(50),
  RedCard VARCHAR(50),
  GoalPlayer VARCHAR(50),
  Exit VARCHAR(50),
  Enter VARCHAR(50),
  FOREIGN KEY(PlayerName)
    REFERENCES Player(Name)
  FOREIGN KEY(TeamName)
    REFERENCES Team(Name)
)
    
  
  


  
  
   
