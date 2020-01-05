import json
import os
import pandas as pd

from functools import reduce
from datetime import date


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def input(cardmember_dict):

	# Build another dictionary with ending 5 digits as the key.
	# key: ending
	# value: cardmember
	ending_dict = {} 

	logins = []

	for cardmember in cardmember_dict.keys():
		for login in cardmember_dict[cardmember]['logins'].keys():
			logins.append(login)
			for ending in cardmember_dict[cardmember]['logins'][login]['endings']:
				ending_dict[ending] = cardmember

	return ending_dict, logins

def concat(series):
	series = series.drop_duplicates()
	return reduce(lambda x, y: x+'\n'+y, series)

def main():
	dic = {'Cardmember':[],
		   'Card':[],
		   'Merchant':[],
		   'Bonus':[],
		   'Expiration':[],
		   'Status':[]}

	config_path = os.path.join('/Users','bzheng','github','amex-offer-monitor','json','config.json')
	with open(config_path) as configfile:
		cardmember_dict = json.load(configfile)['cardmembers']

	ending_dict, logins = input(cardmember_dict)

	for login in logins:
		path = os.path.join('/Users','bzheng','github','amex-offer-monitor','json','raw', 'amexoffers-data_' + login + '.json')

		try:
			with open(path) as json_file:
				data = json.load(json_file)
		except:
			continue
	   
		for card in data.keys():
			ending = card.split('-')[1][:5]
			cardmember = ending_dict[ending]

			
			for offer in data[card]:
				bonus = offer[0].split('\n')[0]
				merchant = offer[0].split('\n')[1]
				expiration = offer[1]
				status = offer[2]

				cardname = '\033[1m' + card + '\033[0m' if status == 'enrolled' else card

				dic['Cardmember'].append(cardmember)
				dic['Card'].append(cardname)
				dic['Bonus'].append(bonus)
				dic['Merchant'].append(merchant)
				dic['Expiration'].append(expiration)
				dic['Status'].append(status)

	df = pd.DataFrame(dic)

	by_name = df.groupby(['Cardmember','Merchant','Bonus','Expiration']).agg({'Card':['nunique',concat]}).rename(columns={'nunique':'Count','concat':'List'}).reset_index(level='Cardmember')
	by_offer = df.groupby(['Merchant','Bonus','Expiration']).agg({'Cardmember':['nunique',concat]}).rename(columns={'nunique':'Count','concat':'List'})

	agg = pd.merge(by_offer, by_name, how='inner', left_index=True, right_index=True)

	today = date.today().strftime('%Y-%m-%d')
	output_path = os.path.join('/Users','bzheng','github','amex-offer-monitor','json','parsed',today+'_summary.csv')

	agg.to_csv(output_path)

if __name__ == '__main__':
  main()
