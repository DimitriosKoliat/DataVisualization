import mysql.connector

mydb = mysql.connector.connect(host="127.0.0.1", user="root",password="password",allow_local_infile=True)

mycursor = mydb.cursor()

tables = ["years", "countries", "measures"]


def dropDB():
    query = """
        DROP DATABASE projectDB
    """
    mycursor.execute(query)
    print("Database projectDB droped")


def createDB():
    query = """
        CREATE DATABASE projectDB
    """
    mycursor.execute(query)
    print("Database projectDB created")
    mycursor.execute("USE projectDB")


def createTables():
    queryC = """
        CREATE TABLE IF NOT EXISTS projectDB.Countries (
        C_ID INT NOT NULL AUTO_INCREMENT,
        C_Name VARCHAR(45) NOT NULL,
        PRIMARY KEY (C_ID),
        UNIQUE INDEX C_Name_UNIQUE (C_Name ASC) )
        ENGINE = InnoDB
    """
    queryY = """
        CREATE TABLE IF NOT EXISTS projectDB.Years (
        Y_ID INT NOT NULL AUTO_INCREMENT,
        Year_Descr VARCHAR(4) NOT NULL,
        PRIMARY KEY (Y_ID),
        UNIQUE INDEX Year_Descr_UNIQUE (Year_Descr ASC) )
        ENGINE = InnoDB
    """
    queryM = """
        CREATE TABLE IF NOT EXISTS projectDB.Measures (
        Countries_C_ID INT NOT NULL,
        Years_Y_ID INT NOT NULL,
        Female_industry_workers_percent_of_female_employment DECIMAL(7,5) NULL,
        Female_long_term_unemployment_rate_percent DECIMAL(7,5) NULL,
        Female_service_workers_percent_of_female_employment DECIMAL(7,5) NULL,
        Happiness_score DECIMAL(7,5) NULL,
        Human_development_index DECIMAL(7,5) NULL,
        Indastry_percent_of_gdb DECIMAL(7,5) NULL,
        Industry_workers_percent_of_employment DECIMAL(7,5) NULL,
        Long_term_unemployment_rate_percent DECIMAL(7,5) NULL,
        Male_industry_workers_percent_of_male_employment DECIMAL(7,5) NULL,
        Male_long_term_unemployment DECIMAL(7,5) NULL,
        Male_service_workers_percent_of_male_employment DECIMAL(7,5) NULL,
        Manuf_employ DECIMAL(7,5) NULL,
        Services_percent_of_gdp DECIMAL(7,5) NULL,
        Service_workers_percent_of_umployment DECIMAL(7,5) NULL,
        Measure_ID INT NULL,
        INDEX fk_Happiness_Countries_idx (Countries_C_ID ASC) ,
        INDEX fk_Happiness_Years1_idx (Years_Y_ID ASC) ,
        PRIMARY KEY (Countries_C_ID, Years_Y_ID),
        CONSTRAINT fk_Happiness_Countries
        FOREIGN KEY (Countries_C_ID)
        REFERENCES projectDB.Countries (C_ID)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
        CONSTRAINT fk_Happiness_Years1
        FOREIGN KEY (Years_Y_ID)
        REFERENCES projectDB.Years (Y_ID)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
        ENGINE = InnoDB
    """
    mycursor.execute(queryC)
    print("Create Countries table")
    mycursor.execute(queryY)
    print("Create years table")
    mycursor.execute(queryM)
    print("Create measures table")


def mainCDB():
    dropDB()
    createDB()
    createTables()