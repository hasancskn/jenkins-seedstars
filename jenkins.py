#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import jenkins, time, sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
server = jenkins.Jenkins('http://localhost:8080', username='admin', password='9c089abe67244ac4b63d45e332fb773b')
jobs = server.get_jobs()
c.execute('''CREATE TABLE IF NOT EXISTS jobs (job_id integer primary key, job_name text, job_check_time datetime)''')
for job in jobs:
	print(job["fullname"])
	try:
		build_number = server.get_job_info(job["name"])["lastCompletedBuild"]["number"]
		build_info = server.get_build_info(job["name"], build_number)
		if build_info["result"] == "SUCCESS":
			print("\t" + time.strftime('%H:%M:%S %m-%d-%Y', time.localtime(build_info["timestamp"]/1000)))
			c.execute('''INSERT INTO jobs(job_name, job_check_time) SELECT ?,? WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE job_name = ?)''', (job["fullname"], build_info["timestamp"]/1000, job["fullname"]))
			conn.commit()
	except Exception as e:
		print("\t" + job["fullname"] + " has no last build")
conn.close()