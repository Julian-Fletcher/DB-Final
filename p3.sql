create database phas3;
use phas3;

create table Location(
	location_id int primary key,
    city varchar(60) not null,
    zip varchar(5) not null,
    address varchar(120) not null,
    manager int
);

create table Vehicle(
	vehicle_id int primary key,
    vehicle_type int not null,
    license_plate varchar(6) not null unique,
    available boolean not null default TRUE,
    mileage int not null check (mileage >= 0),
    location int not null,
    foreign key (location) references Location(location_id)
    on delete cascade
);

create table Employee(
	employee_id int primary key,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    email varchar(30) unique,
    phone varchar(10),
    location_id int
);



alter table Location
add constraint fk_location_manager
foreign key (manager) references Employee(employee_id)
on delete set null;

create table Customer(
	customer_id int primary key,
    license_num varchar(10) not null unique,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    home_location int not null
);

create table Driver(
	license_num varchar(10) primary key,
    customer_id int not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    foreign key (customer_id) references Customer(customer_id)
    on delete cascade
);

create table Reservation(
	reservation_id int primary key,
    pickup_location int not null,
    dropoff_location int not null,
    vehicle_rented int not null,
    customer_id int not null,
    employee_id int not null,
    checkout datetime not null,
	checkin datetime not null,
    miles_begin int not null,
    miles_end int not null,
    miles_driven int not null,
    
    foreign key (pickup_location) references Location(location_id)
		on delete restrict,
    foreign key (dropoff_location) references Location(location_id)
		on delete restrict,    
    foreign key (vehicle_rented) references Vehicle(vehicle_id)
		on delete restrict,
    foreign key (customer_id) references Customer(customer_id)
		on delete restrict,
    foreign key (employee_id) references Employee(employee_id)
		on delete restrict
);

-- Insertions --

-- Employees
INSERT INTO Employee (employee_id, first_name, last_name, email, phone, location_id) 
VALUES 
(1, 'John', 'Doe', 'jdoe@company.com', '1234567890', 1),
(2, 'Jane', 'Smith', 'jsmith@company.com', '0987654321', 2),
(3, 'Mark', 'Johnson', 'mjohnson@company.com', '1122334455', 3),
(4, 'Emily', 'Davis', 'edavis@company.com', '2233445566', 4),
(5, 'Michael', 'Brown', 'mbrown@company.com', '3344556677', 1),
(6, 'Sophia', 'Wilson', 'swilson@company.com', '4455667788', 2);

-- Insert locations
INSERT INTO Location (location_id, city, zip, address, manager) 
VALUES 
(1, 'New York', '10001', '123 Main St', 1),
(2, 'Los Angeles', '90001', '456 Elm St', 2),
(3, 'Chicago', '60601', '789 Oak St', 3),
(4, 'San Francisco', '94101', '101 Pine St', 4);

-- Insert customers
INSERT INTO Customer (customer_id, license_num, first_name, last_name, home_location) 
VALUES 
(1, 'C12345', 'Alice', 'Johnson', 1),
(2, 'C67890', 'Bob', 'Williams', 2),
(3, 'C11223', 'Charlie', 'Brown', 3),
(4, 'C44556', 'David', 'Jones', 4),
(5, 'C77889', 'Eve', 'Taylor', 1),
(6, 'C99000', 'Frank', 'Miller', 2);


-- Insert drivers (2 linked to one customer, 1 to another)
INSERT INTO Driver (license_num, customer_id, first_name, last_name) 
VALUES 
('C12345', 1, 'Alice', 'Johnson'),   -- Driver 1 linked to Customer 1
('C67890', 1, 'Bob', 'Williams'),    -- Driver 2 linked to Customer 1
('C11223', 3, 'Charlie', 'Brown');   -- Driver 3 linked to Customer 3

-- Insert vehicles
INSERT INTO Vehicle (vehicle_id, vehicle_type, license_plate, available, mileage, location) 
VALUES 
(1, 1, 'NY1234', TRUE, 5000, 1), 
(2, 1, 'LA5678', FALSE, 15000, 1), 
(3, 2, 'SF1357', TRUE, 2200, 2), 
(4, 2, 'CH1239', TRUE, 500, 2), 
(5, 1, 'NY2345', FALSE, 9000, 2), 
(6, 2, 'LA6789', TRUE, 8000, 2), 
(7, 1, 'SF2468', TRUE, 12000, 2), 
(8, 1, 'CH2469', TRUE, 500, 3), 
(9, 2, 'NY3456', TRUE, 2000, 3), 
(10, 1, 'LA7890', FALSE, 15000, 3), 
(11, 2, 'SF3579', TRUE, 100, 3), 
(12, 1, 'CH3579', TRUE, 3000, 3), 
(13, 2, 'NY4567', TRUE, 14000, 2), 
(14, 1, 'LA8901', TRUE, 6000, 2), 
(15, 2, 'SF4680', FALSE, 18000, 2);

-- Insert reservations
INSERT INTO Reservation (reservation_id, pickup_location, dropoff_location, vehicle_rented, customer_id, employee_id, checkout, checkin, miles_begin, miles_end, miles_driven) 
VALUES 
(1, 1, 2, 1, 1, 1, '2024-11-01 08:00:00', '2024-11-01 12:00:00', 5000, 5100, 100),
(2, 2, 3, 2, 2, 2, '2024-11-02 09:00:00', '2024-11-02 17:00:00', 15000, 15200, 200),
(3, 3, 4, 3, 3, 3, '2024-11-03 10:00:00', '2024-11-03 15:00:00', 2200, 0, 0);


