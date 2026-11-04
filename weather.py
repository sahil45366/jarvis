import requests


API_KEY = "314655f53b3e4ca0eea81a318f401e41"


def get_weather(city):

    try:

        city = city.strip()


        url = (
            "https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )


        response = requests.get(url)

        data = response.json()

        print("Weather Response:", data)


        if data.get("cod") != 200:

            return "City not found"


        temp = data["main"]["temp"]

        condition = data["weather"][0]["description"]


        return (
            f"{city} temperature is {temp} degree Celsius "
            f"with {condition}"
        )


    except Exception as e:

        print("Weather Error:", e)

        return "Unable to get weather"