from flask import Flask, render_template, request
from recommend_function import create_sparse_matrix, compute_similarity_matrix, get_recipe_info, generate_pie_plot
import pandas as pd

app = Flask(__name__)
app = Flask(__name__, static_folder='static')

# Load preprocessed data
recipe_data = pd.read_csv('C:\\capstone project\\data\\preprocessed-data.csv')

# Create sparse matrix
nutrition_matrix_dense = create_sparse_matrix(recipe_data)

# Compute similarity matrix
similarity_matrix = compute_similarity_matrix(nutrition_matrix_dense)


def filter_recipes(calories_min, calories_max, ingredient_type, recipe_data):
    # Apply filters to the recipe_data DataFrame
    filtered_recipes = recipe_data[
        (recipe_data['calories'] >= calories_min) &
        (recipe_data['calories'] <= calories_max) &
        (recipe_data['ingredients'].str.contains(ingredient_type, case=False))
        ]

    if not filtered_recipes.empty:
        # Check if 'pie_plot_url' column exists
        if 'pie_plot_url' not in filtered_recipes.columns:
            # Generate the pie plot URL for each recipe and add it to the DataFrame
            filtered_recipes.loc[:, 'pie_plot_url'] = filtered_recipes['recipe_id'].apply(generate_pie_plot)

        recipes_list = filtered_recipes.to_dict(orient='records')
        return pd.DataFrame(recipes_list)  # Return DataFrame when recipes match the filters

    return pd.DataFrame()  # Return an empty DataFrame when no recipes match the filters


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        calories_min = int(request.form['calories_min'])
        calories_max = int(request.form['calories_max'])
        ingredient_type = request.form['ingredient_type']
        filtered_recipes = filter_recipes(
            calories_min, calories_max, ingredient_type, recipe_data)
        if not filtered_recipes.empty:
            recipes_list = filtered_recipes.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
            return render_template('recipes.html', recipes=recipes_list)
        else:
            return render_template('recipes.html', recipes=None)
    return render_template('home.html')


@app.route('/recommendations', methods=['GET'])
def recommendations():
    recipe_id = request.args.get('recipe_id')
    num_recommendations = request.args.get('num_recommendations')

    if num_recommendations is not None:
        num_recommendations = int(num_recommendations)
    else:
        num_recommendations = 5  # Default value if num_recommendations is not specified

    # Call the get_recipe_info function to get recommendations
    recommended_recipes = get_recipe_info(recipe_id, num_recommendations)

    # Render the recommendations.html template with the recommended recipes
    return render_template('recommendations.html', recipe_info=recommended_recipes)


@app.route('/recipes')
def recipes():
    recipe_id = request.args.get('recipe_id')
    N = int(request.args.get('N', 5))

    # Retrieve recipe information
    recipe_info = get_recipe_info(recipe_id, N)

    # Render the template with recipe information
    return render_template('recipe_details.html', recipe_info=recipe_info)


if __name__ == '__main__':
    app.run()