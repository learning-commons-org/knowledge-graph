WITH grade6_standards AS (
  SELECT `caseIdentifierUUID`
  FROM standards_framework_item
  WHERE `gradeLevel` LIKE '%"6"%'
),
supporting_components AS (
  SELECT DISTINCT r.`sourceEntityValue` AS lc_id
  FROM relationships r
  JOIN grade6_standards g
    ON g.`caseIdentifierUUID` = r.`targetEntityValue`
  WHERE r.`relationshipType` = 'supports'
    AND r.`sourceEntity` = 'LearningComponent'
    AND r.`sourceEntityKey` = 'identifier'
    AND r.`targetEntity` = 'StandardsFrameworkItem'
    AND r.`targetEntityKey` = 'caseIdentifierUUID'
)
SELECT lc.*
FROM learning_component lc
JOIN supporting_components c
  ON lc.`identifier` = c.lc_id;