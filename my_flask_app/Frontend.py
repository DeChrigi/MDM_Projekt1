from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.io as pio
import DBHandler as dbh
import ChartHandler as ch
import pandas as pd
import ModelHandler

app = Flask(__name__)

def predict_likes(views, comment_count, duration):
    # Prepare the input features as a numpy array
    
    # Make prediction using the provided model
    prediction = ModelHandler.predict(views, comment_count, duration)
    
    return prediction[0]  # Extract the predicted value from the array

@app.route('/charts')
def charts():
    countByCategoryPlot = ch.getCountByCategoryPlot()

    avgViewsByCategoryPlot = ch.getAvgViewsByCategoriesPlot()
    
    avgLikesByCategoryPlot = ch.getAvgLikesByCategoriesPlot()

    avgCommentsByCategoryPlot = ch.getAvgCommentsByCategoriesPlot()

    return render_template('charts.html', countByCategoryPlot=countByCategoryPlot, avgViewsByCategoryPlot=avgViewsByCategoryPlot, avgLikesByCategoryPlot=avgLikesByCategoryPlot, avgCommentsByCategoryPlot=avgCommentsByCategoryPlot)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':

        # Protokollieren des POST-Request
        app.logger.info('Received POST request with data: %s', request.form)
        
        # Holen der Eingabewerte aus dem Formular
        views = int(request.form['views'])
        comment_count = int(request.form['comment_count'])
        duration = int(request.form['duration'])

        print('OUTPUTOUTPUTOUTPUT: ', views, comment_count, duration)
        
        # Vorhersage der Likes mit dem trainierten Modell
        # Übergeben Sie die korrekten Argumente an die predict_likes Funktion
        predicted_likes = predict_likes(views, comment_count, duration)
        
        # Rendern des result.html Templates und Übergeben des vorhergesagten Wertes
        return render_template('index.html', predicted_likes=predicted_likes)


if __name__ == '__main__':
    app.run(debug=True)