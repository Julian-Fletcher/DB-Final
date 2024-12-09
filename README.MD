# Databases Phase 3 
## Setup
### Required Libraries
- mysql.connector -> `pip install mysql.connector`

### Running
To start, you'll want to create a new connection in MYSQL Workbench. Use `p3.sql` to populate with the necessecary information. In `phase3.py` you'll need to modify the following lines:

```python
	connection = mysql.connector.connect(
		host='127.0.0.1',
		user='user1',
		password='',
		database='phas3'
	)
```

with the necessecary information to connect to your MYSQL installation (changing the host, the user, possibly password if you have one set up.)

From there, you can run `python phase3.py` in your preferred terminal and go through the prompts! 

### Important things:
- There are 6 employees with IDs 1-6
- You will need to remember your reservation ID and return locations for return vehicle!