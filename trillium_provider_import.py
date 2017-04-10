import json
import mysql.connector

#######################################################################################
# open mysql connection
#######################################################################################
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'npi',
  'raise_on_warnings': False,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


file = open("providers_4.8.17.txt",'r')
data = file.readlines()

################
# prep
################
sql0 = 'truncate tchp_providers'
cursor.execute(sql0)
cnx.commit()

sql0 = 'truncate tchp_locations'
cursor.execute(sql0)
cnx.commit()

sql0 = 'truncate tchp_specialties'
cursor.execute(sql0)
cnx.commit()

ii = 0

sql = []

for line in data:

    text = data[ii]

    json_txt_start = text.find('"providers":')
    json_txt_end = text.find(',"queryTime":{')
    json_txt2 = text[json_txt_start:json_txt_end]
    json_final = json.loads(json_txt2[12:])
    x = json.dumps(json_final, indent=4, sort_keys=True)

    for i in range(len(json_final)):
        val0 = json_final[i]['nationalProviderIdentifiers'][0]['nationalProviderIdentifier']
        val1 = json_final[i]['gender']
        val2 = json_final[i]['providerName']
        val3 = json_final[i]['firstName']
        val4 = json_final[i]['middleName']
        val5 = json_final[i]['lastName']
        val6 = json_final[i]['degree']

        sql1 = 'INSERT INTO tchp_providers (NPI, gender, providerName, firstName, middleName, lastName, degree) \
                VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(val0, val1, val2, val3, val4, val5, val6)

        if sql1 not in sql:
            sql.append(sql1)

        for iii in range(len(json_final[i]['networkLocation'])):
            #try:
            val0 = json_final[i]['nationalProviderIdentifiers'][0]['nationalProviderIdentifier']
            val1 = iii+1
            val2 = json_final[i]['networkLocation'][iii]['locationName']
            val3 = json_final[i]['networkLocation'][iii]['providerOrgName']
            val4 = json_final[i]['networkLocation'][iii]['primaryLocInd']
            val5 = json_final[i]['networkLocation'][iii]['addressLine1']
            val6 = json_final[i]['networkLocation'][iii]['addressLine2']
            val7 = json_final[i]['networkLocation'][iii]['cityName']
            val8 = json_final[i]['networkLocation'][iii]['stateCode']
            val9 = json_final[i]['networkLocation'][iii]['zipCode']
            val10 = json_final[i]['networkLocation'][iii]['countyName']
            val11 = json_final[i]['networkLocation'][iii]['coordinates']['lat']
            val12 = json_final[i]['networkLocation'][iii]['coordinates']['lon']

            sql1 = 'INSERT INTO tchp_locations (NPI, location_number, locationName, providerOrgName, locationPrimary, addressLine1, addressLine2, city, state, zip, county, lat, lon) \
                    VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                val0, val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12)

            if sql1 not in sql:
                sql.append(sql1)


                for iiii in range(len(json_final[i]['networkLocation'][iii]['specialty'])):
                    #try:
                    val0 = json_final[i]['nationalProviderIdentifiers'][0]['nationalProviderIdentifier']
                    val1 = json_final[i]['networkLocation'][iii]['specialty'][iiii]['fapGrouping']
                    val2 = json_final[i]['networkLocation'][iii]['specialty'][iiii]['specialtyDesc']


                    sql1 = 'INSERT INTO tchp_specialties (NPI, specialtyGroup, specialtyDesc) \
                            VALUES ("{}", "{}", "{}")'.format(
                        val0, val1, val2)

                    if sql1 not in sql:
                        sql.append(sql1)


    for int in range(len(sql)):
        #print(sql[int])
        try:
           cursor.execute(sql[int])
        except:
            continue
    cnx.commit()

    ii += 1