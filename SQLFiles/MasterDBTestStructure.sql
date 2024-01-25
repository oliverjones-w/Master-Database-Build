CREATE TABLE FirmType(
    FirmTypeID INT IDENTITY PRIMARY KEY,
    FirmTypeName VARCHAR(255)
);

CREATE TABLE Firm (
    FirmID INT IDENTITY PRIMARY KEY,
    FirmName VARCHAR(255),
    FirmTypeID INT FOREIGN KEY REFERENCES FirmType(FirmTypeID)
);

CREATE TABLE Name (
    NameID INT IDENTITY PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255)
);

CREATE TABLE ContextualTitle (
    ContextualTitleID INT IDENTITY PRIMARY KEY,
    ContextualTitleName VARCHAR(255)
);

CREATE TABLE HierarchicalTitle(
    HierarchicalTitleID INT IDENTITY PRIMARY KEY,
    HierarchicalTitleName VARCHAR(255)
);

CREATE TABLE Region(
    RegionID INT IDENTITY PRIMARY KEY,
    RegionName VARCHAR(255)
);

CREATE TABLE Location (
    LocationID INT IDENTITY PRIMARY KEY,
    LocationName VARCHAR(255),
    RegionID INT FOREIGN KEY REFERENCES Region(RegionID)
);

CREATE TABLE [Function](
    FunctionID INT IDENTITY PRIMARY KEY,
    FunctionName VARCHAR(255)
);

CREATE TABLE Currency(
    CurrencyID INT IDENTITY PRIMARY KEY,
    CurrencyCode VARCHAR(255),
    CurrencyName VARCHAR(255)
);

CREATE TABLE GroupDesk(
    GroupDeskID INT IDENTITY PRIMARY KEY,
    GroupDeskName VARCHAR(255)
);

CREATE TABLE Focus(
    FocusID INT IDENTITY PRIMARY KEY,
    FocusName VARCHAR(255)
);

CREATE TABLE ProfileNotes(
    ProfileNoteID INT IDENTITY PRIMARY KEY,
    NameID INT FOREIGN KEY REFERENCES Name(NameID),
    NoteContent VARCHAR(MAX),
    DateCreated DATETIME
);

CREATE TABLE ClientCoverage(
    ClientCoverageID INT IDENTITY PRIMARY KEY,
    CoverageName VARCHAR(255)
);

CREATE TABLE SectorCoverage(
    SectorCoverageID INT IDENTITY PRIMARY KEY,
    SectorName VARCHAR(255)
);

CREATE TABLE Date (
    DateID INT IDENTITY PRIMARY KEY,
    Date DATETIME,
    Year INT,
    Quarter INT,
    Month INT,
    Week INT,
    DayofWeek INT
);

CREATE TABLE Position(
    PositionID INT IDENTITY PRIMARY KEY,
    NameID INT FOREIGN KEY REFERENCES Name(NameID),
    FirmID INT FOREIGN KEY REFERENCES Firm(FirmID),
    HierarchicalTitleID INT FOREIGN KEY REFERENCES HierarchicalTitle(HierarchicalTitleID),
    ContextualTitleID INT FOREIGN KEY REFERENCES ContextualTitle(ContextualTitleID),
    GroupDeskID INT FOREIGN KEY REFERENCES GroupDesk(GroupDeskID),
    StartDateID INT FOREIGN KEY REFERENCES Date(DateID),
    EndDateID INT FOREIGN KEY REFERENCES Date(DateID)
);

--Create Junction tables for Many-to-Many Relationships
CREATE TABLE FirmLocation (
    FirmLocationID INT IDENTITY PRIMARY KEY,
    FirmID INT FOREIGN KEY REFERENCES Firm(FirmID),
    LocationID INT FOREIGN KEY REFERENCES Location(LocationID)
);

CREATE TABLE PositionLocation(
    PositionLocationID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    LocationID INT FOREIGN KEY REFERENCES Location(LocationID)
);

CREATE TABLE PositionCurrency(
    PositionCurrencyID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    CurrencyID INT FOREIGN KEY REFERENCES Currency(CurrencyID)
);

CREATE TABLE PositionFunction(
    PositionFunctionID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    FunctionID INT FOREIGN KEY REFERENCES [Function](FunctionID)
);

CREATE TABLE PositionFocus (
    PositionFocusID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    FocusID INT FOREIGN KEY REFERENCES Focus(FocusID)
);

CREATE TABLE PositionClientCoverage (
    PositionClientCoverageID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    ClientCoverageID INT FOREIGN KEY REFERENCES ClientCoverage(ClientCoverageID)
);

CREATE TABLE PositionSectorCoverage (
    PositionSectorCoverageID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    SectorCoverageID INT FOREIGN KEY REFERENCES SectorCoverage(SectorCoverageID)
);

CREATE TABLE PositionReportsTo (
    PositionReportsToID INT IDENTITY PRIMARY KEY,
    PositionID INT FOREIGN KEY REFERENCES Position(PositionID),
    ReporterNameID INT FOREIGN KEY REFERENCES Name(NameID)
);
