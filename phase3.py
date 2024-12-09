import mysql.connector
import random

def main():
	connection = mysql.connector.connect(
		host='127.0.0.1',
		user='user1',
		password='',
		database='phas3'
	)

	if not (connection.is_connected()):
		print('Not connected!')
		return

	print('Connected to database!')
	cursor = connection.cursor()

	while True:
		choice = int(input("*** OPTIONS ***\n1. Create Customer\n2. Create Reservation\n3. Return Vehicle\n4. EXIT\nWhat would you like to do? "))
		if choice == 1:
			create_customer(cursor, connection)
		elif choice == 2:
			create_reservation(cursor, connection)
		elif choice == 3:
			return_vehicle(cursor,  connection)
		elif choice == 4:
			break
		else:
			print("Invalid input!")
	

def create_customer(cursor, connection):
	print("*** CREATING A NEW CUSTOMER ***")
	cursor.execute("SELECT MAX(customer_id) FROM Customer")
	min_value = cursor.fetchone()[0]
	customer_id = min_value + 1

	license_num = input("Please input license num (max 10 characters): ")
	first_name = input("What is your first name: ")
	last_name = input("What is your last name: ")
	
	
	location_num = get_locations(cursor, connection)

	cursor.execute(
		"INSERT INTO Customer (customer_id, license_num, first_name, last_name, home_location) VALUES (%s, %s, %s, %s, %s) ",
		(customer_id, license_num, first_name, last_name, location_num)
	)
	connection.commit()

	# Confirm insertion 
	cursor.execute("SELECT * FROM Customer WHERE license_num = %s", (license_num,))
	customer = cursor. fetchone()
	if customer:
		print("Successfully inserted: ", customer, "into database")



def create_reservation(cursor, connection):
	cursor.execute("SELECT MAX(reservation_id) FROM Reservation")
	min_value = cursor.fetchone()[0]
	reservation_id = min_value + 1

	pickup_location = get_locations(cursor, connection)
	dropoff_location = get_locations(cursor, connection)

	vehicle_rented = select_vehicles(cursor, connection, pickup_location)

	customer_id = input("What is your customer ID")
	employee_id = input("Employee ID: ")

	# Get checkout
	year = input("Enter year (YYYY): ")
	month = input("Enter month (MM): ")
	day = input("Enter day (DD): ")

	# Format as SQL date string
	checkout = f"{year}-{month}-{day}"

	year = input("Enter year (YYYY): ")
	month = input("Enter month (MM): ")
	day = input("Enter day (DD): ")
	checkin = f"{year}-{month}-{day}"

	cursor.execute("SELECT * FROM Vehicle WHERE vehicle_id = %s", (vehicle_rented,))

	miles_begin = cursor.fetchone()[0]
	miles_end = 0
	miles_driven = 0

	cursor.execute(
    "INSERT INTO Reservation (reservation_id, pickup_location, dropoff_location, vehicle_rented, customer_id, employee_id, checkout, checkin, miles_begin, miles_end, miles_driven) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (reservation_id, pickup_location, dropoff_location, vehicle_rented, customer_id, employee_id, checkin, checkin, miles_begin, miles_end, miles_driven)
	)

	#Set vehicle to unavailable
	cursor.execute("UPDATE Vehicle SET available = FALSE WHERE vehicle_id = %s", (vehicle_rented,))

	connection.commit()

	cursor.execute("SELECT * FROM Reservation WHERE reservation_id = %s", (reservation_id,))
	res = cursor.fetchone()

	if res == None:
		print("error inserting")
	else:
		print("Successfully inserted ", res, " into the database. Please keep track of your details!")


def return_vehicle(cursor, connection):
	reservation_id = input("What is the reservation number: ")
	cursor.execute("SELECT * FROM Reservation WHERE reservation_id = %s", (reservation_id,))
	reservation = cursor.fetchone()
	
	if reservation == None:
		print("That reservation was not found! Please try again")

	print("Please select the dropoff location ")
	cur_loc = int(get_locations(cursor, connection))
	
	if cur_loc != reservation[2]:
		print("This is not the correct dropoff location! The vehicle is to be returned to: ", reservation[2])

	miles_driven = random.randint(10,1000)
	
	# Get current vehicle miles
	cursor.execute("SELECT mileage FROM Vehicle WHERE vehicle_id = %s", (reservation[3],))
	current_miles = cursor.fetchone()[0]
	updated_miles = current_miles + miles_driven


	cursor.execute("UPDATE Vehicle SET mileage = %s, available = TRUE, location = %s WHERE vehicle_id = %s", (updated_miles, cur_loc, reservation[3]))
	cursor.execute("UPDATE Reservation SET miles_end = %s, miles_driven = %s WHERE reservation_id = %s", (updated_miles, miles_driven, reservation_id))
	connection.commit()

	cursor.execute("SELECT * FROM Reservation WHERE reservation_id = %s", (reservation_id,))
	updated_res = cursor.fetchone()

	if updated_res == None:
		print("Something went very wrong!")
	else:
		print("Here are the initial details of your reservation: %s", reservation)
		print("Here are the fianl details of your reservation! Thanks!", updated_res)

	print()


# Helper Functions

def get_locations(cursor, connection):
	# Get location numbers to display 
	cursor.execute("SELECT location_id FROM Location")
	loc_nums = [loc[0] for loc in cursor.fetchall()]
	print("Here are the location numbers: ", loc_nums)
	location_num = input("Please select a location: ")

	return location_num 

def select_vehicles(cursor, connection, location_num):
	print("Here are the available vehicles from location", location_num)
	cursor.execute("SELECT * FROM Vehicle WHERE available = TRUE AND location = %s", (location_num,))
	available_vehicles = cursor.fetchall()
	print(available_vehicles)
	vehicle_picked = input("Seelct vehicle by vehilce id: ")
	
	cursor.execute("SELECT * FROM vehicle WHERE vehicle_id = %s", (vehicle_picked,))
	veh = cursor.fetchone()

	print("You have selected vehicle: ", (veh,))
	
	cursor.execute("UPDATE Vehicle SET available = FALSE WHERE vehicle_id = %s", (vehicle_picked,))
	
	connection.commit()

	return vehicle_picked


main()
