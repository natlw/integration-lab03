import requests
import json
from django.shortcuts import render
from django.http import JsonResponse

coordinates = {
    "Gdynia": ("54.52", "18.53"),
    "Warszawa": ("52.237", "21.017"),
}

def weather_view(request):
    place = "Gdynia"
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={coordinates[place][0]}&longitude={coordinates[place][1]}"
           f"&current=temperature_2m,wind_speed_10m"
           f"&hourly=temperature_2m,rain,weather_code,wind_speed_10m")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        times = data["hourly"]["time"][:24]
        temperatures = data["hourly"]["temperature_2m"][:24]
        current_temp = data["current"]["temperature_2m"]

        context = {
            "city": place,
            "times": json.dumps(times),
            "temperatures": json.dumps(temperatures),
            "current_temp": current_temp,
        }

    except requests.exceptions.RequestException as e:
        context = {
            "error": f"Błąd połączenia z API: {str(e)}"
        }

    return render(request, "external_data/weather.html", context)


def posts_view(request):
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json()

        user_posts = [post for post in posts if post["userId"] == 1]

        user_post_count = {}
        for post in posts:
            uid = post["userId"]
            user_post_count[uid] = user_post_count.get(uid, 0) + 1

        avg_title_length = round(sum(len(p["title"]) for p in posts) / len(posts), 2)

        context = {
            "user_posts": user_posts,
            "user_post_count": user_post_count,
            "avg_title_length": avg_title_length,
            "total_posts": len(posts),
        }

    except requests.exceptions.RequestException as e:
        context = {
            "error": f"Błąd połączenia z API: {str(e)}"
        }

    return render(request, "external_data/posts.html", context)


def weather_summary_api(request):
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={coordinates['Gdynia'][0]}&longitude={coordinates['Gdynia'][1]}"
           f"&hourly=temperature_2m"
           f"&forecast_days=1"
           f"&timezone=Europe/Warsaw")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temperatures = data["hourly"]["temperature_2m"][:24]

        summary = {
            "city": "Gdynia",
            "avg_temperature": round(sum(temperatures) / len(temperatures), 2),
            "max_temperature": max(temperatures),
            "min_temperature": min(temperatures),
        }

        return JsonResponse(summary)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)