"""Main file of Lottery Retailer NC"""


from LotteryRetailerNC.lottery_scraper import scrape_lottery_retailers
import googlemaps

if __name__ == "__main__":
                    #You have to put your own GOOGLE place api key here below 
    api_key = 'Your API Key'
    scrape_lottery_retailers(api_key)