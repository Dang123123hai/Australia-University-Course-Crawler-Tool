# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request
import pandas as pd
from searching import course_tracking
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():
    # Get the user's input from the search bar
    search_degree = request.form['mode_search']
    search_course = request.form['course_search']

    # Load the data as a pandas dataframe (assuming it's in CSV format)
    df = course_tracking(search_degree, search_course)

    # Return the filtered dataframe as HTML
    return df.reset_index(drop=True).to_html()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


