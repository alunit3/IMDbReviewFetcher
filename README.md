# IMDb Review Scraper

This project provides a Python-based tool to scrape user reviews from IMDb for any given movie or TV show. It leverages IMDb's GraphQL API to efficiently retrieve reviews, making it a powerful tool for academic research, sentiment analysis, and understanding public opinion about media content.

## Disclaimer

This tool is intended solely for **educational and academic purposes**. It allows researchers and enthusiasts to analyze trends in user reviews, study public perception of movies/shows, and perform sentiment analysis. It should not be used for commercial purposes or in any way that violates IMDb's terms of service. The developers of this tool are not responsible for any misuse.

## Features

-   **API-Based:** This scraper directly interacts with IMDb's GraphQL API, ensuring fast and efficient data retrieval compared to traditional web scraping methods that rely on parsing HTML.
-   **Pagination Support:**  Handles pagination automatically, allowing you to fetch all available reviews for a title, not just those displayed on the first page.
-   **Sorting:**  Allows sorting of reviews by either helpfulness score (default) or submission date.
-   **Structured Data:** Extracts key information from each review, including:
    -   Author ID
    -   Author Name
    -   Review Summary
    -   Review Text
    -   Submission Date
    -   Helpfulness (Upvotes and Downvotes)
    -   Helpfulness Score
    -   Author Rating
-   **Output to Excel:** Saves the extracted data into a well-structured Excel file for easy analysis.
-   **Command-Line Interface:**  Provides a user-friendly command-line interface for easy operation.

## Requirements

-   Python 3.7+
-   `aiohttp`
-   `pandas`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/alunit3/IMDbReviewFetcher.git
    cd IMDbReviewFetcher
    ```
2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script is executed from the command line. Here's the basic usage:

```bash
python imdb_review_scraper.py <tconst> [-s SORT_BY] [-o OUTPUT_FILE]
```

-   **`<tconst>`:** The IMDb title ID (required). You can find this in the URL of the movie/show on IMDb. For example, in the URL `https://www.imdb.com/title/tt0903747/`, the title ID is `tt0903747`.
-   **`-s SORT_BY`** or **`--sort_by SORT_BY`:**  Specifies how to sort the reviews. Options are `HELPFULNESS_SCORE` (default) and `SUBMISSION_DATE`.
-   **`-o OUTPUT_FILE`** or **`--output OUTPUT_FILE`:** Specifies the output Excel filename. If not provided, it defaults to `imdb_reviews_[tconst]_[sort_by].xlsx`.

**Example:**

To scrape reviews for the title `tt0903747`, sort them by submission date, and save them to `reviews.xlsx`, use the following command:

```bash
python imdb_review_scraper.py tt0903747 -s SUBMISSION_DATE -o reviews.xlsx
```

## Example Output

The output Excel file will contain a table with the following columns:

| Column              | Description                                                                                                      |
| :------------------ | :--------------------------------------------------------------------------------------------------------------- |
| `author_id`         | The unique ID of the review author on IMDb.                                                                     |
| `author_name`       | The nickname of the review author.                                                                              |
| `summary`           | The summary of the review (if provided by the author).                                                           |
| `review_text`       | The full text of the review.                                                                                     |
| `submission_date`   | The date the review was submitted.                                                                                |
| `helpfulness_upvotes` | The number of users who found the review helpful (upvotes).                                                    |
| `helpfulness_downvotes` | The number of users who did not find the review helpful (downvotes).                                       |
| `helpfulness_score` | The overall helpfulness score of the review.                                                                     |
| `author_rating`    | The rating given by the author to the movie/show (typically out of 10).                                          |

## Potential Use Cases in Academic Research

-   **Sentiment Analysis:** Analyze the text of reviews to determine the overall sentiment (positive, negative, neutral) towards a movie or show.
-   **Trend Analysis:** Track how reviews change over time or correlate with external events (e.g., awards, news).
-   **Marketing Research:** Study how user reviews might impact box office success or viewership numbers.
-   **Recommendation Systems:** Use review data to develop or improve movie/show recommendation algorithms.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the CC BY-SA 4.0 License - see the [LICENSE](LICENSE) file for details.
