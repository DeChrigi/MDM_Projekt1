import my_flask_app.ApiHandler as ap
import my_flask_app.DBHandler as db
import pandas

df = db.getMostPopularVideosByCountryAll()

print(df)
