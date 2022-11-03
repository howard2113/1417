from flask import Flask, request, jsonify
import requests
import psycopg2
import asyncio
from time import sleep

# database information
host = "localhost"
dbname = "thi"
user = "thi"
password = "thi"
sslmode = "allow"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection success")

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/parking-data/license-plate', methods=['POST'])
def license_plate():
  req = request.get_json()
  cursor = conn.cursor()
  try:
    for v in req:
      cursor.execute("INSERT INTO public.license_plates \
      (parking_id, parking_name, license_plate, datetime, state) \
      VALUES (%s,%s,%s,%s,%s);", 
      (v["parking_id"], v["parking_name"], v["license_plate"], v["datetime"], v["state"]))
    
    conn.commit()
    cursor.close()

    return jsonify({"code": 200, "msg":"OK", "data": None})
  except Exception as e:
    print('/license-plate fail:' + str(e))
    print(req)
    line('/license-plate fail:' + str(e))
    conn.rollback()
    cursor.close()
    return jsonify({"code": 500, "msg":"Server Error", "data": ValueError})


@app.route('/api/v1/parking-data/parking', methods=['POST'])
def parking():
  req = request.get_json()
  cursor = conn.cursor()
  errorList = []
  try:
    for v in req:
      try:
        cursor.execute("INSERT INTO public.off_street_parkings \
        (parking_id, parking_method, parking_type, longitude, latitude, \
        parking_register, business_method, charging_method, charges, large_car, \
        disability_car, disability_moto, electric_car, electric_moto, women_car, \
        reward_car) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
        ON CONFLICT (parking_id, parking_method, parking_type, parking_register) \
        DO UPDATE \
        SET longitude = EXCLUDED.longitude, \
         latitude = EXCLUDED.latitude, \
         business_method = EXCLUDED.business_method, \
         charging_method = EXCLUDED.charging_method, \
         charges = EXCLUDED.charges, \
         large_car = EXCLUDED.large_car, \
         disability_car = EXCLUDED.disability_car, \
         disability_moto = EXCLUDED.disability_moto, \
         electric_car = EXCLUDED.electric_car, \
         electric_moto = EXCLUDED.electric_moto, \
         women_car = EXCLUDED.women_car, \
         reward_car = EXCLUDED.reward_car;", 
        (v["parking_id"], v["parking_method"], v["parking_type"], v["longitude"], v["latitude"], 
        v["parking_register"], v["business_method"], v["charging_method"], v["charges"], v["large_car"], 
        v["disability_car"], v["disability_moto"], v["electric_car"], v["electric_moto"], v["women_car"],
        v["reward_car"]))
      except :
        errorList.append(v)
        continue
    conn.commit()
    cursor.close()

    if len(errorList) != 0:
      print('/parking error list:')
      print(errorList)

    return jsonify({"code": 200, "msg":"OK", "data": None})
  except Exception as e:
    print('/parking fail:' + str(e))
    print(req)
    line('/parking fail:' + str(e))
    conn.rollback()
    cursor.close()
    return jsonify({"code": 500, "msg":"Server Error", "data": ValueError})

@app.route('/api/v1/parking-data/usage-rate', methods=['POST'])
def usage_rate():
  req = request.get_json()
  cursor = conn.cursor()
  try:
    for v in req:
      cursor.execute('INSERT INTO public.usage_rates \
      (parking_register, parking_name, district, address, "year", \
      "month", car_type, average_parking_rate, peak_parking_rate) \
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);', 
      (v["parking_register"], v["parking_name"], v["district"], v["address"], v["year"], 
      v["month"], v["car_type"], v["average_parking_rate"], v["peak_parking_rate"]))
    
    conn.commit()
    cursor.close()

    return jsonify({"code": 200, "msg":"OK", "data": None})
  except Exception as e:
    print('/usage-rate fail:' + str(e))
    print(req)
    line('/usage-rate fail:' + str(e))
    conn.rollback()
    cursor.close()
    return jsonify({"code": 500, "msg":"Server Error", "data": ValueError})

@app.route('/api/v1/parking-data/month-report', methods=['POST'])
def month_report():
  req = request.get_json()
  cursor = conn.cursor()
  try:
    for v in req:
      cursor.execute('INSERT INTO public.month_reports \
      (parking_register, parking_name, "year", "month", total_revenue, \
      total_expenses, total_net_income) \
      VALUES (%s,%s,%s,%s,%s,%s,%s);', 
      (v["parking_register"], v["parking_name"], v["year"], v["month"], v["total_revenue"], 
      v["total_expenses"], v["total_net_income"]))
    
    conn.commit()
    cursor.close()

    return jsonify({"code": 200, "msg":"OK", "data": None})
  except Exception as e:
    print('/month-report fail:' + str(e))
    print(req)
    line('/month-report fail:' + str(e))
    conn.rollback()
    cursor.close()
    return jsonify({"code": 500, "msg":"Server Error", "data": ValueError})

# for line notify
def line(mes):
  print(mes)
  req = requests.post(
    'https://notify-api.line.me/api/notify', 
    headers = {
      'Authorization' : 'Bearer ' + 'hGc3qwvXQfYGTlNQ4WBcRz2VezMqZu2w0q5SFczEqos',
      'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    data = {
      'message': mes
    },
    verify=False
  )

if __name__ == "__main__":
    app.run(port=3636)
