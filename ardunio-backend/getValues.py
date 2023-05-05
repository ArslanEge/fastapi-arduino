# import serial
# import time
# import re
# import requests
# from datetime import datetime

# ser = serial.Serial('/dev/cu.usbserial-10', 9600)  # replace with the correct serial port and baud rate
# url = 'http://localhost:8000/arduino/heat'

# while True:
#     # wait for the serial connection to be established
#     time.sleep(2)

#     # read the response from the Arduino
#     response = ser.readline().decode('utf-8').strip()

#     # extract the temperature and humidity values from the response
#     match = re.match(r'Temperature: (\d+\.\d+) C, Humidity: (\d+\.\d+) %', response)
#     if match:
#         temperature = float(match.group(1))
#         humidity = float(match.group(2))
#         print('Temperature: {} C, Humidity: {} %'.format(temperature, humidity))

#         # get the current date and time
#         now = datetime.now()

#         current_month = str(now.month)
#         current_day = str(now.day)
#         current_hour = str(now.hour)
#         current_minute = str(now.minute)

#         date_time = str(current_month+"/"+current_day+"/"+current_hour+"/"+current_minute)

#         # create the data to be sent in the HTTP POST request
#         tvalue=str(temperature)
#         hvalue=str(humidity)
#         data = {
#             'temperature': tvalue,
#             'humidity': hvalue,
#             'date_time': date_time
#         }
#         header = {
#       'Content-Type': 'application/json',
#     }

#         # make the HTTP POST request
#         try:
#             response = requests.post(url,json=data,timeout=10,headers=header)
#             response.raise_for_status()  # raise an exception for 4xx/5xx status codes
#             print('Data successfully sent!')
#         except requests.exceptions.HTTPError as e:
#             print('Failed to send data: {}'.format(e))
#         except requests.exceptions.RequestException as e:
#             print('Request error: {}'.format(e))

#     else:
#         print('Invalid response: {}'.format(response))

#     # wait before sending the next request
#     time.sleep(10)

# ser.close()
