# DISPLAY WEATHER INFORMATION IN A READABLE FORMAT

def display_weather(weather):
    print("\n" + "+" * 48)
    print("            WEATHER REPORT")
    print("=" *  48)

    print(f"City            : {weather['city']}")
    print(f"Country         : {weather['country']}")
    print(f"Temperature     : {weather['temperature']}℃")
    print(f"Feels Like      : {weather['feels_like']}℃")
    print(f"Humidity        : {weather['humidity']}%")
    print(f"Pressure        : {weather['pressure']}hPa")
    print(f"Condition       : {weather['description'].title()}")
    print(f"Wind Speed      : {weather['wind_speed']}m/s")

    print("=" * 48)

def display_error(message):
    """Display an error message."""
    print("\n" + "=" * 48)
    print("            ERROR")
    print("=" * 48)
    print(message)
    print("=" * 48)