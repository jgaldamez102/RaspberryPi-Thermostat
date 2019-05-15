from pprint import pprint
import json
import requests
import argparse
import LFSR
keys = LFSR.LFSRencrypt()
import random
class tempClient():
	def __init__(self, serv_addr, serv_pwd):
		self.serv_addr=serv_addr
		self.serv_prd=serv_pwd
		print('')

	def send_temp(self, address, temp):
		key = random.randint(0,len(keys))
		temp =int(temp)^keys[key]
		headers = {
			'Content-Type': 'application/json',
			'Authorization': None
		}
		payload = {
			'temp': temp,
			'key':key,
		}
		response = requests.post("http://{}/send_temp".format(address),headers=headers,data=json.dumps(payload))
		pprint(response.json())

def main():
    temp_client = tempClient(args.a,args.t)
    try:
        temp_client.send_temp(args.a,args.t)
    except Exception as e:
        print(e)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='tempClient',description='Used to change temp')
	parser.add_argument('-a', metavar = 'ip_addr:port_num',required = True, help='Password to access server')
	parser.add_argument('-t', metavar='temp',required=True,help='Desired temp')
	args = parser.parse_args()
	main()
