from Scripts.createDB import mainCDB
from Scripts.transformData import mainTD,getCountries,getYears
from Scripts.loadData import mainLD

if __name__ == '__main__':
    mainCDB()
    mainTD()
    mainLD(getCountries(),getYears())
