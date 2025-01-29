db_data = {
    "master_device": """
        INSERT INTO master_device (id_device, production_lot, name, description, manufacturer) 
        VALUES 
            ('DBEM001', 1, 'DBEM001', '', 'DeepInsight'),
            ('DBEM002', 1, 'DBEM002', '', 'DeepInsight'),
            ('DBEM003', 1, 'DBEM003', '', 'DeepInsight'),
            ('DBEM004', 1, 'DBEM004', '', 'DeepInsight'),
            ('DBEM005', 1, 'DBEM005', '', 'DeepInsight'),
            ('DBEM006', 1, 'DBEM006', '', 'DeepInsight'),
            ('DBEM007', 1, 'DBEM007', '', 'DeepInsight'),
            ('DBEM008', 1, 'DBEM008', '', 'DeepInsight'),
            ('DBEM009', 2, 'DBEM009', '', 'DeepInsight'),
            ('DBEM010', 2, 'DBEM010', '', 'DeepInsight'),
            ('DBEM011', 2, 'DBEM011', '', 'DeepInsight'),
            ('DBEM012', 2, 'DBEM012', '', 'DeepInsight'),
            ('DBEM013', 2, 'DBEM013', '', 'DeepInsight'),
            ('DBEM014', 2, 'DBEM014', '', 'DeepInsight')
        ;
        """,

    "master_sensor": """
        INSERT INTO master_sensor (id_sensor, production_lot, name, description, manufacturer) 
        VALUES 
            ('sSMON', 1, 'Sensor internal Monitoring', 'Sensor for monitoring internal parameters of sensor including temperature, humidity, and battery voltage. Included in the beacons of lot 1.', 'DeepInsight'),
            ('sWEA' , 1, 'Weather Sensor', 'Weather sensor measuring temperature, humidity, pressure, and air quality indices. Included in the beacons of lot 1.', 'DeepInsight'),
            ('sAQU' , 1, 'Air Quality Sensor', 'Sensor measuring eCO2 and TVOC levels for air quality assessment. Included in the beacons of lot 1.', 'DeepInsight'),
            ('sACC' , 1, 'Acceleration Sensor', 'Sensor for measuring acceleration in multiple axes. Included in the beacons of lot 1.', 'DeepInsight'),
            ('sALM' , 1, 'Alarm Sensor', 'Sensor for detecting various alarm conditions. Included in the beacons of lot 1.', 'DeepInsight'),
            ('sSMON', 2, 'Sensor internal Monitoring', 'Sensor for monitoring internal parameters including battery voltage. Included in the beacons of lot 2.', 'DeepInsight'),
            ('sWEA' , 2, 'Weather Sensor 2', 'Measures temperature, humidity, and pressure, providing comprehensive weather data. Included in the beacons of lot 2.', 'DeepInsight'),
            ('sAQU' , 2, 'Air Quality Sensor 2', 'Monitors CO2 and TVOC levels, assessing air quality. Included in the beacons of lot 2.', 'DeepInsight'),
            ('sENV' , 2, 'Environment Sensor 2', 'Detects environmental changes like motion and light intensity, enhancing environmental awareness. Included in the beacons of lot 2.', 'DeepInsight'),
            ('sACC' , 2, 'Acceleration Sensor 2', 'Measures acceleration in multiple axes, capturing dynamic movements. Included in the beacons of lot 2.', 'DeepInsight')
        ;
        """,
    
    "master_variable": """
        INSERT INTO master_variable (id_variable, production_lot, name, description, unit, min_value, max_value, step_value) 
        VALUES
            ('00-temp-sSMON', 1, 'Monitorizaicón interna de temperatura', '', '°C', -40, 125, 0.01),
            ('01-hum-sSMON', 1, 'Monitorización interna de humedad', '', '%', 0, 100, 0.01),
            ('02-bat-sSMON', 1, 'Monitorización interna de batería', '', 'V', 0, 4.5, 0.01),
            ('03-pg-sSMON', 1, 'Monitorización interna de estado de carga', 'Booleano para indicar si se está cargando. Enchufada (1), desenchufada (0)', 'adim', 0, 1, 1),
            ('00-temp-sWEA', 1,  'Temperatura', '', '°C', -40, 85, 0.01),
            ('01-hum-sWEA', 1, 'Humedad', '', '%', 0, 100, 0.001),
            ('02-pres-sWEA', 1, 'Presión', '', 'hPa', 300, 1100, 0.0001),
            ('03-siaq-sWEA', 1, 'SIAQ', 'Sistema de Calidad del Aire Interior (System of Indoor Air Quality)', 'adim', 0, 500, 1),
            ('04-diaq-sWEA', 1, 'DIAQ', 'Diagnóstico de la Calidad del Aire Interior (Diagnostic Indoor Air Quality)', 'adim', 0, 500, 1),
            ('Q0-asiaq-sWEA', 1, 'Q0-aSIAQ', '', 'adim', 0, 5, 1),
            ('Q1-adiaq-sWEA', 1, 'Q1-aDIAQ', '', 'adim', 0, 5, 1),
            ('00-eco2-sAQU', 1, 'eCO2', 'Nivel de CO2 equivalente', 'ppm', 400, 60000, 1),
            ('01-tvoc-sAQU', 1, 'TVOC', 'Compuestos Orgánicos Volátiles Totales', 'ppb', 0, 60000, 1),
            ('Q0-calib-sAQU', 1, 'Calibración', '', 'adim', 0, 1, 2),
            ('00-accx-sACC', 1, 'Aceleración en eje X', '', 'G', -8, 8, 0.001),
            ('01-accy-sACC', 1, 'Aceleración en eje Y', '', 'G', -8, 8, 0.001),
            ('02-accz-sACC', 1, 'Aceleración en eje Z', '', 'G', -8, 8, 0.001),
            ('00-almtemp-sALM', 1, 'Temperatura de alarma', '', 'adim', 0, 1, 1),
            ('01-almbat-sALM', 1, 'Batería de alarma', '', 'adim', 0, 1, 1),
            ('02-almsiaq-sALM', 1, 'SIAQ de alarma', '', 'adim', 0, 1, 1),
            ('03-almeco2-sALM', 1, 'eCO2 de alarma', '', 'adim', 0, 1, 1),
            ('04-almtvoc-sALM', 1, 'TVOC de alarma', '', 'adim', 0, 1, 1),
            ('00-bat-sSMON', 2, 'Monitorizaicón interna de batería', '', 'V', 0, 4.5, 0.01),
            ('00-temp-sWEA', 2,  'Temperatura', '', '°C', -40, 85, 0.01),
            ('01-hum-sWEA', 2, 'Humedad', '', '%', 0, 100, 0.001),
            ('02-pres-sWEA', 2, 'Presión', '', 'hPa', 300, 1100, 0.0001),
            ('00-co2-sAQU', 2, 'CO2', 'Nivel de CO2', 'ppm', 400, 60000, 1),
            ('01-tvoc-sAQU', 2, 'TVOC', 'Compuestos Orgánicos Volátiles Totales', 'ppb', 0, 60000, 1),
            ('02-iaq-sAQU', 2, 'IAQ', 'Índice de Calidad del Aire', 'adim', 0, 500, 1),
            ('Q0-ciaq-sAQU', 2, 'Calibración de IAQ', '', 'adim', 0, 3, 1),
            ('00-pir-sENV', 2, 'PIR', 'Sensor de movimiento. Passive Infra Red', 'count', 0, 255, 1),
            ('01-lux-sENV', 2, 'Iluminancia', 'Sensor de luz', 'lux', 0, 1023, 1),
            ('00-accx-sACC', 2, 'Aceleración en eje X', '', 'G', -8, 8, 0.001),
            ('01-accy-sACC', 2, 'Aceleración en eje Y', '', 'G', -8, 8, 0.001),
            ('02-accz-sACC', 2, 'Aceleración en eje Z', '', 'G', -8, 8, 0.001)
        ;
        """,

    "master_location": """
        INSERT INTO master_location (name, description, latitude, longitude, country, city, site, building, room)
        VALUES
            ('Inactive', 'NULL', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
            ('Cátedra SmartE2', 'Laboratorio', 40.334897, -3.878369, 'Spain', 'Móstoles', 'Campus Móstoles URJC', 'Laboratorio III', 'S004'),
            ('Almacén PB9 (provisional) Estantería 1', 'Estantería frente a la puerta', 40.491238, -3.726446, 'Spain', 'Madrid', 'Parque de Bomberos N°9 (provisional)', 'Almacén', 'Almacén RBQ Est 1'),
            ('Almacén PB9 (provisional) Estantería 2', 'Estantería en la esquina opuesta a la puerta', 40.491281, -3.726457, 'Spain', 'Madrid', 'Parque de Bomberos N°9 (provisional)', 'Almacén', 'Almacén RBQ Est 2'),
            ('Cochera PB9 (provisional) TANQG', 'Cochera más próxima al almacén', 40.491231, -3.726529, 'Spain', 'Madrid', 'Parque de Bomberos N°9 (provisional)', 'Cochera', 'TANQG'),
            ('Despacho PB9 (provisional) Jefe Zona / Unidad RBQ', 'Armario Despacho Jefe Zona / Unidad RBQ', 40.490801, -3.726798, 'Spain', 'Madrid', 'Parque de Bomberos N°9 (provisional)', 'Despachos y Oficinas', 'Jefe Zona / Unidad RBQ')
        ;
        """,

    "device_sensor": """
        INSERT INTO device_sensor (id_device, id_sensor) 
                
        VALUES
                
            ('DBEM001', 'sSMON'),
            ('DBEM001', 'sWEA'),
            ('DBEM001', 'sAQU'),
            ('DBEM001', 'sACC'),
            ('DBEM001', 'sALM'),
                    
            ('DBEM002', 'sSMON'),
            ('DBEM002', 'sWEA'),
            ('DBEM002', 'sAQU'),
            ('DBEM002', 'sACC'),
            ('DBEM002', 'sALM'),
                    
            ('DBEM003', 'sSMON'),
            ('DBEM003', 'sWEA'),
            ('DBEM003', 'sAQU'),
            ('DBEM003', 'sACC'),
            ('DBEM003', 'sALM'),
                    
            ('DBEM004', 'sSMON'),
            ('DBEM004', 'sWEA'),
            ('DBEM004', 'sAQU'),
            ('DBEM004', 'sACC'),
            ('DBEM004', 'sALM'),
                    
            ('DBEM005', 'sSMON'),
            ('DBEM005', 'sWEA'),
            ('DBEM005', 'sAQU'),
            ('DBEM005', 'sACC'),
            ('DBEM005', 'sALM'),
                    
            ('DBEM006', 'sSMON'),
            ('DBEM006', 'sWEA'),
            ('DBEM006', 'sAQU'),
            ('DBEM006', 'sACC'),
            ('DBEM006', 'sALM'),
                    
            ('DBEM007', 'sSMON'),
            ('DBEM007', 'sWEA'),
            ('DBEM007', 'sAQU'),
            ('DBEM007', 'sACC'),
            ('DBEM007', 'sALM'),
                    
            ('DBEM008', 'sSMON'),
            ('DBEM008', 'sWEA'),
            ('DBEM008', 'sAQU'),
            ('DBEM008', 'sACC'),
            ('DBEM008', 'sALM'),
                    
            ('DBEM009', 'sSMON'),
            ('DBEM009', 'sWEA'),
            ('DBEM009', 'sAQU'),
            ('DBEM009', 'sENV'),
            ('DBEM009', 'sACC'),
                    
            ('DBEM010', 'sSMON'),
            ('DBEM010', 'sWEA'),
            ('DBEM010', 'sAQU'),
            ('DBEM010', 'sENV'),
            ('DBEM010', 'sACC'),

            ('DBEM011', 'sSMON'),
            ('DBEM011', 'sWEA'),
            ('DBEM011', 'sAQU'),
            ('DBEM011', 'sENV'),
            ('DBEM011', 'sACC'),

            ('DBEM012', 'sSMON'),
            ('DBEM012', 'sWEA'),
            ('DBEM012', 'sAQU'),
            ('DBEM012', 'sENV'),
            ('DBEM012', 'sACC'),

            ('DBEM013', 'sSMON'),
            ('DBEM013', 'sWEA'),
            ('DBEM013', 'sAQU'),
            ('DBEM013', 'sENV'),
            ('DBEM013', 'sACC'),

            ('DBEM014', 'sSMON'),
            ('DBEM014', 'sWEA'),
            ('DBEM014', 'sAQU'),
            ('DBEM014', 'sENV'),
            ('DBEM014', 'sACC')
        ;
        
        """,

    "sensor_variable": """
        INSERT INTO sensor_variable (id_sensor, id_variable) 
        VALUES 
            ('sSMON', '00-temp-sSMON'),
            ('sSMON', '01-hum-sSMON'),
            ('sSMON', '02-bat-sSMON'),
            ('sSMON', '03-pg-sSMON'),
            ('sSMON', '00-bat-sSMON'), 

            ('sWEA', '00-temp-sWEA'),
            ('sWEA', '01-hum-sWEA'),
            ('sWEA', '02-pres-sWEA'),
            ('sWEA', '03-siaq-sWEA'),
            ('sWEA', '04-diaq-sWEA'),
            ('sWEA', 'Q0-asiaq-sWEA'),
            ('sWEA', 'Q1-adiaq-sWEA'),

            ('sAQU', '00-eco2-sAQU'),
            ('sAQU', '01-tvoc-sAQU'),
            ('sAQU', 'Q0-calib-sAQU'),
            ('sAQU', '00-co2-sAQU'),   
            ('sAQU', '02-iaq-sAQU'),   
            ('sAQU', 'Q0-ciaq-sAQU'),  

            ('sENV', '00-pir-sENV'),
            ('sENV', '01-lux-sENV'),

            ('sACC', '00-accx-sACC'),
            ('sACC', '01-accy-sACC'),
            ('sACC', '02-accz-sACC'),

            ('sALM', '00-almtemp-sALM'),
            ('sALM', '01-almbat-sALM'),
            ('sALM', '02-almsiaq-sALM'),
            ('sALM', '03-almeco2-sALM'),
            ('sALM', '04-almtvoc-sALM')
        ;
        """,

    "location_device_tracking" : """
        INSERT INTO location_device_tracking (id_location, id_device_current, last_modified_id_device_current) 
        VALUES 
            (1, 'DBEM001', '2024-02-05 11:00:00'),
            (2, 'DBEM002', '2024-02-05 11:00:00'),
            (1, 'DBEM003', '2024-02-05 11:00:00'),
            (1, 'DBEM004', '2024-02-05 11:00:00'),
            (1, 'DBEM005', '2024-02-05 11:00:00'),
            (1, 'DBEM006', '2024-02-05 11:00:00'),
            (6, 'DBEM007', '2024-02-05 11:00:00'),
            (1, 'DBEM008', '2024-02-05 11:00:00'),
            (2, 'DBEM009', '2024-02-05 11:00:00'),
            (2, 'DBEM010', '2024-02-05 11:00:00'),
            (3, 'DBEM011', '2024-02-05 11:00:00'),
            (4, 'DBEM012', '2024-02-05 11:00:00'),
            (5, 'DBEM013', '2024-02-05 11:00:00'),
            (6, 'DBEM014', '2024-02-05 11:00:00')
        ;
        """,

    "historical_location" : """
        INSERT INTO historical_location (id_location, id_device, timestamp) 
        VALUES 
            (1, 'DBEM001', '2024-02-05 11:00:00'),
            (2, 'DBEM002', '2024-02-05 11:00:00'),
            (1, 'DBEM003', '2024-02-05 11:00:00'),
            (1, 'DBEM004', '2024-02-05 11:00:00'),
            (1, 'DBEM005', '2024-02-05 11:00:00'),
            (1, 'DBEM006', '2024-02-05 11:00:00'),
            (6, 'DBEM007', '2024-02-05 11:00:00'),
            (1, 'DBEM008', '2024-02-05 11:00:00'),
            (2, 'DBEM009', '2024-02-05 11:00:00'),
            (2, 'DBEM010', '2024-02-05 11:00:00'),
            (3, 'DBEM011', '2024-02-05 11:00:00'),
            (4, 'DBEM012', '2024-02-05 11:00:00'),
            (5, 'DBEM013', '2024-02-05 11:00:00'),
            (6, 'DBEM014', '2024-02-05 11:00:00')
        ;
        """,

    "data_last_load": """ 
        INSERT INTO data_last_load (id_device, id_sensor, id_variable, timestamp_last_load) 
        VALUES 

            ('DBEM001', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM001', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM001', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM001', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM001', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM001', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM001', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM001', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM001', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM001', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM001', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM001', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM001', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM001', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM001', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM002', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM002', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM002', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM002', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM002', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM002', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM002', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM002', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM002', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM002', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM002', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM002', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM002', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM002', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM002', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM003', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM003', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM003', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM003', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM003', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM003', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM003', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM003', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM003', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM003', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM003', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM003', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM003', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM003', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM003', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM004', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM004', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM004', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM004', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM004', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM004', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM004', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM004', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM004', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM004', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM004', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM004', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM004', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM004', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM004', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM005', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM005', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM005', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM005', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM005', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM005', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM005', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM005', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM005', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM005', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM005', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM005', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM005', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM005', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM005', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM006', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM006', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM006', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM006', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM006', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM006', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM006', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM006', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM006', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM006', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM006', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM006', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM006', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM006', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM006', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),
            
            ('DBEM007', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM007', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM007', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM007', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM007', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM007', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM007', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM007', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM007', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM007', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM007', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM007', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM007', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM007', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM007', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM008', 'sSMON', '00-temp-sSMON', '2024-02-01 00:00'),
            ('DBEM008', 'sSMON', '01-hum-sSMON', '2024-02-01 00:00'),
            ('DBEM008', 'sSMON', '02-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM008', 'sSMON', '03-pg-sSMON', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', '03-siaq-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', '04-diaq-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', 'Q0-asiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sWEA', 'Q1-adiaq-sWEA', '2024-02-01 00:00'),
            ('DBEM008', 'sAQU', '00-eco2-sAQU', '2024-02-01 00:00'),
            ('DBEM008', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM008', 'sAQU', 'Q0-calib-sAQU', '2024-02-01 00:00'),
            ('DBEM008', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM008', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM008', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            ('DBEM008', 'sALM', '00-almtemp-sALM', '2024-02-01 00:00'),
            ('DBEM008', 'sALM', '01-almbat-sALM', '2024-02-01 00:00'),
            ('DBEM008', 'sALM', '02-almsiaq-sALM', '2024-02-01 00:00'),
            ('DBEM008', 'sALM', '03-almeco2-sALM', '2024-02-01 00:00'),
            ('DBEM008', 'sALM', '04-almtvoc-sALM', '2024-02-01 00:00'),

            ('DBEM009', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM009', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM009', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM009', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM009', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM009', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM009', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM009', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM009', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM009', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM009', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM009', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM009', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),

            ('DBEM010', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM010', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM010', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM010', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM010', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM010', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM010', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM010', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM010', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM010', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM010', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM010', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM010', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),

            ('DBEM011', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM011', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM011', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM011', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM011', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM011', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM011', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM011', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM011', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM011', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM011', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM011', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM011', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),
            
            ('DBEM012', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM012', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM012', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM012', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM012', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM012', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM012', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM012', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM012', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM012', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM012', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM012', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM012', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),

            ('DBEM013', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM013', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM013', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM013', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM013', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM013', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM013', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM013', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM013', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM013', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM013', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM013', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM013', 'sACC', '02-accz-sACC', '2024-02-01 00:00'),

            ('DBEM014', 'sSMON', '00-bat-sSMON', '2024-02-01 00:00'),
            ('DBEM014', 'sWEA', '00-temp-sWEA', '2024-02-01 00:00'),
            ('DBEM014', 'sWEA', '01-hum-sWEA', '2024-02-01 00:00'),
            ('DBEM014', 'sWEA', '02-pres-sWEA', '2024-02-01 00:00'),
            ('DBEM014', 'sAQU', '00-co2-sAQU', '2024-02-01 00:00'),
            ('DBEM014', 'sAQU', '01-tvoc-sAQU', '2024-02-01 00:00'),
            ('DBEM014', 'sAQU', '02-iaq-sAQU', '2024-02-01 00:00'),
            ('DBEM014', 'sAQU', 'Q0-ciaq-sAQU', '2024-02-01 00:00'),
            ('DBEM014', 'sENV', '00-pir-sENV', '2024-02-01 00:00'),
            ('DBEM014', 'sENV', '01-lux-sENV', '2024-02-01 00:00'),
            ('DBEM014', 'sACC', '00-accx-sACC', '2024-02-01 00:00'),
            ('DBEM014', 'sACC', '01-accy-sACC', '2024-02-01 00:00'),
            ('DBEM014', 'sACC', '02-accz-sACC', '2024-02-01 00:00')
        ;
        """,

    "data" : "",

    "trigger_after_insert_id_device_current" : """
        CREATE TRIGGER after_insert_id_device_current
        AFTER INSERT ON location_device_tracking
        FOR EACH ROW
        BEGIN
            DECLARE last_modified_timestamp TIMESTAMP;
            
            SET last_modified_timestamp = NOW();

            INSERT INTO historical_location (id_location, id_device, timestamp)
            VALUES (NEW.id_location, NEW.id_device_current, last_modified_timestamp);
        END 
        """,

    "trigger_after_update_id_device_current":"""
        CREATE TRIGGER after_update_id_device_current
        AFTER UPDATE ON location_device_tracking
        FOR EACH ROW
        BEGIN
            DECLARE last_modified_timestamp TIMESTAMP;
            IF OLD.id_location <> NEW.id_location OR OLD.id_device_current <> NEW.id_device_current THEN
                SET last_modified_timestamp = NOW();

                INSERT INTO historical_location (id_location, id_device, timestamp)
                VALUES (NEW.id_location, NEW.id_device_current, last_modified_timestamp);
            END IF;
        END;
        """

}