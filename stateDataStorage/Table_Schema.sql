create table if not exists barrels (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 itemCode TEXT,
 currentLevel REAL,
 remainStock REAL,
 remainStockTrigger REAL,
 dateExpiry TEXT, 
 dateCreated TEXT 
);

-- INSERT INTO barrels (itemCode, currentLevel, remainStock, remainStockTrigger) VALUES ("abc123",0.5, 4, 2);

