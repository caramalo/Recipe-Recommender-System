from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from recommend_function import create_sparse_matrix, compute_similarity_matrix, get_recipe_info, generate_pie_plot
import pandas as pd

app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Set a secret key for session encryption
bcrypt = Bcrypt(app)

# Load preprocessed data
recipe_data = pd.read_csv('C:\\capstone project\\data\\preprocessed-data.csv')

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    favorite_recipes = db.relationship('Recipe', secondary='user_favorite_recipes', backref='users_favorited')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    favorited_by = db.relationship('User', secondary='user_favorite_recipes', backref='recipes_favorited')


user_favorite_recipes = db.Table('user_favorite_recipes',
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                 db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
                                 )


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
    if 'username' in session:
        # User is already logged in, redirect to the recipe filter
        return redirect(url_for('recipe_filter'))

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

    return render_template('home.html', logged_in=False)


@app.route('/recipe-filter', methods=['GET', 'POST'])
def recipe_filter():
    if 'username' not in session:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

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

    return render_template('recipe_filter.html')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        # User is already logged in, redirect to the recipe filter
        return redirect(url_for('recipe_filter'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username  # Store the username in the session
        return redirect(url_for('recipe_filter'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # User is already logged in, redirect to the recipe filter
        return redirect(url_for('recipe_filter'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username  # Store the username in the session
            return redirect(url_for('recipe_filter'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'username' not in session:
        # User is not logged in
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()
    print(user)  # check the user object

    if user:
        favorite_recipes = user.favorite_recipes
        print(favorite_recipes)

        return render_template('profile.html', username=username, favorite_recipes=favorite_recipes)

    return redirect(url_for('login'))


@app.route('/favorite', methods=['POST'])
def favorite():
    if 'username' not in session:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    recipe_id = int(request.form['recipeId'])
    username = session['username']

    print(f"Received favorite request for recipe ID: {recipe_id}")
    print(f"Username: {username}")

    user = User.query.filter_by(username=username).first()
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe is not None and user is not None:
        user.favorite_recipes.append(recipe)
        db.session.commit()
        flash('Recipe added to favorites!', 'success')

    print("Favorite Recipes:")
    print(user.favorite_recipes)

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
