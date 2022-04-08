from dataclasses import dataclass
from typing import List
import requests

@dataclass
class Location:
    latitude: float
    longitude: float
    price: float

def getPrices(borough: str, page: int) -> List[Location]:
    
    response = requests.post(
        url='https://www.trulia.com/graphql',
        json={
            "operationName": "WEB_searchResultsMapQuery",
            "query": """
query WEB_searchResultsMapQuery(
    $searchDetails: SEARCHDETAILS_Input!,
    $includeNearBy: Boolean!
) {
searchResultMap: searchHomesByDetails(searchDetails: $searchDetails, includeNearBy: $includeNearBy) {
    homes {
    location {
        coordinates {
        latitude
        longitude
        }
    }
    price {
        formattedPrice
    }
    }
}
}
            """,
            "variables": {
                "searchDetails": {
                    "searchType": "SOLD",
                    "location": {
                        "cities": [
                            {
                                "city": borough,
                                "state": "NY"
                            }
                        ]
                    },
                    "filters": {
                        "sort": {
                            "type": "LAST_SALE_DATE",
                            "ascending": False
                        },
                        "page": page,
                        "limit": 250,
                        "offset": 250 * (page + 1),
                        "isAlternateListingSource": False,
                        "propertyTypes": [],
                        "listingTypes": [],
                        "soldWithin": 9,
                        "pets": [],
                        "rentalListingTags": [],
                        "foreclosureTypes": [],
                        "buildingAmenities": [],
                        "unitAmenities": [],
                        "landlordPays": []
                    },
                },
                "includeNearBy": True,
            }
        }
    )
    response.raise_for_status()
    response = response.json()
        
    return [
        Location(
            latitude=item['location']['coordinates']['latitude'],
            longitude=item['location']['coordinates']['longitude'],
            price=_format_price(item['price']['formattedPrice'])
        )
        for item in response['data']['searchResultMap']['homes']
    ]
    

def _format_price(p: str) -> float:
    return float(p.replace('$', '').replace(',', ''))
