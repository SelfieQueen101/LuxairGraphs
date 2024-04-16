import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def load_data(filepath):
    """Load and preprocess the data from a CSV file."""
    data = pd.read_csv(filepath, delimiter=',', skiprows=1, nrows=50)
    data['satisfaction'] = data['Overall, how satisfied were you with your flight experience?']
    data['travel_group'] = data['persona']
    satisfaction_mapping = {
        'Very unsatisfied': 1,
        'Unsatisfied': 2,
        'Neutral': 3,
        'Satisfied': 4,
        'Very satisfied': 5
    }
    data['satisfaction_score'] = data['satisfaction'].map(satisfaction_mapping)
    return data

def calculate_group_satisfaction(data):
    """Group data by travel group and calculate average satisfaction."""
    return data.groupby('travel_group').agg(
        average_satisfaction=('satisfaction_score', 'mean'),
        count=('satisfaction_score', 'count')
    ).reset_index()

def plot_satisfaction(grouped_data):
    """Create and display a bar graph for customer satisfaction by travel group."""
    plt.figure(figsize=(8, 6))
    plt.bar(grouped_data['travel_group'], grouped_data['average_satisfaction'], color='skyblue')
    plt.xlabel('Travel Group')
    plt.ylabel('Average Satisfaction Score')
    plt.title('Customer Satisfaction by Travel Group')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Main program
data = load_data("luxair_convert.csv")

# Calculate and plot average satisfaction by travel group
grouped_satisfaction = calculate_group_satisfaction(data)
plot_satisfaction(grouped_satisfaction)

# Display the data table including satisfaction scores
st.write(grouped_satisfaction)


##############################################
### VISUALISATION 2 ##########################
##############################################
# Count occurrences of improvement areas


# Count occurrences of improvement areas
# Select only the columns related to improvement areas
improvement_columns = ['Overall, how satisfied were you with the Check-In process at the airport counter',
                       'Overall, how satisfied were you with the boarding process?',
                       'Overall, how satisfied were you with your flight experience?']

# Count satisfied and unsatisfied responses for each improvement area
unsatisfactory_rates = {}
for column in improvement_columns:
    unsatisfied_count = (data[column] == 'Unsatisfied') | (data[column] == 'Very unsatisfied')
    total_count = unsatisfied_count | (data[column] == 'Satisfied') | (data[column] == 'Very satisfied')
    unsatisfactory_rates[column] = unsatisfied_count.sum() / total_count.sum()

# Create DataFrame from the unsatisfactory rates
unsatisfactory_df = pd.DataFrame(unsatisfactory_rates.values(), index=unsatisfactory_rates.keys(), columns=['Unsatisfactory Rate'])

# Plot the visualization
plt.figure(figsize=(8, 8))
plt.pie(unsatisfactory_rates.values(), labels=unsatisfactory_rates.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Unsatisfactory Rate by Service Area')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
st.pyplot(plt)

##############################################
### VISUALISATION 3 ##########################
##############################################
def calculate_location_satisfaction(data):
    """Group data by arrival location and calculate average satisfaction."""
    return data.groupby('arrival_airport').agg(
        average_satisfaction=('satisfaction_score', 'mean')
    ).reset_index()

def plot_location_satisfaction(grouped_data):
    """Create and display a bar graph for customer satisfaction by arrival location."""
    # Sort the grouped data by average satisfaction score
    sorted_data = grouped_data.sort_values(by='average_satisfaction', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data['arrival_airport'], sorted_data['average_satisfaction'], color='skyblue')
    plt.xlabel('Arrival Location')
    plt.ylabel('Average Satisfaction Score')
    plt.title('Customer Satisfaction by Arrival Location')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Main program
data = load_data("luxair_convert.csv")  # Limiting to the first 50 rows

# Calculate and plot average satisfaction by arrival location
location_satisfaction = calculate_location_satisfaction(data)
plot_location_satisfaction(location_satisfaction)

# Display the data table including average satisfaction scores
st.write(location_satisfaction)