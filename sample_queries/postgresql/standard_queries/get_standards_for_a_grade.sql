SELECT *
FROM standards_framework_item
WHERE EXISTS (
  SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem 
  WHERE elem = '6'
)
AND "jurisdiction" = 'Multi-State';