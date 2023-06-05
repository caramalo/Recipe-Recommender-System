import pandas as pd

import ast  # used to convert the string representation of the dictionary to a dictionary object

from sklearn.preprocessing import normalize

# Read the raw recipe data from a CSV file into a DataFrame
recipe_data = pd.read_csv("C:\\capstone project\\data\\raw-data_recipe_1000.csv")


# Define a function to round the average rate to 2 decimal places
def average_rate(col):
    return f'{col:.2f}'


# Apply the average_rate function to the aver_rate column and convert it to float type
recipe_data.aver_rate = recipe_data.aver_rate.apply(average_rate)
recipe_data.aver_rate = recipe_data.aver_rate.astype(float)

# Convert the string representation of dictionaries in the nutritions column to actual dictionary objects
list_dictionaries = []
for row in recipe_data.nutritions:
    list_dictionaries.append(ast.literal_eval(row))

# Extract specific nutritional values from the dictionaries
calories_list = []
fat_list = []
carbohydrates_list = []
protein_list = []
for x in range(len(list_dictionaries)):
    calories_list.append(list_dictionaries[x]['calories']['displayValue'])
    fat_list.append(list_dictionaries[x]['fat']['displayValue'])
    carbohydrates_list.append(list_dictionaries[x]['carbohydrates']['displayValue'])
    protein_list.append(list_dictionaries[x]['protein']['displayValue'])

# Create a new DataFrame with the extracted nutritional values
data = {'calories': calories_list, 'fat': fat_list, 'carbohydrates': carbohydrates_list, 'protein': protein_list}
df = pd.DataFrame(data)

# Set the index of the DataFrame to the recipe_id column from recipe_data and drop rows with missing values
df.index = recipe_data['recipe_id']
df = df.dropna()


# Define a function to clean text values, replacing '< 1' with 1
def text_cleaning(cols):
    if cols == '< 1':
        return 1
    else:
        return cols


# Apply text_cleaning function to each column and convert them to numeric type
for col in df.columns:
    df[col] = df[col].apply(text_cleaning)
df = df.apply(pd.to_numeric)

# Normalize the nutrition data using sklearn's normalize function
df_normalized = pd.DataFrame(normalize(df, axis=0))
df_normalized.columns = df.columns
df_normalized.index = df.index

# Merge the recipe_data DataFrame with the normalized nutrition data
recipe_final = pd.merge(recipe_data, df, on='recipe_id')
recipe_final = recipe_final.drop(columns=['nutritions'])

# Print the head of the final DataFrame
print(recipe_final.head())

# Save the final DataFrame to a CSV file
recipe_final.to_csv("C:\\capstone project\\data\\preprocessed-data.csv", index=False)
