import pymysql.cursors

t1 = """
CREATE TABLE IF NOT EXISTS devices (
  device VARCHAR(200) UNIQUE NOT NULL,
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
"""

t2 = """
CREATE TABLE IF NOT EXISTS battery (
  device INTEGER UNSIGNED NOT NULL,
  day DATE NOT NULL,
  minute SMALLINT UNSIGNED NOT NULL,
  value SMALLINT NOT NULL,
  PRIMARY KEY(device, minute, day),
  FOREIGN KEY (device) REFERENCES devices (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
"""

t3 = """
CREATE TABLE IF NOT EXISTS temperature (
  device INTEGER UNSIGNED NOT NULL,
  day DATE NOT NULL,
  minute SMALLINT UNSIGNED NOT NULL,
  value SMALLINT NOT NULL,
  PRIMARY KEY(device, minute, day),
  FOREIGN KEY (device) REFERENCES devices (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
"""

tables = [t1, t2, t3]

connection = pymysql.connect(host='localhost', user='test', password='password', db='tsdata', charset='utf8mb4',
														 cursorclass=pymysql.cursors.DictCursor)

try:
	with connection.cursor() as cursor:
		for q in tables:
			cursor.execute(q)
finally:
	connection.close()
