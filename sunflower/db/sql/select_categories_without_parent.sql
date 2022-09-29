SELECT *
FROM category
WHERE parent_id is null
LIMIT 5;
