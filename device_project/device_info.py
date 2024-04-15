import redis
import csv
from datetime import datetime

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

file_path = 'C:/Users/agrahsa/Documents/DSF/Django/device_project/device_sheet.csv'

def parse_timestamp(timestamp_str):
    timestamp_str = timestamp_str[:-1]
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

with open(file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    sorted_data = sorted(csv_reader, key=lambda x: parse_timestamp(x['sts']))
    print("data", sorted_data)


latest_data = {}
for row in sorted_data:
    device_id = row['device_fk_id']
    latest_data[device_id] = {
        'latitude': float(row['latitude']),
        'longitude': float(row['longitude']),
        'time_stamp': row['time_stamp']
    }

    for field, value in latest_data[device_id].items():
        redis_client.hset(device_id, field, value)


redis_data = {key.decode(): redis_client.hgetall(key) for key in redis_client.keys()}
print("Data stored in Redis cache:")
print(redis_data)
