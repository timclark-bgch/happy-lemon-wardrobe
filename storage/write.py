import uuid
import warnings

import pymysql.cursors

import datetime
import itertools


def store(db, data):
	with db.cursor() as cursor:
		cursor.execute(__store(data), list(itertools.chain(*data)))
	db.commit()


__store_template = """
INSERT INTO battery (device, day, minute, value) VALUES {}
ON DUPLICATE KEY UPDATE 
 device = VALUES(device),
 day = VALUES(day),
 minute = VALUES(minute),
 value = VALUES(value)
"""


def __store(data):
	return __store_template.format(','.join('(%s, %s, %s, %s)' for _ in data))


def create_identifiers(db, labels):
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		with db.cursor() as cursor:
			cursor.execute(__identifiers(labels), labels)
		db.commit()


def __identifiers(labels):
	template = "INSERT IGNORE INTO devices (device) VALUES {}"
	return template.format(','.join('(%s)' for _ in labels))


def get_identifiers(db, labels):
	with db.cursor() as cursor:
		cursor.execute(__devices(labels), labels)
		return cursor.fetchall()


def __devices(labels):
	template = "SELECT device, id FROM devices WHERE device IN ({})"
	return template.format(','.join('%s' for _ in labels))


connection = pymysql.connect(host='localhost', user='test', password='password', db='tsdata', charset='utf8mb4',
														 cursorclass=pymysql.cursors.DictCursor)

try:
	devices = [str(uuid.uuid4()) for _ in range(1, 500)]
	create_identifiers(connection, devices)
	create_identifiers(connection, devices)
	create_identifiers(connection, devices)
	create_identifiers(connection, devices)

	now = datetime.datetime.utcnow()
	date = now.date()
	minute = now.minute

	identifiers = get_identifiers(connection, devices)

	measurements = [(i['id'], date, minute, 100) for i in identifiers]
	store(connection, measurements)

	for d in range(0, 10):
		for m in range(0, 1440):
			measurements = [(i['id'], date + datetime.timedelta(days=d), m, m - d) for i in identifiers]
			store(connection, measurements)

finally:
	connection.close()
