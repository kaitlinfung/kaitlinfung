import pyodbc 

#This function connects to our local MS SQL Server database called Cosmetic. 
def getConnect():
    server = 'localhost' 
    database = 'Cosmetic' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    return cnxn

#Prompt for the product name from the user
print('Please type the product name to search for hazards:')
product_name = input()


#Establishes database connection and query statement
#The SQL query utilizes a join statement to link two tables within the database 
#The two tables contain data from the open source Kaggle data sets. The first sets which contains the reportable ingredients list may be downloaded from this repository. 
#The file names is Reportable_Ingredients_List.xlsx
#The second data set contains the product list with its chemical ingredients. It can be downloaded from the following Kaggle link:
#https://www.kaggle.com/yamqwe/chemicals-in-cosmeticse
cnxn = getConnect()
cursor = cnxn.cursor()
stmt = 'SELECT DISTINCT c.ProductName, c.CasNumber, c.ChemicalName, '\
    'c.CompanyName, i.HazardTraits, i.Hazardcount '\
    'FROM Cosmetic_chemicals c '\
    'LEFT JOIN Ingredients_List i '\
    'ON c.CasNumber = i.CasNumber where ProductName like \'%{}%\''.format(product_name)
cursor.execute(stmt)
row = cursor.fetchone()
f = open("../Cosmetic Chemicals/chem_info.txt", "w")
header = '{:<29} {:<34} {:<24} {:<44} {:<3}'.format('Product Name', 'Chemical Name', 'Company Name', 'Hazard Traits','Hazard Count')
print(header)
f.write(header)
while row:
    if (row):
        name = 'NA'
        if row.ProductName:
            name = row.ProductName
            name = (name[:25] + '..') if len(name) > 25 else name
        chemName = 'NA'
        if (row.ChemicalName):
            chemName = row.ChemicalName
            chemName = (chemName[:30] + '..') if len(chemName) > 30 else chemName
        companyName = 'NA'
        if (row.CompanyName):
            companyName = row.CompanyName
            companyName = (companyName[:22] + '..') if len(companyName) > 22 else companyName
        hazards = 'NA'
        if (row.HazardTraits):
            hazards = row.HazardTraits
            hazards = (hazards[:40] + '..') if len(hazards) > 40 else hazards
        hazardcount = '0'
        if (row.Hazardcount):
            hazardcount = str(int(row.Hazardcount))

        var_names = '{:<29} {:<34} {:<24} {:<44} {:<3}'.format(name, chemName, companyName,hazards,hazardcount)
        print(var_names)
        f.write(var_names)
    row = cursor.fetchone()

cnxn.close()
f.close()