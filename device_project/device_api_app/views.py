# api/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import redis


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@api_view(['GET'])
def get_latest_device_info(request, device_id):
    data = redis_client.hgetall(device_id)
    if not data:
        return Response({"error": "Device ID not found"}, status=status.HTTP_404_NOT_FOUND)

    data = {key.decode(): value.decode() for key, value in data.items()}
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_start_end_locations(request, device_id):
    data = redis_client.hgetall(device_id)
    if not data:
        return Response({"error": "Device ID not found"}, status=status.HTTP_404_NOT_FOUND)
    data = {key.decode(): value.decode() for key, value in data.items()}
    return Response({
        "start_location": (data['latitude'], data['longitude']),
        "end_location": (data['latitude'], data['longitude'])
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_location_points(request, device_id, start_time, end_time):
    location_points = []
    for key in redis_client.keys():
        key_str = key.decode()
        if key_str.startswith(device_id) and start_time <= redis_client.hget(key, b'time_stamp').decode() <= end_time:
            data = redis_client.hgetall(key)
            data = {key.decode(): value.decode() for key, value in data.items()}
            location_points.append({
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "time_stamp": data['time_stamp']
            })
        print("data----", start_time, end_time)
    return Response(location_points, status=status.HTTP_200_OK)
