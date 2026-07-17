import traceback
from weather_service import get_weather
from display import display_weather, display_error

def main():
    print("=" * 40)
    print("          WEATHER API APPLICATION")
    print("=" * 40)
    while True:
        try:
            city = input("\nEnter a city name: ").strip()

            # Validate empty input
            if not city:
                print("Please, enter a city name.")
                continue

            # Exit input
            if city.lower() == "exit":
                print("\nThank you for using the Weather API App.")
                break

            # Get weather information
            result = get_weather(city)

            # Display weather or error message
            if result["success"]:
                display_weather(result["data"])
            else:
                display_error(result["message"])

            # Ask if the user wants another search
            choice = input("\nSearch another city? (yes/no): ").strip().lower()

            if choice not in ("yes", "y"):
                print("\nGoodbye!")
                break

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by the user.")
            break

        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            traceback.print_exc()

if __name__ == "__main__":
    main()