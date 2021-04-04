import requests 
import datetime
from flask import request

#get json weatherdata
def get_weather_json():
    ip_address = request.remote_addr
    #for testing localhost ipdata is changed 
    #print(ip_address)
    if str(ip_address) == "127.0.0.1":
        ip_address = "90.194.108.13"
    #print(ip_address)
    reg = requests.get('http://ip-api.com/json/{ip}'.format(ip=ip_address)) 
    #Using IP-API to obtain the user IP address, to find the users current location 
    ip_data = reg.json()
    lat = float(ip_data['lat']) #Extracting Latitude data from JSON return        
    lon = float(ip_data['lon']) #Extracting Longitudinal data from  JSON return 
    location = ip_data['city']
    req = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(lon)+'&appid=2e0c8a3dcfbaa00cbe3b5d5c2909ddc1')
    #Using openweather API to get the weather data using the latitude and longitudinal data.The current weather and the weather for the next 5 days would be returned  
    json_vals = req.json()
    json_data = json_vals['list']
    #print(len(json_data))


    json_extracted_list=[]    
    for day in range(int(len(json_data)/8)):
        minVal = 999
        maxVal = 0
        for measurement in range(8): #there are 8 measurements / day
            json_measurement = json_data[day*8+measurement]
            #print(json_measurement)
            if (json_measurement['main']['temp_min'] - 273) < minVal:
                minVal = json_measurement['main']['temp_min'] - 273
            if (json_measurement['main']['temp_max'] - 273) > maxVal:
                maxVal = json_measurement['main']['temp_max'] - 273
        datet = datetime.datetime.strptime(json_data[day*8]['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date = datet.date()
        #print(str(date)+"->Min: "+str(minVal)+" Max: "+str(maxVal))
        json_element = {"date":str(date), "max":"{number:4.2f}".format(number=maxVal), "min":"{number:4.2f}".format(number=minVal)}
        json_extracted_list.append(json_element)

    json_retval = {"title":"Weather forecast", "Region":location, "days":json_extracted_list}
    return json_retval