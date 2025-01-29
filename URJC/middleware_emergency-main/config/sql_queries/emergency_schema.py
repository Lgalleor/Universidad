db_schema = {

    "master_device": """
        CREATE TABLE IF NOT EXISTS master_device
            (
                id_device VARCHAR(255) PRIMARY KEY, 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                manufacturer VARCHAR(255) 
            )
        ;
        """,

    "master_sensor": """
        CREATE TABLE IF NOT EXISTS master_sensor
            (
                id_sensor VARCHAR(255), 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                manufacturer VARCHAR(255), 
                PRIMARY KEY (id_sensor, production_lot)
            )
        ;
        """,

    "master_variable": """
        CREATE TABLE IF NOT EXISTS master_variable
            (
                id_variable VARCHAR(255), 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                unit VARCHAR(255), 
                min_value FLOAT, 
                max_value FLOAT, 
                step_value FLOAT, 
                PRIMARY KEY (id_sensor, production_lot) 
            )
        ;
        """,

    "master_device": """
        CREATE TABLE IF NOT EXISTS master_device
            (
                id_device VARCHAR(255) PRIMARY KEY, 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                manufacturer VARCHAR(255) 
            )
        ;
         """,

    "master_sensor": """
        CREATE TABLE IF NOT EXISTS master_sensor
            (
                id_sensor VARCHAR(255), 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                manufacturer VARCHAR(255), 
                PRIMARY KEY (id_sensor, production_lot)
            )
        ;
        """,

    "master_variable": """
        CREATE TABLE IF NOT EXISTS master_variable
            (
                id_variable VARCHAR(255), 
                production_lot INT NOT NULL, 
                name VARCHAR(255), 
                description TEXT, 
                unit VARCHAR(255), 
                min_value FLOAT, 
                max_value FLOAT, 
                step_value FLOAT, 
                PRIMARY KEY (id_variable, production_lot) 
            )
        ;
        """,

    "master_location": """
        CREATE TABLE IF NOT EXISTS master_location
            (
                id_location INT AUTO_INCREMENT PRIMARY KEY, 
                name VARCHAR(255), 
                description TEXT, 
                latitude DECIMAL(11,7), 
                longitude DECIMAL(11,7), 
                country VARCHAR(255), 
                city VARCHAR(255), 
                site VARCHAR(255), 
                building VARCHAR(255), 
                room VARCHAR(255)
            )
        ;
        """,

    "device_sensor": """
        CREATE TABLE IF NOT EXISTS device_sensor
            (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                id_device VARCHAR(255), 
                id_sensor VARCHAR(255), 
                FOREIGN KEY (id_device) REFERENCES master_device(id_device), 
                FOREIGN KEY (id_sensor) REFERENCES master_sensor(id_sensor)
            )
        ;
        """,

    "sensor_variable": """
        CREATE TABLE IF NOT EXISTS sensor_variable
            (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                id_sensor VARCHAR(255), 
                id_variable VARCHAR(255), 
                FOREIGN KEY (id_sensor) REFERENCES master_sensor(id_sensor), 
                FOREIGN KEY (id_variable) REFERENCES master_variable(id_variable)
            )
        ;
        """,

    "location_device_tracking": """
        CREATE TABLE IF NOT EXISTS location_device_tracking
            (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                id_location INT NOT NULL, 
                id_device_current VARCHAR(255) NOT NULL, 
                last_modified_id_device_current TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                FOREIGN KEY (id_location) REFERENCES master_location(id_location), 
                FOREIGN KEY (id_device_current) REFERENCES master_device(id_device)
            )
        ;
        """,

    "historical_location": """
        CREATE TABLE IF NOT EXISTS historical_location
            (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                timestamp DATETIME NOT NULL, 
                id_device VARCHAR(255), 
                id_location INT
            )
        ;
         """,

    "data": """
        CREATE TABLE IF NOT EXISTS data 
            (
                id_data INT AUTO_INCREMENT, 
                timestamp DATETIME NOT NULL, 
                value FLOAT NOT NULL, 
                id_device VARCHAR(255) NOT NULL, 
                id_sensor VARCHAR(255) NOT NULL, 
                id_variable VARCHAR(255) NOT NULL, 
                id_location INT, 
                PRIMARY KEY (id_data, timestamp)
            )
        ;
        """,

    "data_last_load": """
        CREATE TABLE IF NOT EXISTS `data_last_load`
            (
                `id_sensor` VARCHAR(255) NOT NULL, 
                `id_variable`VARCHAR(255) NOT NULL, 
                `id_device` VARCHAR(255) NOT NULL, 
                `timestamp_last_load` datetime NOT NULL
            )
        ;
        """,

    "deployment":"""
        CREATE TABLE deployment (
        id_deployment INT AUTO_INCREMENT PRIMARY KEY,
        start_date TIMESTAMP NOT NULL,
        end_date TIMESTAMP NULL,
        id_location INT NOT NULL,
        comments TEXT,
        FOREIGN KEY (id_location) REFERENCES master_location(id_location)
        );
        """,

    "partitions": """ 
        ALTER TABLE data
        PARTITION BY RANGE (TO_DAYS(timestamp)) (
            PARTITION pmin VALUES LESS THAN (TO_DAYS('2020-01-01')),
            PARTITION p202301 VALUES LESS THAN (TO_DAYS('2023-02-01')),
            PARTITION p202302 VALUES LESS THAN (TO_DAYS('2023-03-01')),
            PARTITION p202303 VALUES LESS THAN (TO_DAYS('2023-04-01')),
            PARTITION p202304 VALUES LESS THAN (TO_DAYS('2023-05-01')),
            PARTITION p202305 VALUES LESS THAN (TO_DAYS('2023-06-01')),
            PARTITION p202306 VALUES LESS THAN (TO_DAYS('2023-07-01')),
            PARTITION p202307 VALUES LESS THAN (TO_DAYS('2023-08-01')),
            PARTITION p202308 VALUES LESS THAN (TO_DAYS('2023-09-01')),
            PARTITION p202309 VALUES LESS THAN (TO_DAYS('2023-10-01')),
            PARTITION p202310 VALUES LESS THAN (TO_DAYS('2023-11-01')),
            PARTITION p202311 VALUES LESS THAN (TO_DAYS('2023-12-01')),
            PARTITION p202312 VALUES LESS THAN (TO_DAYS('2024-01-01')),
            PARTITION p202401 VALUES LESS THAN (TO_DAYS('2024-02-01')),
            PARTITION p202402 VALUES LESS THAN (TO_DAYS('2024-03-01')),
            PARTITION p202403 VALUES LESS THAN (TO_DAYS('2024-04-01')),
            PARTITION p202404 VALUES LESS THAN (TO_DAYS('2024-05-01')),
            PARTITION p202405 VALUES LESS THAN (TO_DAYS('2024-06-01')),
            PARTITION p202406 VALUES LESS THAN (TO_DAYS('2024-07-01')),
            PARTITION p202407 VALUES LESS THAN (TO_DAYS('2024-08-01')),
            PARTITION p202408 VALUES LESS THAN (TO_DAYS('2024-09-01')),
            PARTITION p202409 VALUES LESS THAN (TO_DAYS('2024-10-01')),
            PARTITION p202410 VALUES LESS THAN (TO_DAYS('2024-11-01')),
            PARTITION p202411 VALUES LESS THAN (TO_DAYS('2024-12-01')),
            PARTITION p202412 VALUES LESS THAN (TO_DAYS('2025-01-01')),
            PARTITION pmax VALUES LESS THAN MAXVALUE
        );
        """,

    "data_idx_id_device": "CREATE INDEX idx_id_device ON data (id_device);",

    "data_idx_id_sensor": "CREATE INDEX idx_id_sensor ON data (id_sensor);",

    "data_idx_id_variable": "CREATE INDEX idx_id_variable ON data (id_variable);",

    "data_idx_device_sensor": "CREATE INDEX idx_device_sensor ON data (id_device, id_sensor);"
}