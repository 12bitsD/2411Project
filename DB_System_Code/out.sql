PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
-- 宴会
CREATE TABLE Banquet (
    BIN INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DateTime DATETIME NOT NULL,
    Address TEXT NOT NULL,
    Location TEXT NOT NULL,
    ContactFirstName TEXT NOT NULL,
    ContactLastName TEXT NOT NULL,
    Available TEXT CHECK(Available IN ('Y', 'N')) NOT NULL,
    Quota INTEGER NOT NULL CHECK(Quota > 0)
);
-- 菜单
CREATE TABLE Meal (
    MealID INTEGER PRIMARY KEY AUTOINCREMENT,
    BIN INTEGER NOT NULL,
    Type TEXT NOT NULL,
    DishName TEXT NOT NULL,
    Price REAL NOT NULL CHECK(Price >= 0),
    SpecialCuisine TEXT
);
-- 菜单与宴会的中间链接表
CREATE TABLE BanquetMeal (
    BIN INTEGER,
    MealID INTEGER,
    PRIMARY KEY (BIN, MealID),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (MealID) REFERENCES Meal(MealID) ON DELETE CASCADE ON UPDATE RESTRICT
);
-- 参与者
CREATE TABLE AttendeesAccount (
    AccountID TEXT PRIMARY KEY (AccountID LIKE '%@%'),
    BIN INTEGER NOT NULL,
    FirstName TEXT NOT NULL CHECK (FirstName GLOB '[A-Za-z]*'),
    LastName TEXT NOT NULL CHECK (LastName GLOB '[A-Za-z]*'),
    Address TEXT NOT NULL,
    AttendeeType TEXT NOT NULL CHECK (AttendeeType IN ('staff', 'student', 'alumni', 'guest')),
    Password TEXT NOT NULL,
    MobileNumber TEXT NOT NULL CHECK (MobileNumber GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    AffiliatedOrganization TEXT NOT NULL CHECK (AffiliatedOrganization IN ('PolyU', 'HKCC', 'SPEED', 'Others')),
    DrinkChoice TEXT,
    MealChoice TEXT,
    Remarks TEXT,
    SeatNumber INTEGER NOT NULL,
    FOREIGN KEY (BIN) REFERENCES Banquets (BIN) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (MealChoice) REFERENCES Meal (Meal_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- 舍弃中间表将信息全部汇总至Attendees
-- CREATE TABLE Registrations (
--     RegistrationID INTEGER PRIMARY KEY AUTOINCREMENT,
--     RegistrationDate DATE NOT NULL,
--     AccountID TEXT NOT NULL,
--     BIN INTEGER NOT NULL,
--     DrinkChoice TEXT
--     MealChoice TEXT,
--     Remarks TEXT,
--     SeatNumber INTEGER NOT NULL,
--     FOREIGN KEY (AccountID) REFERENCES AttendeesAccount (AccountID) ON DELETE CASCADE ON UPDATE RESTRICT,
--     FOREIGN KEY (BIN) REFERENCES Banquets (BIN) ON DELETE CASCADE ON UPDATE RESTRICT,
--     FOREIGN KEY (MealChoice) REFERENCES Meal (Meal_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
-- );
DELETE FROM sqlite_sequence;
COMMIT;
