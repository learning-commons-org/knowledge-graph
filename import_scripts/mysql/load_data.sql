-- Load data from CSV files (adjust paths to your downloaded files)
-- Note: Use mysql --local-infile=1 when running this script
LOAD DATA LOCAL INFILE '/path/to/StandardsFramework.csv'
INTO TABLE standards_framework
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/path/to/StandardsFrameworkItem.csv'
INTO TABLE standards_framework_item
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/path/to/LearningComponent.csv'
INTO TABLE learning_component
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/path/to/Relationships.csv'
INTO TABLE relationships
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;