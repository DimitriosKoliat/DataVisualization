from flask import Flask,render_template,request,jsonify,redirect,url_for,json
from flask_mysqldb import MySQL,MySQLdb 
import numpy as np

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'projectDB'

mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('homePage.html' )

@app.route('/DiagramBuilder')
def countries():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM countries ORDER BY C_Name")
    countries = cur.fetchall()
    cur.execute("SELECT * FROM years ORDER BY Year_Descr")
    years = cur.fetchall()
    return render_template('diagramBuilder.html',countries=countries,years=years)

@app.route('/diagram', methods=['GET', 'POST'])
def getSelectedCountries():
    if request.method == 'POST':
        countries = request.form.getlist('C_Name')
        year1 = request.form['Year_Descr']
        year2 = request.form['Year_Descr2']
        measureId = request.form.getlist('measure')
        measureType = []
        for id in measureId:
            measureType.append(idToSelection(id))
        diagramId = request.form['diagram']
        timePeriodId = request.form['time_period']
        finalList = prepareDataForCharts(countries,year1,year2,measureType,diagramId)
        TPC = timePeriodChanges(finalList,timePeriodId)
        data = findTextFromID(TPC,measureType,diagramId)
        measureName = titleFixer(measureType)
        data = json.dumps(data)
        measureName = json.dumps(measureName)
        return diagram(data,measureName,diagramId)
    return render_template('diagramBuilder.html')

@app.route('/diagram')
def diagram(dt,mn,diagram):
    if(diagram == '1'):
        return render_template('diagramViewTimelines.html' , data = dt , measureName = mn)
    elif(diagram == '2'):
        return render_template('diagramViewBarCharts.html' , data = dt , measureName = mn)
    elif(diagram == '3'):
        return render_template('diagramViewScatterPlots.html' , data = dt , measureName = mn)    
    
def idToSelection(id):
    measure = ''
    if(id == '1'):
        measure = 'Female_industry_workers_percent_of_female_employment'
    elif(id == '2'):
            measure = 'Female_long_term_unemployment_rate_percent'
    elif(id == '3'):
        measure = 'Female_service_workers_percent_of_female_employment'
    elif(id == '4'):
        measure = 'Happiness_score'
    elif(id == '5'):
        measure = 'Human_development_index'
    elif(id == '6'):
        measure = 'Industry_percent_of_gdb'
    elif(id == '7'):
        measure = 'Industry_workers_percent_of_employment'
    elif(id == '8'):
        measure = 'Long_term_unemployment_rate_percent'
    elif(id == '9'):
        measure = 'Male_industry_workers_percent_of_male_employment'
    elif(id == '10'):
        measure = 'Male_long_term_unemployment'
    elif(id == '11'):
        measure = 'Male_service_workers_percent_of_male_employment'
    elif(id == '12'):
        measure = 'Manuf_employ'
    elif(id == '13'):
        measure = 'Services_percent_of_gdp'
    elif(id == '14'):
        measure = 'Service_workers_percent_of_umployment'
    return measure        

def measureToText(id):
    measure = ''
    if(id == 'Female_industry_workers_percent_of_female_employment'):
        measure = 'Female industry workers percent of female employment'
    elif(id == 'Female_long_term_unemployment_rate_percent'):
            measure = 'Female long term unemployment rate percent'
    elif(id == 'Female_service_workers_percent_of_female_employment'):
        measure = 'Female service workers percent of female employment'
    elif(id == 'Happiness_score'):
        measure = 'Happiness score'
    elif(id == 'Human_development_index'):
        measure = 'Human development index'
    elif(id == 'Industry_percent_of_gdb'):
        measure = 'Industry percent of gdb'
    elif(id == 'Industry_workers_percent_of_employment'):
        measure = 'Industry workers percent of employment'
    elif(id == 'Long_term_unemployment_rate_percent'):
        measure = 'Long term unemployment rate percent'
    elif(id == 'Male_industry_workers_percent_of_male_employment'):
        measure = 'Male industry workers percent of male employment'
    elif(id == 'Male_long_term_unemployment'):
        measure = 'Male long term unemployment'
    elif(id == 'Male_service_workers_percent_of_male_employment'):
        measure = 'Male service workers percent of male employment'
    elif(id == 'Manuf_employ'):
        measure = 'Manuf employ'
    elif(id == 'Services_percent_of_gdp'):
        measure = 'Services percent of gdp'
    elif(id == 'Service_workers_percent_of_umployment'):
        measure = 'Service workers percent of umployment'
    return measure

def prepareDataForCharts(countries,year1,year2,measureType,diagram):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(year1<year2):
        startingYear = year1
        endingYear = year2
    else:
        startingYear = year2
        endingYear = year1
    finalList = []
    if(len(measureType) == 1):
        finalList.append([])
        finalList[0].append('Year')
        i=0
        while(int(endingYear)-int(startingYear)+1 != i):
            y_id = int(startingYear)+i
            if(len(finalList)-1 < i+1):
                finalList.append([])
                finalList[i+1].append(y_id)
            for c_id in countries:
                if(i==0):
                    finalList[0].append(c_id)
                query = '''
                    SELECT * FROM measures WHERE  Countries_C_ID = %s AND Years_Y_ID = %s 
                '''
                values = (c_id,y_id)
                cur.execute(query,values)
                results = cur.fetchall()
                results=results[0]
                finalList[i+1].append(results.get(measureType[0]))
            i+=1    
    else:
        if(diagram == '3'):
            finalList.append([])
            finalList[0].append('a')
            i=0
            while(int(endingYear)-int(startingYear)+1 != i):
                y_id = int(startingYear)+i
                if(len(finalList)-1 < i+1):
                    finalList.append([])
                for c_id in countries:
                    if(i==0):
                        finalList[0].append(c_id)            
                    query = '''
                        SELECT * FROM measures WHERE  Countries_C_ID = %s AND Years_Y_ID = %s 
                    '''
                    values = (c_id,y_id)
                    cur.execute(query,values)
                    results = cur.fetchall()
                    results=results[0]
                    if(results.get(measureType[0]) == None):
                        finalList[i+1].append(0)
                    else:
                        #finalList[i+1].append(results.get(measureType[0]))
                        finalList[i+1].append(float(round(results.get(measureType[0])*100,1)))
                    if(results.get(measureType[1]) == None):
                        finalList[i+1].append(0)
                    else:
                        #finalList[i+1].append(results.get(measureType[1]))
                        finalList[i+1].append(float((results.get(measureType[1])*10)))
                i+=1  
        else:
            countMeasures = []
            for c in countries:
                for m in measureType:
                    countMeasures.append(c)
                    countMeasures.append(m)
            finalList.append([])
            finalList[0].append('Year')
            i=0  
            while(int(endingYear)-int(startingYear)+1 != i):
                y_id = int(startingYear)+i
                if(len(finalList)-1 < i+1):
                    finalList.append([])
                    finalList[i+1].append(y_id)
                for c_id in countries:
                    j=0
                    while(j != len(measureType)):
                        if(i==0):
                            finalList[0].append(c_id + measureType[j])            
                        query = '''
                            SELECT * FROM measures WHERE  Countries_C_ID = %s AND Years_Y_ID = %s 
                        '''
                        values = (c_id,y_id)
                        cur.execute(query,values)
                        results = cur.fetchall()
                        results=results[0]
                        finalList[i+1].append(results.get(measureType[j]))
                        j+=1
                i+=1  
    return finalList
        
def timePeriodChanges(data,timePeriod):
    newData = []
    newData.append(data[0])
    if(timePeriod == '1'):
        period = 1
    elif(timePeriod == '2'):
        period = 5
    elif(timePeriod == '3'):
        period = 10
    elif(timePeriod == '4'):
        period = 20
    dataSize =len(data)-1.
    counter = 0
    i = 0
    while(1):
        if(dataSize/period > 1):
            i+=1
            newData.append([])
            year = ''
            c = 1
            year += str(data[counter+1][0])
            if(period != 1):   
                year += '-'
                year += str(data[counter + period][0])
            newData[i].append(year)
            while(c != len(data[0])):
                per = 0
                mo = 0
                p = 1  
                while(p-1 != period):
                    if(data[p + counter][c] != None):
                        mo += data[p + counter][c]
                        per +=1
                    p+=1
                c+=1
                if(per < 1):
                    mo=0
                else:
                    mo = mo / per
                newData[i].append(float(round(mo*100,1)))
            dataSize-=period
            counter += period
        else:
            newData.append([])
            year = ''
            c = 1
            year += str(data[counter+1][0])
            if(period !=1):  
                year += '-'
                year += str(data[len(data)-1][0])
            newData[len(newData)-1].append(year)
            while(c != len(data[0])):
                per = 0
                mo = 0
                p = 1
                while(p-1 != dataSize):
                    if(data[p][c] != None):
                        mo += data[p][c]
                        per +=1                  
                    p+=1
                c+=1
                if(per < 1):
                    mo=0
                else:
                    mo = mo / per
                newData[len(newData)-1].append(float(round(mo*100,1)))           
            break
    return newData

def findTextFromID(data,measureType,diagramId):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    i = 1
    while(i != len(data[0])):
        query = '''
                SELECT * FROM countries WHERE C_ID = %s 
            '''
        values = (data[0][i],)
        cur.execute(query,values)
        if(len(measureType) ==  1):
            data[0][i] = cur.fetchall()[0].get("C_Name")
        else:
            d = data[0][i][1:]
            d = d.replace("_"," ")
            data[0][i] = cur.fetchall()[0].get("C_Name") + " " + d
            data[0][i] = ''.join([a for a in data[0][i] if not a.isdigit()])

        i+=1
    if(data[0][0] == 'Year'):
        i = 1
        while(i != len(data)):
            years = data[i][0]
            years = years.split('-')
            j = 0
            yearsDescr = ''
            while(j != len(years)):
                query = '''
                    SELECT * FROM years WHERE Y_ID = %s 
                '''
                values = (years[j],)
                cur.execute(query,values)
                yearsDescr += cur.fetchall()[0].get("Year_Descr")
                if(j != len(years) - 1):
                    yearsDescr += '-'
                j+=1
            data[i][0] = yearsDescr
            i+=1
    return data 

def titleFixer(m):
    title = ''
    i=0
    if(len(m) == 1):
        title += m[0].replace("_"," ")
    else:
        for x in m:
            title += x.replace("_"," ")
            if(i+2 == len(m)):
                title += " and "
            elif(i+1 == len(m)):
                title += ""
            else:
                title += ", "
            i+=1
    return title


     
if __name__ == '__main__':
    app.run(debug=True)