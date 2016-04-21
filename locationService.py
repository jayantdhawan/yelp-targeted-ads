"""
Script to search the restaurants in nearby location using the google API 
"""

import requests
import json
import math
import time

# Function to return the latitude and longitude of a given location 
def get_latitude_and_longitude_by_location(location):
	google_api = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location
	response = requests.get(google_api)
	resp_json_payload = response.json()
	lat_lng_json = resp_json_payload['results'][0]['geometry']['location']
	return lat_lng_json

# Function to return the nearby businesses
def get_nearby_business_id(lat, lng, distance):
	nearby_business_ids = []
	with open("preprocess/restaurants.json", 'r') as business_file:
		for line in business_file:
			json_object = json.loads(line)
			# Compute the distance between src and des
			distance_from_to = get_mile_distance_from_to(lat, lng, json_object['latitude'], json_object['longitude'])
			if distance_from_to <= distance:
				nearby_business_ids.append(json_object['business_id'])
				# print json_object['business_id'], json_object['latitude'], json_object['longitude']	
	return nearby_business_ids

def get_mile_distance_from_to(src_lat, src_lng, des_lat, des_lng):
	# 3960 is Earth's radius by mile
	return distance_on_unit_sphere(src_lat, src_lng, des_lat, des_lng) * 3960

def distance_on_unit_sphere(src_lat, src_lng, des_lat, des_lng):
	# Reference from http://www.johndcook.com/blog/python_longitude_latitude/
    # Convert latitude and longitude to 
    # Spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - src_lat)*degrees_to_radians
    phi2 = (90.0 - des_lat)*degrees_to_radians
         
    # theta = longitude
    theta1 = src_lng*degrees_to_radians
    theta2 = des_lng*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc



def main():
	start_time = time.time()

	lat_lng_json = get_latitude_and_longitude_by_location('raleigh_nc') # get lat and lng via lat_lng_json['lat'], lat_lng_json['lng']  
	print lat_lng_json['lat'], lat_lng_json['lng'] # 40.3954586 -80.0229105
	print len(get_nearby_business_id(lat_lng_json['lat'], lat_lng_json['lng'], 3))

	end_time = time.time()
	print (end_time - start_time) % 60  # Get seconds

if __name__ == "__main__":
	main()