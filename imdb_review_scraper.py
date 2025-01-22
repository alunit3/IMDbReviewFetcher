import asyncio
import aiohttp
import random
import time
import pandas as pd
from typing import Dict, Any, List
import argparse

def generate_amazon_session_id():
    """Generates a random Amazon session ID."""
    return f"{random.randint(100, 999)}-{random.randint(1000000, 9999999)}-{int(time.time() * 1000) % 10000000}"

async def fetch_reviews(session: aiohttp.ClientSession, tconst: str, after: str = "", sort_by: str = "HELPFULNESS_SCORE") -> Dict[str, Any]:
    """
    Fetches reviews for a given title ID (tconst) from IMDb's GraphQL API.

    Args:
        session: The aiohttp ClientSession to use for the request.
        tconst: The IMDb title ID (e.g., "tt10919420").
        after: The cursor for pagination (optional).
        sort_by: The sorting criteria ("HELPFULNESS_SCORE" or "SUBMISSION_DATE").

    Returns:
        The JSON response from the API as a dictionary.
    """
    sessionid = generate_amazon_session_id()
    headers = {
        'Host': 'caching.graphql.imdb.com',
        'X-Apollo-Operation-Id': '80ddad46e8e68fcfef2d7a400809a4ab7fd6d5213d8e313befa3db0a963bff68',
        'X-Apollo-Operation-Name': 'TitleUserReviewsQuery',
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'X-Imdb-Consent-Info': 'e30',
        'X-Imdb-Weblab-Search-Algorithm': 'C',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Supreme; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36 IMDb/9.1.2.109120200 (Supreme|Supreme; Android 34; Supreme) IMDb-flg/9.1.2 (1080,2031,403,402) IMDb-var/app-andr-ph',
        'X-Imdb-Client-Name': 'imdb-app-android',
        'X-Imdb-Client-Version': '9.1.2.109120200',
        'Content-Type': 'application/json',
        'X-Imdb-User-Language': 'en-US',
        'X-Imdb-User-Country': 'US',
        'X-Amzn-Sessionid': sessionid,
    }

    if sort_by not in ["HELPFULNESS_SCORE", "SUBMISSION_DATE"]:
        raise ValueError("Invalid sort_by value. Must be either 'HELPFULNESS_SCORE' or 'SUBMISSION_DATE'")

    params = {
        'operationName': 'TitleUserReviewsQuery',
        'variables': f'{{"tConst":"{tconst}","sort":{{"by":"{sort_by}","order":"DESC"}},"after":"{after}","filter":{{}}}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"80ddad46e8e68fcfef2d7a400809a4ab7fd6d5213d8e313befa3db0a963bff68"}}',
    }

    async with session.get('https://caching.graphql.imdb.com/', params=params, headers=headers) as response:
        return await response.json()

async def extract_reviews_data(tconst: str, sort_by: str = "HELPFULNESS_SCORE") -> List[Dict[str, Any]]:
    """
    Extracts reviews data for a given title ID, handling pagination.

    Args:
        tconst: The IMDb title ID.
        sort_by: The sorting criteria ("HELPFULNESS_SCORE" or "SUBMISSION_DATE").

    Returns:
        A list of dictionaries, where each dictionary represents a review.
    """
    all_reviews = []
    end_cursor = ""
    page_num = 1
    total_reviews = 0

    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Fetching page {page_num} for title ID '{tconst}' (sorting by {sort_by})...")
            response_json = await fetch_reviews(session, tconst, end_cursor, sort_by)

            if 'data' not in response_json or 'title' not in response_json['data'] or 'reviews' not in response_json['data']['title']:
                print(f"Error: Invalid response format or no reviews found. Response: {response_json}")
                print("This might be due to an issue with the IMDb API or an invalid title ID.")
                break

            reviews_data = response_json['data']['title']['reviews']

            if reviews_data is None:
                print(f"No reviews found for tconst: {tconst}")
                break
            
            num_reviews_on_page = len(reviews_data['edges'])
            total_reviews += num_reviews_on_page
            print(f"Retrieved {num_reviews_on_page} reviews on this page. Total reviews fetched so far: {total_reviews}")

            for edge in reviews_data['edges']:
                review = edge['node']
                all_reviews.append({
                    'author_id': review['author']['id'],
                    'author_name': review['author']['nickName'],
                    'summary': review['summary']['originalText'] if review['summary'] else None,
                    'review_text': review['text']['originalText']['plainText'] if review['text'] and review['text']['originalText'] else None,
                    'submission_date': review['submissionDate'],
                    'helpfulness_upvotes': review['helpfulness']['upVotes'],
                    'helpfulness_downvotes': review['helpfulness']['downVotes'],
                    'helpfulness_score': review['helpfulness']['score'],
                    'author_rating': review['authorRating'],
                })

            page_info = reviews_data['pageInfo']
            end_cursor = page_info['endCursor']
            if end_cursor is None:
                print(f"All pages fetched for title ID '{tconst}'. Total reviews extracted: {total_reviews}")
                break

            page_num += 1
    return all_reviews

def main():
    parser = argparse.ArgumentParser(description="Scrape IMDb reviews for a given title ID.")
    parser.add_argument("tconst", help="The IMDb title ID (e.g., tt11280740). You can find this in the URL of the movie/show on IMDb.")
    parser.add_argument("-s", "--sort_by", choices=["HELPFULNESS_SCORE", "SUBMISSION_DATE"], default="HELPFULNESS_SCORE",
                        help="How to sort the reviews (default: HELPFULNESS_SCORE).")
    parser.add_argument("-o", "--output", help="The output filename (default: imdb_reviews_[tconst]_[sort_by].xlsx).")
    args = parser.parse_args()

    tconst = args.tconst
    sort_by = args.sort_by
    output_filename = args.output

    if not output_filename:
        output_filename = f"imdb_reviews_{tconst}_{sort_by}.xlsx"

    print(f"Starting IMDb review scraper for title ID: {tconst}")
    print(f"Sorting reviews by: {sort_by}")
    print(f"Output file will be saved as: {output_filename}")

    loop = asyncio.get_event_loop()
    reviews = loop.run_until_complete(extract_reviews_data(tconst, sort_by))
    loop.close()

    if reviews:
        df = pd.DataFrame(reviews)
        df.to_excel(output_filename, index=False)
        print(f"Reviews successfully saved to {output_filename}")
    else:
        print("No reviews were extracted.")
        print("Please check the title ID and try again. If the issue persists, it might be a problem with the IMDb API.")

if __name__ == "__main__":
    main()