
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics
import numpy as np
from scipy.stats import norm

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
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def calculate_and_print_hourly_diffs(df, var1, var2):

    if df is None:
        print("No Dataframe to calculate differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    print("Hourly Temperature Differences",var1," and ",var2)
    for index, row in df.iterrows():
        print(f"{row['time']}: {row[diff_var]:.2f} °C")

def calculate_and_plot_graph_hourly_diffs(df, var1, var2):
 
    if df is None:
        print("No Dataframe to plot differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]
    print(df[diff_var])
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df[diff_var], marker='o', linestyle='-')
    plt.title(f"Hourly Temperature Difference: {var2} - {var1}")
    plt.xlabel("Time")
    plt.ylabel("Temperature Difference (°C)")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # Add horizontal line at y=0
    plt.axhline(0, color='red', linestyle='--')
    plt.show()



def find_Hmm_2group(df, var1, var2):
    """
    Calculates the hourly difference between two variables, creates a binary list,
    groups consecutive 1s and 0s, and plots the difference.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        var1 (str): The name of the first variable.
        var2 (str): The name of the second variable.
    """

    if df is None:
        print("No Dataframe to plot differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    # Create the binary list
    binary_list = [1 if diff >= 1 else 0 for diff in df[diff_var]]
    #print(f"Binary List: {binary_list}")

    if not binary_list:
        print("Empty binary list.")
        return

    groups = []
    current_group = []
    current_value = binary_list[0]

    for value in binary_list:
        if value == current_value:
            current_group.append(value)
        else:
            groups.append(current_group)
            current_group = [value]
            current_value = value

    groups.append(current_group)  # Add the last group

    group_lengths = [len(group) for group in groups]

    group_1_lengths = []
    group_0_lengths = []

    for i in range(len(groups)):
        if groups[i][0] == 1:
            group_1_lengths.append(group_lengths[i])
        else:
            group_0_lengths.append(group_lengths[i])

    # print(f"Group 1 Lengths: {group_1_lengths}")
    # print(f"Group 0 Lengths: {group_0_lengths}")

    # Calculate the means
    mean_group_1 = sum(group_1_lengths) / len(group_1_lengths) if group_1_lengths else 0
    mean_group_0 = sum(group_0_lengths) / len(group_0_lengths) if group_0_lengths else 0
    std_dev_group_1 = statistics.stdev(group_1_lengths) if len(group_1_lengths) > 1 else 0
    std_dev_group_0 = statistics.stdev(group_0_lengths) if len(group_0_lengths) > 1 else 0


    print(f"Mean Group 1 Lengths: {mean_group_1}")
    print(f"Mean Group 0 Lengths: {mean_group_0}")
    print(f"Standard Deviation Group 1 Lengths: {std_dev_group_1}")
    print(f"Standard Deviation Group 0 Lengths: {std_dev_group_0}")

    # plt.figure(figsize=(10, 6))
    # plt.plot(df['time'], df[diff_var], marker='o', linestyle='-')
    # plt.title(f"Hourly Temperature Difference: {var2} - {var1}")
    # plt.xlabel("Time")
    # plt.ylabel("Temperature Difference (°C)")
    # plt.grid(True)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    # plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    # plt.xticks(rotation=45, ha='right')
    # plt.tight_layout()
    # # Add horizontal line at y=0
    # plt.axhline(0, color='red', linestyle='--')
    # plt.show()

    # Plotting Normal Distribution for group_1_lengths
    if len(group_1_lengths) > 1:
        plt.figure(figsize=(8, 6))
        x = np.linspace(min(group_1_lengths), max(group_1_lengths), 100)
        plt.plot(x, norm.pdf(x, mean_group_1, std_dev_group_1), 'r-')
        plt.hist(group_1_lengths, density=True, alpha=0.6, color='skyblue')
        plt.title(f"Normal Distribution (Group 1 Lengths)")
        plt.xlabel("Length")
        plt.ylabel("Probability Density")
        plt.tight_layout()
        plt.show()

    # Plotting Normal Distribution for group_0_lengths
    if len(group_0_lengths) > 1:
        plt.figure(figsize=(8, 6))
        x = np.linspace(min(group_0_lengths), max(group_0_lengths), 100)
        plt.plot(x, norm.pdf(x, mean_group_0, std_dev_group_0), 'r-')
        plt.hist(group_0_lengths, density=True, alpha=0.6, color='skyblue')
        plt.title(f"Normal Distribution (Group 0 Lengths)")
        plt.xlabel("Length")
        plt.ylabel("Probability Density")
        plt.tight_layout()
        plt.show()



    
def calculate_and_print_hourly_diffs_grouped(df, var1, var2):
    """
    Calculates hourly temperature differences, groups them into above/equal and below 0, and calculates the mean and standard deviation for each group.
    Also plots the normal distribution graph for each group.

    Args:
        df (pandas.DataFrame): DataFrame containing time and temperature data.
        var1 (str): name of the air temperature column
        var2 (str): name of the soil temperature column
    """
    if df is None:
        print("No Dataframe to calculate differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    print("Hourly Temperature Differences", var1, "and", var2, "(Grouped):")

    above_or_equal_zero = []
    below_zero = []

    for index, row in df.iterrows():
        diff = row[diff_var]
        if diff >= 0:
            above_or_equal_zero.append(diff)
        elif diff < 0:
            below_zero.append(diff)

    if above_or_equal_zero:
        print("\nAbove or Equal to 0 °C:")
        #for diff in above_or_equal_zero:
            #print(f"{diff:.2f} °C")
        if len(above_or_equal_zero) > 0:
            mean_above = sum(above_or_equal_zero) / len(above_or_equal_zero)
            std_dev_above = statistics.stdev(above_or_equal_zero)
            print(f"Mean: {mean_above:.2f} °C")
            print(f"Standard Deviation: {std_dev_above:.2f} °C")

            # Plotting Normal Distribution for above_or_equal_zero
            plt.figure(figsize=(8, 6))
            x = np.linspace(min(above_or_equal_zero), max(above_or_equal_zero), 100)
            plt.plot(x, norm.pdf(x, mean_above, std_dev_above), 'r-')
            plt.hist(above_or_equal_zero, density=True, alpha=0.6, color='skyblue')
            plt.title(f"Normal Distribution (Above/Equal 0 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    if below_zero:
        print("\nBelow 0 °C:")
        #for diff in below_zero:
            #print(f"{diff:.2f} °C")
        if len(below_zero) > 0:
            mean_below = sum(below_zero) / len(below_zero)
            std_dev_below = statistics.stdev(below_zero)
            print(f"Mean: {mean_below:.2f} °C")
            print(f"Standard Deviation: {std_dev_below:.2f} °C")

            # Plotting Normal Distribution for below_zero
            plt.figure(figsize=(8, 6))
            x = np.linspace(min(below_zero), max(below_zero), 100)
            plt.plot(x, norm.pdf(x, mean_below, std_dev_below), 'r-')
            plt.hist(below_zero, density=True, alpha=0.6, color='skyblue')
            plt.title(f"Normal Distribution (Below 0 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")


import pandas as pd
import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def calculate_and_print_hourly_diffs_3grouped(df, var1, var2):
    """
    Calculates hourly temperature differences, groups them into three ranges, and calculates the mean and standard deviation for each group.
    Also plots the normal distribution graph for each group.

    Args:
        df (pandas.DataFrame): DataFrame containing time and temperature data.
        var1 (str): name of the air temperature column
        var2 (str): name of the soil temperature column
    """
    if df is None:
        print("No Dataframe to calculate differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    print("Hourly Temperature Differences", var1, "and", var2, "(Grouped):")

    above_1_5 = []
    between_1_5_minus1_5 = []
    below_minus1_5 = []

    for index, row in df.iterrows():
        diff = row[diff_var]
        if diff >= 1.5:
            above_1_5.append(diff)
        elif -1.5 < diff < 1.5:
            between_1_5_minus1_5.append(diff)
        elif diff <= -1.5:
            below_minus1_5.append(diff)

    # Group 1: Above or Equal to 1.5
    if above_1_5:
        print("\nAbove or Equal to 1.5 °C:")
        if len(above_1_5) > 0:
            mean_above_1_5 = sum(above_1_5) / len(above_1_5)
            std_dev_above_1_5 = statistics.stdev(above_1_5)
            print(f"Mean: {mean_above_1_5:.2f} ")
            print(f"Standard Deviation: {std_dev_above_1_5:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(above_1_5), max(above_1_5), 100)
            plt.plot(x, norm.pdf(x, mean_above_1_5, std_dev_above_1_5), 'r-', label="Normal Distribution")
            plt.hist(above_1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Above/Equal 1.5 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    # Group 2: Between 1.5 and -1.5
    if between_1_5_minus1_5:
        print("\nBetween 1.5 and -1.5 °C:")
        if len(between_1_5_minus1_5) > 0:
            mean_between = sum(between_1_5_minus1_5) / len(between_1_5_minus1_5)
            std_dev_between = statistics.stdev(between_1_5_minus1_5)
            print(f"Mean: {mean_between:.2f} ")
            print(f"Standard Deviation: {std_dev_between:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(between_1_5_minus1_5), max(between_1_5_minus1_5), 100)
            plt.plot(x, norm.pdf(x, mean_between, std_dev_between), 'r-', label="Normal Distribution")
            plt.hist(between_1_5_minus1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Between 1.5 and -1.5 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    # Group 3: Below or Equal to -1.5
    if below_minus1_5:
        print("\nBelow or Equal to -1.5 °C:")
        if len(below_minus1_5) > 0:
            mean_below_minus1_5 = sum(below_minus1_5) / len(below_minus1_5)
            std_dev_below_minus1_5 = statistics.stdev(below_minus1_5)
            print(f"Mean: {mean_below_minus1_5:.2f} ")
            print(f"Standard Deviation: {std_dev_below_minus1_5:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(below_minus1_5), max(below_minus1_5), 100)
            plt.plot(x, norm.pdf(x, mean_below_minus1_5, std_dev_below_minus1_5), 'r-', label="Normal Distribution")
            plt.hist(below_minus1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Below/Equal -1.5 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")



def calculate_and_plot_graph_hourly_diffs_3group(df, var1, var2):
    """
    Calculates and plots hourly temperature differences with horizontal lines based on 3 groups.
    """
    if df is None:
        print("No Dataframe to plot differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df[diff_var], marker='o', linestyle='-')
    plt.title(f"Hourly Temperature Difference: {var2} - {var1}")
    plt.xlabel("Time")
    plt.ylabel("Temperature Difference (°C)")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add horizontal lines based on 3 groups
    #plt.axhline(0, color='red', linestyle='--', label='0 °C')
    plt.axhline(1.5, color='green', linestyle='--', label='1.5 °C')
    plt.axhline(-1.5, color='blue', linestyle='--', label='-1.5 °C')

    plt.legend() #add legend.
    plt.show()



def calculate_and_print_hourly_diffs_4grouped(df, var1, var2):
 
    if df is None:
        print("No Dataframe to calculate differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    print("Hourly Temperature Differences", var1, "and", var2, "(Grouped):")

    above_1_5 = []
    between_1_5_0 = []
    between_0_minus1_5 = []
    below_minus1_5 = []

    for index, row in df.iterrows():
        diff = row[diff_var]
        if diff >= 1.5:
            above_1_5.append(diff)
        elif 0 <= diff < 1.5:
            between_1_5_0.append(diff)
        elif -1.5 < diff < 0:
            between_0_minus1_5.append(diff)
        elif diff <= -1.5:
            below_minus1_5.append(diff)

    # Group 1: diff >= 1.5
    if above_1_5:
        print("\nAbove or Equal to 1.5 °C:")
        if len(above_1_5) > 0:
            mean_above_1_5 = sum(above_1_5) / len(above_1_5)
            std_dev_above_1_5 = statistics.stdev(above_1_5)
            print(f"Mean: {mean_above_1_5:.2f} ")
            print(f"Standard Deviation: {std_dev_above_1_5:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(above_1_5), max(above_1_5), 100)
            plt.plot(x, norm.pdf(x, mean_above_1_5, std_dev_above_1_5), 'r-', label="Normal Distribution")
            plt.hist(above_1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Above or Equal to 1.5 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    # Group 2: 0 <= diff < 1.5
    if between_1_5_0:
        print("\nBetween equal 0 and -1.50 °C:")
        if len(between_1_5_0) > 0:
            mean_between_1_5_0 = sum(between_1_5_0) / len(between_1_5_0)
            std_dev_between_1_5_0 = statistics.stdev(between_1_5_0)
            print(f"Mean: {mean_between_1_5_0:.2f} ")
            print(f"Standard Deviation: {std_dev_between_1_5_0:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(between_1_5_0), max(between_1_5_0), 100)
            plt.plot(x, norm.pdf(x, mean_between_1_5_0, std_dev_between_1_5_0), 'r-', label="Normal Distribution")
            plt.hist(between_1_5_0, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Between equal 0 and -1.50 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    # Group 3: -1.5 < diff < 0
    if between_0_minus1_5:
        print("\nBetween -1.5 and 0 °C:")
        if len(between_0_minus1_5) > 0:
            mean_between_0_minus1_5 = sum(between_0_minus1_5) / len(between_0_minus1_5)
            std_dev_between_0_minus1_5 = statistics.stdev(between_0_minus1_5)
            print(f"Mean: {mean_between_0_minus1_5:.2f} ")
            print(f"Standard Deviation: {std_dev_between_0_minus1_5:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(between_0_minus1_5), max(between_0_minus1_5), 100)
            plt.plot(x, norm.pdf(x, mean_between_0_minus1_5, std_dev_between_0_minus1_5), 'r-', label="Normal Distribution")
            plt.hist(between_0_minus1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Between -1.5 and 0 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

    # Group 4: diff <= -1.5
    if below_minus1_5:
        print("\nBelow or Equal to -1.5 °C:")
        if len(below_minus1_5) > 0:
            mean_below_minus1_5 = sum(below_minus1_5) / len(below_minus1_5)
            std_dev_below_minus1_5 = statistics.stdev(below_minus1_5)
            print(f"Mean: {mean_below_minus1_5:.2f} ")
            print(f"Standard Deviation: {std_dev_below_minus1_5:.2f} ")

            plt.figure(figsize=(8, 6))
            x = np.linspace(min(below_minus1_5), max(below_minus1_5), 100)
            plt.plot(x, norm.pdf(x, mean_below_minus1_5, std_dev_below_minus1_5), 'r-', label="Normal Distribution")
            plt.hist(below_minus1_5, density=True, alpha=0.6, color='skyblue', label="Temperature Difference")
            plt.title(f"Normal Distribution (Below or Equal to -1.5 °C)")
            plt.xlabel("Temperature Difference (°C)")
            plt.ylabel("Probability Density")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No data in this group to calculate mean and standard deviation")

def calculate_and_plot_graph_hourly_diffs_4group(df, var1, var2):
    """
    Calculates and plots hourly temperature differences with horizontal lines based on 4 groups.
    """
    if df is None:
        print("No Dataframe to plot differences")
        return

    diff_var = f"{var2}_diff_to_{var1}"
    df[diff_var] = df[var2] - df[var1]

    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df[diff_var], marker='o', linestyle='-')
    plt.title(f"Hourly Temperature Difference: {var2} - {var1}")
    plt.xlabel("Time")
    plt.ylabel("Temperature Difference (°C)")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add horizontal lines based on 3 groups
    plt.axhline(0, color='red', linestyle='--', label='0 °C')
    plt.axhline(1.5, color='green', linestyle='--', label='1.5 °C')
    plt.axhline(-1.5, color='blue', linestyle='--', label='-1.5 °C')

    plt.legend() #add legend.
    plt.show()
