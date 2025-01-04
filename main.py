import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to download the page
def get_topic_link(base_url):
    try:
        response = req.get(url=base_url)
        response.raise_for_status()
    except req.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return []

    page_content = response.text
    print(response.status_code)

    soup = BeautifulSoup(page_content, "html.parser")
    tags = soup.find_all("div", class_="py-4 border-bottom d-flex flex-justify-between")
    topic_links = []

    for tag in tags:
        url_end = tag.find("a")["href"]
        topic_link = f"https://www.github.com{url_end}"
        topic_links.append(topic_link)
    return topic_links

# Function to extract topic information
def get_info_topic(topic_link):
    response1 = req.get(topic_link)
    topic_soup = BeautifulSoup(response1.text, "html.parser")
    topic_tag = topic_soup.find("h1").text.strip()
    topic_desc = topic_soup.find("p").text
    return {"title": topic_tag, "desc": topic_desc}

# Function to extract repo tags
def get_info_tags(topic_link):
    response = req.get(topic_link)
    info_soup = BeautifulSoup(response.text, "html.parser")
    return info_soup.find_all("div", class_="d-flex flex-justify-between flex-items-start flex-wrap gap-2 my-3")

# Function to extract repo information
def get_info(tag):
    repo_username = tag.find_all("a")[0].text.strip()
    repo_name = tag.find_all("a")[1].text.strip()
    url_end = tag.find("a")["href"]
    repo_url = f"https://www.github.com{url_end}"
    star_tag = tag.find("span", {"id": "repo-stars-counter-star"})
    repo_star = star_tag.text.strip() if star_tag else "0"

    return {
        "repo_username": repo_username,
        "repo_name": repo_name,
        "repo_url": repo_url,
        "repo_star": int(float(repo_star[:-1]) * 1000) if repo_star.endswith("k") else int(repo_star)
    }

# Function to save data to CSV
def save_CSV(results):
    df = pd.DataFrame(results)
    df.to_csv("github.csv", index=False)

# Function to save data to Excel
def save_XLX(results):
    df = pd.DataFrame(results)
    df.to_excel("github.xlsx", index=False)

# Main function to run the scraper
def main():
    base_url = "https://github.com/topics"
    topic_links = get_topic_link(base_url)
    result2 = []

    for topic_link in topic_links:
        print(f"Getting info {topic_link}")
        topic_tags = get_info_topic(topic_link)
        repo_tags = get_info_tags(topic_link)

        for tag in repo_tags:
            repo_info = get_info(tag)
            result2.append(topic_tags | repo_info)

        time.sleep(2)

    save_CSV(result2)
    save_XLX(result2)

if __name__ == "__main__":
    main()