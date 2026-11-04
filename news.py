import requests


API_KEY = "433192f085ef48a3bebca7757044aedb"


def get_news(query="India"):

    try:

        url = (
    "https://newsapi.org/v2/everything?"
    f"q={query}&"
    "language=en&"
    "pageSize=5&"
    f"apiKey={API_KEY}"
)

        response = requests.get(url)

        data = response.json()

        print("News Response:", data)


        if data.get("status") != "ok":

            return "Unable to get news"


        articles = data.get(
            "articles",
            []
        )[:3]


        # No news found

        if not articles:

            return "No latest news available right now"


        news_text = "Today's top news are. "


        for article in articles:

            title = article.get(
                "title",
                ""
            )
            title = title.split(" - ")[0]

            

            news_text += title + ". "


        return news_text



    except Exception as e:

        print(
            "News Error:",
            e
        )

        return "News service is not available"