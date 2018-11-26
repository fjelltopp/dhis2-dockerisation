UPDATE
  users
SET
  password = '$2a$10$40.AJANpSQYryO5Sl4kqjuwhmLLWS1XycPrv1xC.DD.prEt1pMEY.'
WHERE
  username = 'Tomasz';

INSERT INTO userrolemembers
  (userid, userroleid)
SELECT
  users.userid, userrole.userroleid
FROM
  users, userrole
WHERE
  users.username = 'Tomasz'
AND
  userrole.name = 'Superuser'
ON CONFLICT
  DO NOTHING;