UPDATE drivers
SET %s = %s
WHERE id = %s
RETURNING *;