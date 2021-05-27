import mysql.connector

mydb = mysql.connector.connect(host="127.0.0.1", user="root",password="password",allow_local_infile=True)

mycursor = mydb.cursor()


tables = ["years", "countries", "measures"]


def loadTableCounties(countries):
    print("Add data into countries table")
    queryLC = """
        INSERT INTO projectDB.COUNTRIES (C_ID,C_NAME) VALUES (%s, %s)
    """
    for c in countries:
        valuesLC = (countries.index(c)+1, c)
        mycursor.execute(queryLC, valuesLC)
    mydb.commit()


def loadTableYears(years):
    print("Add data into years table")
    queryLY = """
       INSERT INTO projectDB.years( Y_ID, Year_Descr) values (%s,%s)
    """
    for y in years:
        valuesLY = (years.index(y)+1, y)
        mycursor.execute(queryLY, valuesLY)
    mydb.commit()


def printTable(select):
    if(tables[select] == "years"):
        queryPT = """
            SELECT * FROM years
        """
        print("Print Years table")
    elif(tables[select] == "countries"):
        queryPT = """
            SELECT * FROM countries
        """
        print("Print Countries table")
    elif(tables[select] == "measures"):
        queryPT = """
            SELECT * FROM measures
        """
        print("Print Measures table")
    mycursor.execute(queryPT)
    results = mycursor.fetchall()
    for row in results:
        print(row)



def loadDataFromFinalFile():
    mycursor.execute("USE projectDB")
    mycursor.execute("set global local_infile=true;")
    print("Add data into measures table")
    queryLD = """
    LOAD DATA LOCAL INFILE "final.csv"
    INTO TABLE measures
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS
    (@a, @b, @c, @d ,@e ,@f ,@g ,@h ,@i ,@j ,@k ,@l ,@m ,@n ,@o ,@p ,@q)
       SET Countries_C_ID = IF(@a = '', NULL, @a),
           Years_Y_ID = IF(@b = '', NULL, @b),
           Female_industry_workers_percent_of_female_employment = IF(@c = '', NULL, @c),
           Female_long_term_unemployment_rate_percent = IF(@d = '', NULL, @d),
           Female_service_workers_percent_of_female_employment = IF(@e = '', NULL, @e),
           Happiness_score = IF(@f = '', NULL, @f),
           Human_development_index = IF(@g = '', NULL, @g),
           Indastry_percent_of_gdb = IF(@h = '', NULL, @h),
           Industry_workers_percent_of_employment = IF(@i = '', NULL, @i),
           Long_term_unemployment_rate_percent = IF(@j = '', NULL, @j),
           Male_industry_workers_percent_of_male_employment = IF(@k = '', NULL, @k),
           Male_long_term_unemployment = IF(@l = '', NULL, @l),
           Male_service_workers_percent_of_male_employment = IF(@m = '', NULL, @m),
           Manuf_employ = IF(@n = '', NULL, @n),
           Services_percent_of_gdp = IF(@o = '', NULL, @o),
           Service_workers_percent_of_umployment = IF(@p = '', NULL, @p),
           Measure_ID = IF(@1 = '', NULL, @q);
    """
    mycursor.execute(queryLD)
    mydb.commit()

def mainLD(c,y):
    loadTableCounties(c)
    loadTableYears(y)
    #printTable(s)
    loadDataFromFinalFile()