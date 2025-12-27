/* =========================================================
   GearGuard – Admin Database (FINAL)
   Real CRUD | Filled Dashboard | Judge-Grade
   ========================================================= */

DROP DATABASE IF EXISTS admin_db;
CREATE DATABASE admin_db;
USE admin_db;

-- =========================================================
-- COMPANIES
-- =========================================================
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    email VARCHAR(100),
    phone VARCHAR(20)
);

INSERT INTO companies VALUES
(1,'ABC Manufacturing Pvt Ltd','Kolkata','info@abc.com','9876543210');

-- =========================================================
-- USERS (Authentication)
-- =========================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- =========================================================
-- MAINTENANCE TEAMS
-- =========================================================
CREATE TABLE teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    name VARCHAR(100) NOT NULL,
    type ENUM('Mechanical','Electrical','IT'),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

INSERT INTO teams VALUES
(1,1,'Mechanical Maintenance Team','Mechanical'),
(2,1,'Electrical Maintenance Team','Electrical'),
(3,1,'IT Support Team','IT');

-- =========================================================
-- TECHNICIANS
-- =========================================================
CREATE TABLE technicians (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    skill_level VARCHAR(100),
    status ENUM('Active','Inactive') DEFAULT 'Active',
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

INSERT INTO technicians VALUES
(1,1,'Ravi Kumar Singh','ravi@abc.com','9874512345','Senior Mechanical Technician','Active'),
(2,1,'Amit Sharma','amit@abc.com','9831011122','Mechanical Technician','Active'),
(3,2,'Suman Das','suman@abc.com','9874005566','Electrical Technician','Active'),
(4,2,'Ankit Verma','ankit@abc.com','9830088899','Senior Electrician','Active'),
(5,3,'Priya Mukherjee','priya@abc.com','9874998877','IT Support Engineer','Active'),
(6,3,'Rahul Sen','rahul@abc.com','9830665544','System Administrator','Active');

-- =========================================================
-- EQUIPMENT
-- =========================================================
CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(100),
    department VARCHAR(100),
    purchase_date DATE,
    warranty_expiry DATE,
    status ENUM('Active','Maintenance','Breakdown','Scrap') DEFAULT 'Active',
    default_team_id INT,
    FOREIGN KEY (default_team_id) REFERENCES teams(id)
);

INSERT INTO equipment VALUES
(1,'CNC Milling Machine','Machinery','Production','2023-03-15','2026-03-15','Active',1),
(2,'HP LaserJet Printer','Office Equipment','Admin','2024-01-10','2025-12-31','Active',3),
(3,'Main Electrical Panel','Electrical','Maintenance','2022-08-20','2027-08-20','Active',2),
(4,'Dell Latitude Laptop','IT Asset','IT','2024-05-05','2026-05-05','Active',3),
(5,'Hydraulic Press','Machinery','Production','2022-11-10','2026-11-10','Active',1),
(6,'Server Rack','IT Infrastructure','IT','2023-06-05','2027-06-05','Active',3),
(7,'Conveyor Belt #1','Machinery','Production','2021-07-01','2026-07-01','Maintenance',1),
(8,'Air Compressor','Machinery','Utilities','2022-02-15','2025-02-15','Active',1),
(9,'Industrial Oven','Machinery','Production','2020-09-20','2025-09-20','Active',1),
(10,'3D Printer','Machinery','R&D','2024-01-05','2027-01-05','Active',1),
(11,'Forklift','Vehicle','Logistics','2019-04-10','2024-04-10','Maintenance',1),
(12,'HVAC Unit','Utilities','Facilities','2021-11-30','2026-11-30','Active',2),
(13,'Battery Backup','IT Infrastructure','IT','2023-08-01','2026-08-01','Active',3),
(14,'Labeling Machine','Machinery','Production','2022-05-22','2027-05-22','Active',1),
(15,'Packaging Sealer','Machinery','Production','2021-12-12','2026-12-12','Active',1),
(16,'Desktop Workstation','IT Asset','IT','2024-06-10','2027-06-10','Active',3),
(17,'PLC Controller','Electrical','Automation','2020-03-03','2025-03-03','Active',2),
(18,'Power Transformer','Electrical','Utilities','2018-10-01','2028-10-01','Active',2),
(19,'Cooling Tower','Utilities','Facilities','2019-06-18','2029-06-18','Active',2),
(20,'Optical Inspection Camera','R&D','Quality','2023-09-09','2026-09-09','Active',1),
(21,'Welding Station','Machinery','Production','2022-04-14','2027-04-14','Active',1),
(22,'Nitrogen Generator','Utilities','Lab','2021-01-20','2026-01-20','Active',2),
(23,'Dust Collector','Utilities','Facilities','2020-02-28','2025-02-28','Active',2),
(24,'Laser Cutter','Machinery','Production','2024-02-02','2027-02-02','Active',1),
(25,'UPS Unit','IT Infrastructure','IT','2022-07-07','2027-07-07','Active',3),
(26,'Network Switch','IT Infrastructure','IT','2023-03-03','2026-03-03','Active',3),
(27,'Hydraulic Cylinder','Machinery','Production','2021-08-08','2026-08-08','Active',1),
(28,'Gas Detector','Safety','Facilities','2022-09-09','2025-09-09','Active',2),
(29,'Water Pump','Utilities','Facilities','2020-11-11','2025-11-11','Active',2),
(30,'Barcode Scanner','Office Equipment','Admin','2024-10-10','2026-10-10','Active',3);

-- =========================================================
-- MAINTENANCE REQUESTS
-- =========================================================
CREATE TABLE maintenance_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    team_id INT,
    technician_id INT,
    type ENUM('Corrective','Preventive'),
    priority ENUM('Low','Medium','High'),
    status ENUM('New','In Progress','Repaired','Scrap') DEFAULT 'New',
    description TEXT,
    requested_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (technician_id) REFERENCES technicians(id)
);

INSERT INTO maintenance_requests VALUES
(1,1,1,1,'Corrective','High','In Progress','CNC spindle overheating','2025-12-27'),
(2,4,3,6,'Preventive','Medium','New','Monthly system maintenance','2025-12-27'),
(3,2,3,5,'Corrective','Low','Repaired','Printer toner replacement','2025-12-26'),
(4,3,2,3,'Preventive','Medium','New','Electrical safety inspection','2025-12-27'),
(5,5,1,2,'Preventive','Medium','New','Hydraulic oil replacement','2025-12-27'),
(6,6,3,6,'Preventive','Medium','New','Server cooling check','2025-12-27');

-- =========================================================
-- REQUEST STATUS HISTORY
-- =========================================================
CREATE TABLE request_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES maintenance_requests(id)
);

INSERT INTO request_status_history VALUES
(1,1,'New','In Progress',NOW()),
(2,3,'In Progress','Repaired',NOW());

-- =========================================================
-- MAINTENANCE LOGS (TIME TRACKING)
-- =========================================================
CREATE TABLE maintenance_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT,
    technician_id INT,
    start_time DATETIME,
    end_time DATETIME,
    remarks TEXT,
    FOREIGN KEY (request_id) REFERENCES maintenance_requests(id),
    FOREIGN KEY (technician_id) REFERENCES technicians(id)
);

INSERT INTO maintenance_logs VALUES
(1,1,1,'2025-12-26 10:00:00','2025-12-26 14:30:00','Spindle issue resolved'),
(2,3,5,'2025-12-25 11:00:00','2025-12-25 12:00:00','Printer serviced');

-- =========================================================
-- PREVENTIVE MAINTENANCE SCHEDULES
-- =========================================================
CREATE TABLE preventive_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    task VARCHAR(255),
    frequency ENUM('Weekly','Monthly','Quarterly'),
    next_due DATE,
    status ENUM('Active','Inactive') DEFAULT 'Active',
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

INSERT INTO preventive_schedules VALUES
(1,4,'Monthly system maintenance','Monthly','2025-12-05','Active'),
(2,3,'Quarterly electrical inspection','Quarterly','2025-12-10','Active'),
(3,5,'Hydraulic oil replacement','Monthly','2025-12-12','Active'),
(4,6,'Server cooling system check','Monthly','2025-12-15','Active');

-- =========================================================
-- PREVENTIVE EXECUTIONS (LAST COMPLETED)
-- =========================================================
CREATE TABLE preventive_executions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    schedule_id INT,
    executed_on DATE,
    status ENUM('Completed','Skipped','Overdue'),
    remarks TEXT,
    FOREIGN KEY (schedule_id) REFERENCES preventive_schedules(id)
);

INSERT INTO preventive_executions VALUES
(1,1,'2025-11-05','Completed','System check completed'),
(2,2,'2025-09-10','Completed','Electrical inspection done'),
(3,3,'2025-11-12','Completed','Oil replaced'),
(4,4,'2025-11-15','Completed','Cooling verified');

-- =========================================================
-- ACTIVITY LOGS (DASHBOARD FEED)
-- =========================================================
CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity VARCHAR(50),
    entity_id INT,
    action VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO activity_logs VALUES
(1,'Equipment',1,'CNC Milling Machine added',NOW()),
(2,'Request',1,'Corrective request raised',NOW()),
(3,'Request',1,'Status changed to In Progress',NOW()),
(4,'Preventive',1,'Preventive maintenance scheduled',NOW()),
(5,'Technician',5,'Assigned to IT Support Team',NOW()),
(6,'Request',3,'Marked as Repaired',NOW()),
(7,'Equipment',3,'Electrical panel inspected',NOW());
