import requests
import random
import sys

random.seed(random.randint(0,100))

Countries = ['USA', 'Canada', 'Mexico','UK', 'Ireland', 'Germany', 'France', 'Switzerland', 'Spain']

def generate_athelte(number):
	for i in range(number):

		location = Countries[(random.randint(0, 8))]

		user_id = str(random.randint(100,10000))

		email = 'dummyADO' + user_id + "@tcd.ie"


		data = {
			'email':email,
			'location':location,
		}

		res = requests.post('http://127.0.0.1:80/user/register_ado', data=data)
		print(f'ADO\n {data}\n registered successfully.')


if __name__ == '__main__':
	number = int(sys.argv[1])
	generate_athelte(number)