import googlemaps
import pandas as pd
import time
from LotteryRetailerNC.geocoding_utils import get_county_from_address


def scrape_lottery_retailers(api_key):
    # Initialize the Google Maps API client
    gmaps = googlemaps.Client(key=api_key)

    # Load existing data from the Excel file if it exists
    try:
        df = pd.read_excel('lottery_retailers.xlsx')
    except FileNotFoundError:
        # If the file doesn't exist, create an empty DataFrame
        df = pd.DataFrame(columns=['Name', 'County', 'Address', 'Link'])

    # List of NC counties
    nc_counties = ['Alamance', 'Alexander', 'Alleghany', 'Anson', 'Ashe', 'Avery', 'Beaufort', 
                   'Bertie', 'Bladen', 'Brunswick', 'Buncombe', 'Burke', 'Cabarrus', 'Caldwell',
                     'Camden', 'Carteret', 'Caswell', 'Catawba', 'Chatham', 'Cherokee', 'Chowan',
                       'Clay', 'Cleveland', 'Columbus', 'Craven', 'Cumberland', 'Currituck', 'Dare',
                         'Davidson', 'Davie', 'Duplin', 'Durham', 'Edgecombe', 'Forsyth', 'Franklin', 
                         'Gaston', 'Gates', 'Graham', 'Granville', 'Greene', 'Guilford', 'Halifax', 
                         'Harnett', 'Haywood', 'Henderson', 'Hertford', 'Hoke', 'Hyde', 'Iredell', 
                         'Jackson', 'Johnston', 'Jones', 'Lee', 'Lenoir', 'Lincoln', 'Macon', 'Madison',
                         'Martin', 'McDowell', 'Mecklenburg', 'Mitchell', 'Montgomery', 'Moore', 'Nash', 
                         'New Hanover', 'Northampton', 'Onslow', 'Orange', 'Pamlico', 'Pasquotank', 'Pender',
                         'Perquimans', 'Person', 'Pitt', 'Polk', 'Randolph', 'Richmond', 'Robeson', 'Rockingham',
                         'Rowan', 'Rutherford', 'Sampson', 'Scotland', 'Stanly', 'Stokes', 'Surry', 'Swain', 
                         'Transylvania', 'Tyrrell', 'Union', 'Vance', 'Wake', 'Warren', 'Washington', 'Watauga', 
                         'Wayne', 'Wilkes', 'Wilson', 'Yadkin', 'Yancey']

    # Iterate through counties
    for county in nc_counties:
        # Initialize page token to None for the first iteration
        page_token = None

        # Loop to fetch multiple pages of results
        while True:
            # Search for lottery retailers in North Carolina county
            places_result = gmaps.places(query=f"lottery retailers in {county} County, North Carolina", region="US-NC", page_token=page_token)

            
            df = process_results(places_result, df, gmaps)

            
            if 'next_page_token' in places_result:
                # Wait briefly before making the next request (as per API guidelines I beleive)
                time.sleep(2)
                
                # Set the page token for the next iteration
                page_token = places_result['next_page_token']
            else:
                
                break

    # Export DataFrame to Excel file
    df.to_excel('lottery_retailers.xlsx', index=False)


def process_results(places_result, df, gmaps):
    
    new_rows = []

    for place in places_result.get('results', []):
        name = place.get('name', 'N/A')
        address = place.get('formatted_address', 'N/A')
        
        
        place_id = place.get('place_id', 'N/A')

        # Check if the place is closed temporarily or permanently
        business_status = place.get('business_status', 'OPERATIONAL')

        if business_status not in ['CLOSED_TEMPORARILY', 'CLOSED_PERMANENTLY']:
            
            county = get_county_from_address(address, gmaps)

            
            link = f'https://www.google.com/maps/place/?q=place_id:{place_id}'

            
            new_rows.append({'Name': name, 'County': county, 'Address': address, 'Link': link})

            
            print("Name:", name)
            print("County:", county)
            print("Address:", address)
            print("Link:", link)
            print("---")

    
    new_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    new_df = new_df.drop_duplicates(subset=['Name', 'Address'])

    return new_df


def get_county_from_address(address, gmaps):
   
    geocode_result = gmaps.geocode(address)

   
    for component in geocode_result[0]['address_components']:
        if 'administrative_area_level_2' in component['types']:
            return component['long_name']

    return 'N/A'
