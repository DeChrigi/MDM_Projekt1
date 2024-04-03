from flask import Flask, render_template, request
import ChartHandler as ch
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pickle
from pathlib import Path
import numpy as np


load_dotenv()

app = Flask(__name__)

# init app, load model from storage
print("*** Init and load model ***")
if os.getenv("AZURE_STORAGE_CONNECTION_STRING") != None:
    azureStorageConnectionString = os.getenv("AZURE_STORAGE_CONNECTION_STRING") 
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("youtube-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("youtube-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("../model").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "LinearRegressor.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
         download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    print("AZURE_STORAGE_CONNECTION_STRING not set")   

file_path = Path(".", "./", "LinearRegressor.pkl")
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)

def predict_likes(views, comment_count, duration):
    print('OUTPUTOUTPUTOUTPUT2: ', views, comment_count, duration)
    
    # Make prediction using the provided model
    prediction = model.predict(np.array([[views, comment_count, duration]]))
    
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
    app.run(host='0.0.0.0', port="80")