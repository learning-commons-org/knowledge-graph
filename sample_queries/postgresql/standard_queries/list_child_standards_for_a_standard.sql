SELECT child.*
FROM relationships r
JOIN standards_framework_item child
  ON child."caseIdentifierUUID" = r."targetEntityValue"
WHERE r."relationshipType" = 'hasChild'
  AND r."sourceEntity" = 'StandardsFrameworkItem'
  AND r."sourceEntityKey" = 'caseIdentifierUUID'
  AND r."sourceEntityValue" = '57165a88-d7cc-11e8-824f-0242ac160002'
  AND r."targetEntity" = 'StandardsFrameworkItem'
  AND r."targetEntityKey" = 'caseIdentifierUUID';