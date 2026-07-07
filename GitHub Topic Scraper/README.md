# Github-Repo-Topics-Scraper
This is web scraping project for Github Topics.
According to me it would be really helpful and beneficial for developers who are starting out to get data of different github repositories based on different topics.

### Libraries used: 
- requests
- beautifulsoup
- pandas

### Features of this Web Scraper:
1. It's going to scrape https://github.com/topics 
2. It'll get a list of topics. For each topic, we'll get topic title, topic page URL and topic description. 
3. For each topic, it'll get the top 25 repositories in the topic from the topic page.
4. For each repository, it'll grab the repo name, username, stars and repo URL.
5. For each topic it'll create a CSV file in the following format:

```
Repo Name,Username,Stars,Repo URL
three.js,mrdoob,69700,https://github.com/mrdoob/three.js
libgdx,libgdx,18300,https://github.com/libgdx/libgdx
```
