-- WARNING: This recursive query may hit performance issues or database recursion limits
-- on large/deep hierarchies. If execution fails, either increase your database's recursion
-- limit settings or use an iterative approach in application code.

WITH RECURSIVE all_descendants AS (
  -- Base case: direct children of the StandardsFramework
  SELECT sfi.`caseIdentifierUUID`
  FROM relationships r
  JOIN standards_framework_item sfi
    ON sfi.`caseIdentifierUUID` = r.`targetEntityValue`
  WHERE r.`sourceEntity` = 'StandardsFramework'
    AND r.`sourceEntityKey` = 'caseIdentifierUUID'
    AND r.`sourceEntityValue` = 'c64961be-d7cb-11e8-824f-0242ac160002'
    AND r.`targetEntity` = 'StandardsFrameworkItem'
    AND r.`targetEntityKey` = 'caseIdentifierUUID'
  
  UNION ALL
  
  -- Recursive case: children of already found items
  SELECT sfi.`caseIdentifierUUID`
  FROM relationships r
  JOIN standards_framework_item sfi
    ON sfi.`caseIdentifierUUID` = r.`targetEntityValue`
  JOIN all_descendants ad
    ON ad.`caseIdentifierUUID` = r.`sourceEntityValue`
  WHERE r.`sourceEntity` = 'StandardsFrameworkItem'
    AND r.`sourceEntityKey` = 'caseIdentifierUUID'
    AND r.`targetEntity` = 'StandardsFrameworkItem'
    AND r.`targetEntityKey` = 'caseIdentifierUUID'
    AND r.`relationshipType` = 'hasChild'
)
SELECT `caseIdentifierUUID`
FROM all_descendants;