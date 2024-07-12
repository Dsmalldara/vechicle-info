import pandas as pd
import numpy as np
from faker import Faker

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
# Initializing Faker 
fake = Faker()

# Lists of possible car attributes
makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Tesla', 'BMW', 'Mercedes', 'Audi', 'Hyundai', 'Kia']
models = {
    'Toyota': ['Corolla', 'Camry', 'Prius', 'Highlander'],
    'Honda': ['Accord', 'Civic', 'CR-V', 'Fit'],
    'Ford': ['Fusion', 'Mustang', 'Explorer', 'F-150'],
    'Chevrolet': ['Malibu', 'Impala', 'Tahoe', 'Silverado'],
    'Tesla': ['Model S', 'Model 3', 'Model X', 'Model Y'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5'],
    'Mercedes': ['C-Class', 'E-Class', 'GLC', 'GLE'],
    'Audi': ['A3', 'A4', 'Q5', 'Q7'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Optima', 'Soul', 'Sportage', 'Sorento']
}
engine_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric']
transmissions = ['Manual', 'Automatic']
conditions = ['New', 'Used']
accidents = ['No', 'Yes']
service_types = ['Oil Change', 'Brake Repair', 'Transmission Fix', 'Battery Replacement']
symptoms = ['Strange noise in engine', 'Poor acceleration', 'Battery issues', 'Brake issues', 'Overheating']
warning_lights = ['Check Engine Light', 'ABS Warning Light', 'Battery Warning Light', 'Brake Warning Light']

#  dummy owner info
owners = []
for _ in range(50):
    owners.append({
        'Name': fake.name(),
        'Phone Number': fake.phone_number(),
        'Email': fake.email(),
        'Address': fake.address()
    })
owners_df = pd.DataFrame(owners)

#  dummy vehicle info
vehicles = []
for owner in owners:
    make = np.random.choice(makes)
    model = np.random.choice(models[make])
    vehicles.append({
        'Owner': owner['Name'],
        'Make': make,
        'Model': model,
        'Year': np.random.randint(2010, 2023),
        'Engine Type': np.random.choice(engine_types),
        'Transmission': np.random.choice(transmissions),
        'Mileage': np.random.randint(5000, 200000),
        'Purchase Date': fake.date_between(start_date='-10y', end_date='today'),
        'Condition': np.random.choice(conditions),
        'Previous Accidents': np.random.choice(accidents)
    })
vehicles_df = pd.DataFrame(vehicles)

# service hist
service_history = []
for owner in owners:
    for _ in range(np.random.randint(1, 5)):
        service_history.append({
            'Owner': owner['Name'],
            'Service Date': fake.date_between(start_date='-5y', end_date='today'),
            'Service Type': np.random.choice(service_types),
            'Parts Replaced': np.random.choice(['Oil Filter', 'Brake Pads', 'Transmission Fluid', 'Battery', 'Spark Plugs', 'Conductors'])
        })
service_history_df = pd.DataFrame(service_history)

# vehicle condition
current_condition = []
for owner in owners:
    current_condition.append({
        'Owner': owner['Name'],
        'Symptoms': np.random.choice(symptoms),
        'Warning Lights': np.random.choice(warning_lights),
        'Last Service Date': fake.date_between(start_date='-2y', end_date='today')
    })
current_condition_df = pd.DataFrame(current_condition)

#  usage patterns
usage_patterns = []
for owner in owners:
    usage_patterns.append({
        'Owner': owner['Name'],
        'Avg Monthly Mileage': np.random.randint(500, 3000),
        'Driving Conditions': np.random.choice(['City', 'Highway', 'Mixed']),
        'Primary Use': np.random.choice(['Personal', 'Commercial'])
    })
usage_patterns_df = pd.DataFrame(usage_patterns)

# Combine all data into a dictionary
data = {
    'Owners': owners_df,
    'Vehicles': vehicles_df,
    'Service History': service_history_df,
    'Current Condition': current_condition_df,
    'Usage Patterns': usage_patterns_df
}

# Save the data to CSV files
for key, df in data.items():
    df.to_csv(f'{key.lower().replace(" ", "_")}.csv', index=False)

print("Data generation complete and saved to CSV files.")

#reading the data set from  the csv file
owners = pd.read_csv('owners.csv')
vehicles = pd.read_csv('vehicles.csv')
servicehist = pd.read_csv('service_history.csv')
current_condition = pd.read_csv('current_condition.csv')
usage_patterns = pd.read_csv('usage_patterns.csv')

#combining all data frames together

combined_data = pd.merge(owners, vehicles, left_on='Name', right_on='Owner')
combined_data = pd.merge(combined_data, servicehist, on='Owner')
combined_data = pd.merge(combined_data,current_condition, on='Owner')
combined_data = pd.merge(combined_data, usage_patterns, on='Owner')

#check for duplicates
duplicate_mask = combined_data.duplicated(subset=['Name', 'Phone Number', 'Email', 'Address'])


cleaned_data = combined_data[~duplicate_mask]


#  service counts for various  types of services done on all vehicles
service_frequency = servicehist['Service Type'].value_counts()
print(service_frequency)



# sns.scatterplot(data=combined_data, x='Mileage', y='Avg Monthly Mileage')
# plt.title('Correlation Between Mileage and Average Monthly Mileage')
# plt.show()
sns.lmplot(data=combined_data, x='Mileage', y='Avg Monthly Mileage', line_kws={'color': 'red'})
plt.title('Correlation Between Mileage and Average Monthly Mileage with Trend Line')
plt.show()



sns.boxplot(data=combined_data, x='Driving Conditions', y='Mileage')
plt.title('Impact of Driving Conditions on Mileage')
plt.show()


sns.boxplot(data=combined_data, x='Primary Use', y='Mileage')
plt.title("Correlation between Primary Use and Mileage")
plt.show()  


# Impact of Previous Accidents on Mileage
sns.barplot(data=combined_data, x='Previous Accidents', y='Mileage')
plt.title('Impact of Previous Accidents on Mileage')
plt.show()

# Age of Vechicle vs Frequency of Service
combined_data['dateof_purchase'] = pd.to_datetime(combined_data['Purchase Date'])
combined_data['yearof_purchase'] = combined_data['dateof_purchase'].dt.year
combined_data['vehicle_year'] = 2024 - combined_data['yearof_purchase'] 
sns.boxplot(data=combined_data, x='vehicle_year', y='Service Type')
plt.title('Vechicle age vs frequency of service')
plt.xlabel('Age of Vehicle')
plt.ylabel('Frequency of Service')
plt.show()



#  Correlation between Engine type and Service Type
sns.barplot(data=combined_data, x='Engine Type', y='Service Type')
plt.title('Engine type vs Service Type ')
plt.xlabel('Engine Type ')
plt.ylabel('Service Type')
plt.show()
            


# correlation between primary use and part replaced

sns.countplot(data=combined_data, x='Parts Replaced', hue='Primary Use')
plt.title('Primary Use vs. Parts Replaced')
plt.xlabel('Parts Replaced')
plt.ylabel('Count')
plt.show()


# comparision between  Transmission and mileage

sns.boxplot(data=combined_data, x='Transmission', y='Mileage')
plt.title('Comparing Transmission type of vechicle owners and Mileage')
plt.xlabel('Transmission')
plt.ylabel('Mileage')
plt.show()


# Creating the boxplot for Condition of vehicle and Mileage
plt.figure(figsize=(10, 6))
sns.boxplot(data=combined_data, x='Condition', y='Mileage')
plt.title('Comparing Vehicle Condition and Mileage')
plt.xlabel('Condition')
plt.ylabel('Mileage')
plt.show()

# Plotting 
sns.countplot(data=combined_data, x='Service Type', hue='Warning Lights')
plt.title('Service Type vs. Warning Lights')
plt.xlabel('Service Type')
plt.ylabel('Count')
plt.show()
