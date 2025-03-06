
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def fetch_meteo_data(latitude, longitude, start_date, end_date, temperature_variables):
    """
    Fetches temperature data from the Open-Meteo API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        temperature_variables (list): List of temperature variable names.

    Returns:
        pandas.DataFrame: DataFrame containing time and temperature data, or None on error.
    """
    variables_string = ",".join(temperature_variables)
    #url = f"https://api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&hourly={variables_string}&start_date={start_date}&end_date={end_date}"
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly={variables_string}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        time_data = data['hourly']['time']
        df = pd.DataFrame({'time': time_data})
        for var in temperature_variables:
            df[var] = data['hourly'][var]
        df['time'] = pd.to_datetime(df['time'])
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except KeyError as e:
        print(f"Error processing data: {e}")
        return None

def plot_temperature_data(df, temperature_variables):
    """
    Plots temperature data from a DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing time and temperature data.
        temperature_variables (list): List of temperature variable names.
    """
    if df is None:
        print("No Dataframe to plot")
        return

    plt.figure(figsize=(14, 8))
    for var in temperature_variables:
        label = var.replace("_", " ").title() + " (°C)"
        plt.plot(df['time'], df[var], label=label, marker='o', linestyle='-')

    plt.title('Temperature at Different Depths')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def calculate_and_print_daily_diffs(df, temperature_variables):
    """
    Calculates and prints daily sums of temperature differences (soil vs. air).

    Args:
        df (pandas.DataFrame): DataFrame containing time and temperature data.
        temperature_variables (list): List of temperature variable names.
    """
    if df is None:
        print("No Dataframe to calculate differences")
        return

    daily_diffs = {}
    for var in temperature_variables[1:]:
        diff_var = f"{var}_diff_to_air"
        df[diff_var] = df[var] - df["temperature_2m"]
        daily_diff = df.groupby(df['time'].dt.date)[diff_var].sum()
        daily_diffs[var] = daily_diff

    print("Daily Sums of Temperature Differences (Soil vs. Air):")
    for var, daily_diff in daily_diffs.items():
        overall = 0.0
        print(f"\n{var.replace('_', ' ').title()}:")
        for date, total_diff in daily_diff.items():
            print(f"{date}: {total_diff:.2f} °C")
            overall += total_diff
        print(f"total: {overall:.2f}")

