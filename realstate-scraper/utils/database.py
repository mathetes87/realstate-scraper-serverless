import boto3, os
import logging as log

class BaseUrls:
    def __init__(self):
        self._dynamo = boto3.resource('dynamodb', region_name="us-east-1")
        self.table_name = os.environ.get("baseUrlsTableName")
        self.table = self._dynamo.Table(self.table_name)
        log.info(f"Dynamo table name for base urls: '{self.table_name}'")
        self.items = self._get_items()

    def _get_items(self):
        response = self.table.scan()
        return response["Items"]

class Listings:
    def __init__(self):
        self._dynamo = boto3.resource('dynamodb', region_name="us-east-1")
        self.table_name = os.environ.get("listingsTableName")
        self.table = self._dynamo.Table(self.table_name)
        log.info(f"Dynamo table name for listings: '{self.table_name}'")

    def insert(self, listing):
        response = self.table.put_item(
            Item=listing
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        return



if __name__ == "__main__":
    os.environ["listingsTableName"] = "listingsTable"
    listings = Listings()

    print(listings.insert({
        "url": "test url",
        "other": 123
    }))