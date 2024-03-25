from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
import DBHandler as dbh
import ChartHandler as ch
import pandas as pd

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)