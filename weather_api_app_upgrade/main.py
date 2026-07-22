from config import validate_config
from weather_service import get_weather
from display import display_weather, display_error

def main():

    try:
        validate_config()
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("=" * 40)
    print("          WEATHER API APPLICATION")
    print("=" * 40)
    
    while True:

        try:
            # Get city name from the user
            city = input("\nEnter a city name (or type exit): ").strip()

            # Exit application
            if city.lower() == "exit":
                print("\nThank you for using the Weather API App.")
                break

            # Validate empty input
            if not city:
                display_error("Please, enter a city name.")
                continue

            #  Retrieve weather information
            result = get_weather(city)

            # Display result
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
            display_error(f"An unexpected error occurred: {error}")

if __name__ == "__main__":
    main()