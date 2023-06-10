import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import pairwise_distances

# Enable memory profiling to monitor memory usage
import memory_profiler


# Define a decorator for memory profiling
def profile(func):
    def wrapper(*args, **kwargs):
        # Run the function while monitoring memory usage
        mem_usage_before = memory_profiler.memory_usage()[0]
        result = func(*args, **kwargs)
        mem_usage_after = memory_profiler.memory_usage()[0]

        # Calculate memory usage
        mem_usage = mem_usage_after - mem_usage_before

        # Print memory usage
        print(f"Memory usage: {mem_usage} MB")
        return result

    return wrapper


# Define function for loading preprocessed data
@profile
def load_data():
    recipe_df = pd.read_csv(
        'C:\\capstone project\\data\\preprocessed-data.csv')  # Update the file path to the new preprocessed data
    # Convert cooking directions column to dictionary-like objects
    recipe_df['cooking_directions'] = recipe_df['cooking_directions'].apply(eval)

    return recipe_df


# Load preprocessed data
recipe_data = load_data()


# Define function for creating sparse matrix
@profile
def create_sparse_matrix(recipe_data):
    nutrition = recipe_data[['calories', 'fat', 'carbohydrates', 'protein']]
    nutrition_matrix = csr_matrix(nutrition)
    nutrition_matrix_dense = nutrition_matrix.toarray()
    return nutrition_matrix_dense


# Define function for computing similarity matrix using item-based collaborative filtering
@profile
def compute_similarity_matrix(nutrition_matrix_dense):
    similarity_matrix = pairwise_distances(nutrition_matrix_dense, metric='hamming')
    return similarity_matrix


# Load preprocessed data
recipe_data = load_data()

# Create sparse matrix
nutrition_matrix_dense = create_sparse_matrix(recipe_data)

# Compute similarity matrix
similarity_matrix = compute_similarity_matrix(nutrition_matrix_dense)


def generate_pie_plot(recipe_id):
    recipe = recipe_data.loc[recipe_data['recipe_id'] == recipe_id].iloc[0]
    fat = recipe['fat']
    protein = recipe['protein']
    carbs = recipe['carbohydrates']

    total = fat + protein + carbs

    fat_percentage = (fat / total) * 100
    protein_percentage = (protein / total) * 100
    carbs_percentage = (carbs / total) * 100

    labels = ['Fat', 'Protein', 'Carbohydrates']
    sizes = [fat_percentage, protein_percentage, carbs_percentage]
    explode = (0.1, 0.1, 0.1)  # Explode slices for emphasis

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the pie plot image to a file
    pie_plot_path = f'static/images/pie_plot_{recipe_id}.png'  # Modify the file name as per your requirement
    plt.savefig(pie_plot_path, transparent=True)
    plt.close()  # Close the plot to release memory resources

    return pie_plot_path


# Define function for recipe recommendation
def get_recipe_info(recipe_id, N):
    recipe_id = int(recipe_id)
    # Check if the recipe_id exists in the DataFrame
    if recipe_id not in recipe_data['recipe_id'].values:
        return None

    # Get index of recipe
    idx = recipe_data.loc[recipe_data['recipe_id'] == recipe_id].index

    if len(idx) == 0:
        return None

    idx = idx[0]  # Use the first index if there are multiple matches

    # Compute similarity scores
    similarity_scores = similarity_matrix[idx]
    sorted_indices = np.argsort(similarity_scores)[:N]

    # Retrieve recommended recipes
    recommended_recipes = recipe_data.loc[sorted_indices]

    recipe_info = []
    for i in range(N):
        recipe_name = recommended_recipes.iloc[i]['recipe_name']
        image_url = recommended_recipes.iloc[i]['image_url']
        ingredients_list = recommended_recipes.iloc[i]['ingredients']
        cooking_directions = recommended_recipes.iloc[i]['cooking_directions']

        # Get nutritional information
        calories = recommended_recipes.iloc[i]['calories']
        fat = recommended_recipes.iloc[i]['fat']
        carbohydrates = recommended_recipes.iloc[i]['carbohydrates']
        protein = recommended_recipes.iloc[i]['protein']

        # Extract cook time and prep time from the cooking_directions dictionary
        cook_time = cooking_directions.get('cook', 'N/A')
        prep_time = cooking_directions.get('prep', 'N/A')

        recipe_info.append({
            'recipe_id': recommended_recipes.iloc[i]['recipe_id'],
            'recipe_name': recipe_name,
            'image_url': image_url,
            'ingredients_list': ingredients_list,
            'cooking_directions': cooking_directions,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'calories': calories,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'protein': protein,
            'pie_plot_url': generate_pie_plot(recommended_recipes.iloc[i]['recipe_id'])
        })

    return recipe_info
