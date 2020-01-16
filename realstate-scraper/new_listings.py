import simplejson as json
from utils.database import BaseUrls
from bs4 import BeautifulSoup
import asyncio, httpx



async def get_soup(
    session: httpx.AsyncClient,
    base_url: str
) -> dict:
    print(f"Requesting {base_url}")
    resp = await session.get(base_url)
    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(f"Received data for {base_url}")
    return soup


async def main(base_urls):
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with httpx.AsyncClient() as session:
        tasks = []
        for base_url in base_urls:
            tasks.append(get_soup(session=session, base_url=base_url))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        soups = await asyncio.gather(*tasks, return_exceptions=True)
        return soups

def get_new_listings(event, context):
    base_urls = BaseUrls()
    base_urls = [item["baseUrl"] for item in base_urls.items]

    soups = asyncio.run(main(base_urls))

    body = {
        "baseUrls": [soup.title.text for soup in soups],
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
