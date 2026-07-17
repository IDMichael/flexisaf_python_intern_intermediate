# DISPLAY WEATHER INFORMATION IN A READABLE FORMAT

def display_weather(weather):
    print("\n" + "+" * 40)
    print("              WEATHER REPORT")
    print("=" *  40)

    print(f"City            : {weather['city']}")
    print(f"Country         : {weather['country']}")
    print(f"Temperature     : {weather['temperature']}℃")
    print(f"Feels Like      : {weather['feels_like']}℃")
    print(f"Humidity        : {weather['humidity']}%")
    print(f"Pressure        : {weather['pressure']}hPa")
    print(f"Condition       : {weather['description'].capitalize()}")
    print(f"Wind Speed      : {weather['wind_speed']}m/s")

    print("=" * 40)

def display_error(message):
    print("\n" + "=" * 40)
    print("                ERROR")
    print("=" * 40)
    print(message)
    print("=" * 40)