# Generate list of urls to hit
# Hit url, save raw to outputfile
# Include checkpointing
import argparse
import concurrent.futures
import json
import os
import urllib.request
from datetime import date

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


def save_results(results, output_path):
    with open(output_path + ".temp", "w") as out_fp:
        json.dump(results, out_fp)
    os.rename(output_path + ".temp", output_path)


def load_results(output_path):
    if os.path.exists(output_path):
        with open(output_path) as fp:
            return json.load(fp)
    else:
        return {}


def main(output_path):
    # List of days.  Only the last year is available
    results = load_results(output_path)

    urls = []
    today = date.today()
    for daydelta in range(365):
        day = (today - relativedelta(days=daydelta)).strftime("%Y%m%d")
        # Loop month.  index at 1
        for sign in range(1, 13):
            url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={sign}&laDate={day}"
            if url not in results:
                urls.append(url)

    with concurrent.futures.ThreadPoolExecutor(1) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
        for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(urls)):
            url = future_to_url[future]
            try:
                data = future.result().decode()
                results[url] = data
                save_results(results, output_path)
            except Exception as exc:
                print("%r generated an exception: %s" % (url, exc))
            else:
                pass
                #print("%r page is %d bytes" % (url, len(data)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Scrapes horoscope.com's daily horoscopes for the past year
        """
    )
    parser.add_argument(
        "output_path", type=str, help="Path where the parsed data should be dumped."
    )
    args = parser.parse_args()
    main(args.output_path)
