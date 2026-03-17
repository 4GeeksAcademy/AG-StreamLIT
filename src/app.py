#-------------Librerias------------

import pickle
import pandas as pd
from flask import Flask, render_template, request


#=============Flask=================

app=Flask(__name__)

#Cargar el modelo
model=pickle.load(open("src/model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    platforms = request.form["platforms"]
    publishers = request.form["publishers"]
    releaseyear = int(request.form["releaseyear"])

    input_data = pd.DataFrame([{
        "platforms": platforms,
        "publishers": publishers,
        "releaseyear": releaseyear
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        result = "Top Seller 🎮🔥"
    else:
        result = "Not a Top Seller"

    return render_template("index.html", prediction_text=result)

if __name__ == "__main__":
    app.run(debug=True)
