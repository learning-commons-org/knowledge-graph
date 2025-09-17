SELECT sfi.*
FROM relationships r
JOIN standards_framework_item sfi
  ON sfi.`caseIdentifierUUID` = r.`targetEntityValue`
WHERE r.`relationshipType` = 'supports'
  AND r.`sourceEntity` = 'LearningComponent'
  AND r.`sourceEntityKey` = 'identifier'
  AND r.`targetEntity` = 'StandardsFrameworkItem'
  AND r.`targetEntityKey` = 'caseIdentifierUUID'
  AND r.`sourceEntityValue` = '019a93e7-1877-5e9b-b4b3-476f201fccc8';