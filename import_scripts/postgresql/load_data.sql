-- Load data from CSV files (adjust paths to your downloaded files)
\COPY standards_framework_item FROM '/path/to/StandardsFrameworkItem.csv' DELIMITER ',' CSV HEADER;
\COPY standards_framework FROM '/path/to/StandardsFramework.csv' DELIMITER ',' CSV HEADER;
\COPY learning_component FROM '/path/to/LearningComponent.csv' DELIMITER ',' CSV HEADER;
\COPY relationships FROM '/path/to/Relationships.csv' DELIMITER ',' CSV HEADER;