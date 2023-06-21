# Recipe Recommender System User Guide

## 1. General Information
- **Title**: Recipe Recommender System User Guide

## 2. Title Page and Copyright Page
- **Title**: Recipe Recommender System User Guide
- **Edition**: 1.1
- **Date**: 6/11/2023

## 3. Preface
Welcome to the Recipe Recommender System User Guide! This guide is designed to help you navigate and make the most of our recipe recommender system. Whether you're a cooking enthusiast or looking for culinary inspiration, this system will provide personalized recipe recommendations based on your preferences. This user guide outlines the system's features, provides step-by-step instructions, and offers troubleshooting assistance. We hope this guide enhances your experience and encourages you to explore the world of delicious recipes!

## 4. Table of Contents
1. General Information
2. System Summary
3. Getting Started
4. Using the System
5. Troubleshooting
6. FAQ
7. Help/Contact Me

## 5. General Information
The Recipe Recommender System is a web-based application that helps users discover and explore various recipes based on their preferences and dietary requirements. The system uses a combination of user-selected filters and advanced algorithms to generate personalized recipe recommendations. By leveraging nutritional information, images, and user ratings, the system aims to provide a seamless and delightful recipe discovery experience.

## 6. System Summary
The Recipe Recommender System consists of a Flask web application. The system allows users to filter recipes based on criteria such as caloric restrictions and ingredient selection. It also provides nutritional information, cooking directions, and user ratings for each recipe. The system utilizes machine learning techniques to analyze user preferences and generate tailored recipe recommendations.

## 7. Getting Started
To access the Recipe Recommender System, follow these steps:
- Visit [https://reevepaul.pythonanywhere.com/](https://reevepaul.pythonanywhere.com/).
- Explore the homepage and use the search functionality to filter recipes based on user preferences. Additionally, consider registering and logging in. Once registered and logged in, a unique profile will be created for the user in which they can store their favorite recipes.
- Customize the filters to narrow down the recipe results according to the user's preference. If recipes that match the user's criteria exist in the database, then they will be shown to the user. The user can then select a recipe from the choices provided, and full information regarding that selected recipe and recommendations for four other recipes will be shown.

## 8. Using the System
- Navigating the User Interface:
  - The system's user interface is designed to be intuitive and user-friendly.
  - The homepage displays search filter options to assist in finding an initial recipe that the user may like, along with login and register functionalities.
- Registering a new account:
  - In the initial landing page, select the register button. Then simply provide a username and password to create an account.
- Login:
  - If the user is previously registered, then they just have to select the login option and input the appropriate credentials to access their profiles.
- Searching and Filtering Recipes:
  - Use the search bar to set values for the minimum and maximum calorie requirements. In the ingredients field, input an ingredient that you want in the recipe, such as beef, chicken, fish, etc.
  - Click on submit and select a recipe from the options given. If none of the options are appealing, the user can return to the recipe filter page to adjust the criteria.
- Viewing Recipe Details and Recommendations:
  - After selecting a recipe, the system displays detailed information about the recipe, such as nutritional composition, ingredients, cooking directions, and a graphical representation of the dish.
  - Users can also favorite recipes and save them to their user profiles.
  - Additionally, the system recommends four additional recipes that the user might like. These recommendations also include nutritional composition, ingredients, cooking directions, graphical representations, and the option to favorite and save recipes to the user profile.

## 9. Troubleshooting
- Login Issues:
  - Make sure you are using the correct username and password combination.
  - Check if the Caps Lock key is accidentally enabled, as passwords are case-sensitive.
  - Clear your browser cache and try logging in again.
- Recipe Filtering Issues:
  - Double-check if you have entered the minimum and maximum calories correctly.
  - Ensure that the ingredient type you entered is valid and matches the available options.
- Recipe Recommendations Issues:
  - If the recommended recipes do not match your preferences, try adjusting the criteria or preferences and refresh the page.

## 10. FAQ
- What is the purpose of this web application?
  - This web application is designed to help users filter and search for recipes based on specific criteria such as calorie range and ingredient type. It also provides recommendations and allows users to save their favorite recipes. This application is meant to help users more easily find recipes that suit their preferences and lifestyles.
- How does the recipe recommendation system work?
  - To provide personalized recipe recommendations, this project incorporates two powerful techniques: item-based collaborative filtering and Hamming distance.
    Item-based collaborative filtering focuses on finding similarities between recipes rather than users. By analyzing the behavior and preferences of users who have interacted with certain recipes, the system builds a similarity matrix. This matrix measures the similarity between pairs of recipes using techniques like cosine similarity, Pearson correlation, Hamming distance, etc. This allows the system to identify recipes that share similarities and recommend them to users based on their previous interactions. By leveraging the preferences of similar users, item-based collaborative filtering provides personalized recommendations that align with a user's taste.

## 11. Help/Contact Me
You can contact me via email at reeve.pauls@gmail.com.

-------------------------------------------------------------

# System Administration Guide: Recipe Recommender System

## 1. Cover Page
- **Title**: Recipe Recommender System Administration Guide

## 2. Title Page and Copyright Page
- **Title**: Recipe Recommender System Administration Guide
- **Edition**: 1.0
- **Date**: 6/11/2023

## 3. Table of Contents
- System Overview
- System Configuration
- System Maintenance
- Security Related Processes

## 4. System Overview
- **Flask Setup**:
  - The Flask app is created using `Flask(__name__)`.
  - Flask-Bcrypt is used for password hashing.
  - SQLAlchemy is used for database management.
  - Flask-Migrate is used for database migrations.
- **Database Models**:
  - The User model represents a user and has attributes like id, username, password, and favorite_recipes.
  - The Recipe model represents a recipe and has attributes like id, recipe_name, image_url, and favorited_by.
  - There is a many-to-many relationship between users and recipes through the user_favorite_recipes table.
- **Helper Functions**:
  - `filter_recipes`: Filters the recipe data based on user-specified criteria like minimum and maximum calories and ingredient type.
- **Routes**:
  - `/`: Renders the home page with a form to filter recipes or redirects to the recipe filter page if the user is already logged in.
  - `/recipe-filter`: Renders the recipe filter page with a form to filter recipes based on criteria.
  - `/recommendations`: Renders a page with recommended recipes based on a given recipe ID and number of recommendations.
  - `/recipes`: Renders the details of a specific recipe based on the recipe ID.
  - `/register`: Handles user registration with a form to create a new account.
  - `/login`: Handles user login with a form for username and password authentication.
  - `/profile`: Renders the user's profile page with their favorite recipes.
  - `/favorite`: Adds a recipe to the user's favorites list.
  - `/logout`: Clears the user session and redirects to the home page.
- **Recommendation Functions**:
  - `generate_pie_plot`: Generates a pie plot image for a recipe based on its nutritional information.
  - `get_recipe_info`: Retrieves recommended recipes based on a given recipe ID and the similarity matrix.
- **Preprocessed Data and Matrix Computation**:
  - The preprocessed data is loaded from the CSV file `preprocessed-data.csv`.
  - The data is transformed into a sparse matrix using the `create_sparse_matrix` function.
  - The similarity matrix is computed using item-based collaborative filtering and the `compute_similarity_matrix` function.
- **Additional Dependencies**:
  - The system relies on the Pandas, NumPy, Matplotlib, and PIL (Pillow) libraries for data manipulation, array operations, plotting, and image processing.
  - The `urllib.request` module is used for handling image URLs.

## 5. System Configuration
- This system is deployed using [pythonAnywhere.com](https://www.pythonanywhere.com/). The steps are as follows:
  - Create a new web app on PythonAnywhere:
    - Go to the "Web" tab in the PythonAnywhere dashboard.
    - Click on "Add a new web app."
    - Select "Flask" as the web framework.
    - Choose the Python version (e.g., 3.11).
    - Click "Next" to proceed.
    - Enter a name for your web app (e.g., "my-flask-app").
    - Choose the option "Manual Configuration."
    - Click "Next" to create the web app.
  - Set up the virtual environment:
    - In the "Virtualenv" section, select the option "Enter the path to a virtualenv."
    - Enter the path to the virtual environment for the Flask app (e.g., "/home/your-username/my-flask-app/venv").
    - Click "Next" to continue.
  - Configure the WSGI file:
    - In the "WSGI configuration file" section, click on the link to edit the WSGI file.
    - Replace the existing code in the file with the following:
      ```python
      import sys
      path = '/home/your-username/my-flask-app'  # Replace with the path to your Flask app
      if path not in sys.path:
          sys.path.append(path)
      
      from app import app as application
      ```
    - Save the changes and close the file editor.
  - Upload the Flask app files:
    - In the "Code" section, open the file browser.
    - Upload all the files and directories of the Flask app to the root directory of the web app.
    - Make sure to include the following files and directories:
      1. `app.py` (the main Flask app file)
      2. `templates/` (directory containing HTML templates)
      3. `static/` (directory containing static files, such as CSS and images)
  - Install dependencies:
    - Open a command line interface in PythonAnywhere and navigate to the root directory of the web app (e.g., "/home/your-username/my-flask-app").
    - Activate the virtual environment by running the command: `source venv/bin/activate`.
    - Install the dependencies by running the command: `pip install -r requirements.txt`.
  - Configure the database:
    - Update the Flask app in PythonAnywhere appropriately to interact with databases.
  - Start the web application.

## 6. System Maintenance
- The web application's source code, configuration files, and associated database should be backed up regularly.
- Stay up to date with the latest version of Flask and all other dependencies used in the application.

## 7. Security Related Processes
- **Authentication and Access Control**:
  - Implement secure authentication mechanisms to protect user accounts and sensitive data.
  - Utilize secure password storage techniques, such as hashing, to store user passwords.
  - Enforce strong password policies, including password complexity requirements and regular password resets.
- **Security Updates and Patches**:
  - Stay informed about the latest security vulnerabilities and updates related to Flask and its dependencies.
  - Regularly update the Flask framework, libraries, and components used in the application to address any potential security vulnerabilities.
