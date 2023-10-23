UPDATE drivertimes
SET %s = %s
WHERE id = %s
RETURNING *;