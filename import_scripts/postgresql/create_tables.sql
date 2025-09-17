CREATE TABLE IF NOT EXISTS standards_framework_item (
    "identifier" TEXT,
    "caseIdentifierURI" TEXT,
    "caseIdentifierUUID" TEXT,
    "statementCode" TEXT,
    "description" TEXT,
    "statementType" TEXT,
    "normalizedStatementType" TEXT,
    "jurisdiction" TEXT,
    "academicSubject" TEXT,
    "gradeLevel" JSON,
    "inLanguage" TEXT,
    "dateCreated" DATE,
    "dateModified" DATE,
    "notes" TEXT,
    "author" TEXT,
    "provider" TEXT,
    "license" TEXT,
    "attributionStatement" TEXT
);

CREATE TABLE IF NOT EXISTS standards_framework (
    "identifier" TEXT,
    "caseIdentifierURI" TEXT,
    "caseIdentifierUUID" TEXT,
    "name" TEXT,
    "description" TEXT,
    "jurisdiction" TEXT,
    "academicSubject" TEXT,
    "inLanguage" TEXT,
    "adoptionStatus" TEXT,
    "dateCreated" DATE,
    "dateModified" DATE,
    "notes" TEXT,
    "author" TEXT,
    "provider" TEXT,
    "license" TEXT,
    "attributionStatement" TEXT
);

CREATE TABLE IF NOT EXISTS learning_component (
    "identifier" TEXT,
    "description" TEXT,
    "academicSubject" TEXT,
    "inLanguage" TEXT,
    "dateCreated" DATE,
    "dateModified" DATE,
    "author" TEXT,
    "provider" TEXT,
    "license" TEXT,
    "attributionStatement" TEXT
);

CREATE TABLE IF NOT EXISTS relationships (
    "identifier" TEXT,
    "relationshipType" TEXT,
    "description" TEXT,
    "sourceEntity" TEXT,
    "sourceEntityKey" TEXT,
    "sourceEntityValue" TEXT,
    "targetEntity" TEXT,
    "targetEntityKey" TEXT,
    "targetEntityValue" TEXT,
    "dateCreated" DATE,
    "dateModified" DATE,
    "author" TEXT,
    "provider" TEXT,
    "license" TEXT,
    "attributionStatement" TEXT
);
