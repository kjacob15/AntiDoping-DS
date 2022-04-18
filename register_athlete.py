import requests
import random
import datetime
import time
import sys

random.seed(random.randint(0,100))

def random_date(seed):
    d = random.randint(int(time.time()), int(time.time())+9999999)
    return datetime.date.fromtimestamp(d).strftime('%d/%m/%Y')

Regions = ['US','EU']
US_countries  = ['USA', 'Canada', 'Mexico']
EU_countries = ['UK', 'Ireland', 'Germany', 'France', 'Switzerland', 'Spain']


def generate_athelte(number):
	for i in range(number):

		region = Regions[(random.randint(0, 1))]
		print(region)

		if region == 'EU':
			location = EU_countries[random.randint(0, 5)]
		else:
			location = US_countries[random.randint(0, 2)]

		print(location)

		user_id = str(random.randint(100,10000))

		email = 'dummyAthelete' + user_id + "@tcd.ie"

		name = 'dummyAthelete' + user_id

		date = str(random_date(random.randint(int(time.time()), int(time.time())+9999999)))

		time_stamp = str(random.randint(9,22))

		data = {
			'email':email,
			'location':location,
			'time':time_stamp,
			'name':name,
			'date':date,
			'region': region 
		}

		res = requests.post('http://127.0.0.1:80/user/register_athlete', data=data)
		print(f'Athelte\n {data}\n registered successfully.')

if __name__ == '__main__':
	number = int(sys.argv[1])
	generate_athelte(number)

