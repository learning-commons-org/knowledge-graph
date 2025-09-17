SELECT lc.*
FROM relationships r
JOIN learning_component lc
  ON lc."identifier" = r."sourceEntityValue"
WHERE r."relationshipType" = 'supports'
  AND r."sourceEntity" = 'LearningComponent'
  AND r."sourceEntityKey" = 'identifier'
  AND r."targetEntity" = 'StandardsFrameworkItem'
  AND r."targetEntityKey" = 'caseIdentifierUUID'
  AND r."targetEntityValue" = '6ba1c7ad-d7cc-11e8-824f-0242ac160002';