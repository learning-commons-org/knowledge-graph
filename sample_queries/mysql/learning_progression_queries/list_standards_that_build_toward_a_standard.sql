SELECT sfi.*
FROM relationships r
JOIN standards_framework_item sfi
  ON sfi.`caseIdentifierUUID` = r.`sourceEntityValue`
WHERE r.`relationshipType` = 'buildsTowards'
  AND r.`sourceEntity` = 'StandardsFrameworkItem'
  AND r.`sourceEntityKey` = 'caseIdentifierUUID'
  AND r.`targetEntity` = 'StandardsFrameworkItem'
  AND r.`targetEntityKey` = 'caseIdentifierUUID'
  AND r.`targetEntityValue` = '6ba1b8b8-d7cc-11e8-824f-0242ac160002';