SELECT parent.*
FROM relationships r
JOIN standards_framework_item parent
  ON parent.`caseIdentifierUUID` = r.`sourceEntityValue`
WHERE r.`relationshipType` = 'hasChild'
  AND r.`sourceEntity` = 'StandardsFrameworkItem'
  AND r.`sourceEntityKey` = 'caseIdentifierUUID'
  AND r.`targetEntity` = 'StandardsFrameworkItem'
  AND r.`targetEntityKey` = 'caseIdentifierUUID'
  AND r.`targetEntityValue` = '57165d0c-d7cc-11e8-824f-0242ac160002';