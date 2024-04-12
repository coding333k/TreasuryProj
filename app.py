from flask import Flask, render_template,url_for, request, jsonify, send_file
import util
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import io

# this just references this file
app = Flask(__name__)

def plot_curves_simple(df):
    """
    Plots the Discrete Par Curve and Zero Curve from the given DataFrame.
    
    Parameters:
        df (DataFrame): DataFrame containing the data to plot.
    """
    # Plot the curves with seaborn
    plt.figure(figsize=(10, 6))

    # Discrete Par Curve
    sns.scatterplot(data=df, x='Months', y='Yields_4_1', color='blue', label='Discrete Par')

    # Zero Curve
    sns.lineplot(data=df, x='Months', y='Zero41', color='red', label='Zero Curve')

    # Set plot title and labels
    plt.title('Discrete Par Curve and Zero Curve')
    plt.xlabel('Months')
    plt.ylabel('Rate')
    plt.ylim(0, max(df['Yields_4_1']) + 0.01)
    plt.grid(True)
    plt.legend()

    # Save the plot to a file
    plot_path = 'static/plot.png'  # Save the plot image in the 'static' folder
    plt.savefig(plot_path)

    return plot_path

@app.route("/")
def index():
    # Read the JSON file into a DataFrame
    df = pd.read_json('models/yield_curves.json')

    # Call the method to generate the plot and get the plot path
    plot_path = plot_curves_simple(df)

    # Render the HTML template and pass the plot image path to it
    return render_template('index.html', plot_path=plot_path)

@app.route("/download_csv")
def download_csv():
    # Read the JSON file into a DataFrame
    df = pd.read_json('models/yield_curves.json')
    
    # Convert the DataFrame to a CSV string
    csv_string = df.to_csv(index=False)
    
    # Create an in-memory file-like object in binary mode
    csv_io = io.BytesIO()
    csv_io.write(csv_string.encode())
    csv_io.seek(0)
    
    # Return the CSV file as an attachment with the specified download name
    return send_file(csv_io, as_attachment=True, download_name='yield_curves.csv', mimetype='text/csv')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)