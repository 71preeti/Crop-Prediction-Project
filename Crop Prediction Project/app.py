# from flask import Flask, render_template, request
# import joblib

# app = Flask(__name__)

# # Load the pre-trained crop prediction model
# with open('models/kmeans_model.lb', 'rb') as file:
#     model = joblib.load(file)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     nitrogen = float(request.form['nitrogen'])
#     phosphorus = float(request.form['phosphorus'])
#     potassium = float(request.form['potassium'])
#     temperature = float(request.form['temperature'])
#     humidity = float(request.form['humidity'])
#     ph = float(request.form['ph'])
#     rainfall = float(request.form['rainfall'])

#     # Prepare the input data for the model
#     input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]

#     # Make the prediction
#     prediction = model.predict(input_data)[0]

#     return render_template('result.html', crop=prediction)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request,url_for
import joblib
import pandas as pd
from pymongo import MongoClient


std_scaler= joblib.load('./models/std_scaler.lb')
kmeans_model= joblib.load('./models/kmeans_model.lb')
df=pd.read_csv('./models/filter_crops.csv')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')




# receive data in backened
@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        N=float(request.form['N'])
        PH=float(request.form['PH'])
        P=float(request.form['P'])
        K=float(request.form['K'])
        humidity=float(request.form['humidity'])
        rainfall=float(request.form['rainfall'])
        temperature=float(request.form['temperature'])
        UNSEEN_DATA=[[N,	P	,K	,temperature	,humidity,	PH,	rainfall]]
        transformed_data=std_scaler.transform(UNSEEN_DATA)
        # return UNSEEN_DATA
        cluster=kmeans_model.predict(transformed_data)[0]
        suggestion_crops=list(df[df['cluster_no']==cluster]['label'].unique())
        data={'N':N,	'P':P	,'K':K	,'temperature':temperature	,'humidity':humidity,	'PH':PH,	'rainfall':rainfall}
        data_id=collection.insert_one(data).inserted_id
        print("Your data is inserted into the mongodb , your record id is:",data_id)
        # return f" your suggested crops is {suggestion_crops}"
        return render_template('predict.html',suggestion_crops=suggestion_crops)
    

        # return render_template('predict.html'
        #                        ,suggestion_crops=suggestion_crops )
        # return " your data is transformed"

# mongodb+srv://preet:<preet123>@atlascluster.tjvht.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster


connection_string="mongodb+srv://ancientlearning71:1bp5hNR4YOam3gsL@firstcluster.bp2vi.mongodb.net/?retryWrites=true&w=majority&appName=firstcluster"
client=MongoClient(connection_string)
database=client['Farmer']
collection=database['Farmer Data']


if __name__ == '__main__':
    app.run(debug=True)
