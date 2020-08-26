CREATE TABLE diamonds (
    carat FLOAT,
    cut varchar(14),
    color varchar(12),
    clarity varchar(12),
    depth FLOAT,
    "table" FLOAT,
    price NUMBER(19),
    x FLOAT,
    y FLOAT,
    z FLOAT
);



CREATE TABLE batting (
    "playerID" varchar(12),
    "yearID" NUMBER(19),
    stint NUMBER(19),
    "teamID" varchar(12),
    "lgID" varchar(12),
    "G" NUMBER(19),
    "AB" NUMBER(19),
    "R" NUMBER(19),
    "H" NUMBER(19),
    "X2B" NUMBER(19),
    "X3B" NUMBER(19),
    "HR" NUMBER(19),
    "RBI" NUMBER(19),
    "SB" NUMBER(19),
    "CS" NUMBER(19),
    "BB" NUMBER(19),
    "SO" NUMBER(19),
    "IBB" NUMBER(19),
    "HBP" NUMBER(19),
    "SH" NUMBER(19),
    "SF" NUMBER(19),
    "GIDP" NUMBER(19)
);




CREATE TABLE awards_players (
    "playerID" varchar(12),
    "awardID" varchar(12),
    "yearID" NUMBER(19),
    "lgID" varchar(12),
    tie varchar(12),
    notes varchar(12)
);



CREATE TABLE functional_alltypes (
    "index" NUMBER(19),
    "Unnamed: 0" NUMBER(19),
    id NUMBER(10),
    bool_col varchar(4),
    tinyint_col NUMBER(5),
    smallint_col NUMBER(5),
    int_col NUMBER(10),
    bigint_col NUMBER(10),
    float_col FLOAT(23),
    double_col DOUBLE PRECISION,
    date_string_col varchar(50),
    string_col varchar(50),
    timestamp_col TIMESTAMP,
    year NUMBER(10),
    month NUMBER(10)
);

CREATE INDEX "ix_functional_alltypes_index" ON functional_alltypes ("index");
