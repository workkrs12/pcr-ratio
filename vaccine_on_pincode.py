import requests
# import main Flask class and request object
from flask import Flask, request,jsonify

# create the Flask app
app = Flask(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}


def fetch_monthly_dates():
	try:
		data=requests.get(f'https://opstra.definedge.com/api/weeklies',headers=headers).json()
		print(data)
		return data
	except Exception as e:
		print("Monthly dates fetching issue", e)
		pass

def fetch_pcr_data(month:str):
	try:
		data=requests.get(f'https://opstra.definedge.com/api/openinterest/optionchain/free/NIFTY&{month}',headers=headers).json()
		total_puts_oi=int(data['totalputoi'])
		total_calls_oi=int(data['totalcalloi'])
		# print(total_puts_oi/total_calls_oi)
		return total_puts_oi,total_calls_oi
	except Exception as e:
		print("Fetchiing pcr oi data fetching issue", e)
		return 0,0


@app.route('/')
def home():
	return jsonify("Hello PCR analysis")
@app.route('/pcr')
def fetch_pcr():
	monthly_dates=fetch_monthly_dates()
	pcr=0
	total_puts=0
	total_calls=0
	for monthly_date in monthly_dates:
		puts,calls=fetch_pcr_data(monthly_date)
		total_puts=total_puts+puts
		total_calls=total_calls+calls


	total_pcr=total_puts/total_calls

	print(total_pcr)
	return jsonify(total_pcr)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=False, port=5000)
