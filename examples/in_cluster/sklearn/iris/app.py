import streamlit as st
import pandas as pd
import joblib
import argparse

from PIL import Image


def load_model(model_path: str):
    model = open(model_path, "rb")
    return joblib.load(model)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-path',
        type=str,
    )
    args = parser.parse_args()

    setosa = Image.open("images/iris-setosa.png")
    versicolor = Image.open("images/iris-versicolor.png")
    virginica = Image.open("images/iris-virginica.png")
    classifier = load_model(args.model_path)
    print(classifier)

    st.title("Iris flower species Classification")
    st.sidebar.title("Features")
    parameter_list = [
        "Sepal length (cm)",
        "Sepal Width (cm)",
        "Petal length (cm)",
        "Petal Width (cm)"
    ]
    sliders = []
    for parameter, parameter_df in zip(parameter_list, ['5.2', '3.2', '4.2', '1.2']):
        values = st.sidebar.slider(
            label=parameter,
            key=parameter,
            value=float(parameter_df),
            min_value=0.0,
            max_value=8.0,
            step=0.1
        )
        sliders.append(values)

    input_variables = pd.DataFrame([sliders], columns=parameter_list)

    prediction = classifier.predict(input_variables)
    if prediction == 0:
        st.image(setosa)
    elif prediction == 1:
        st.image(versicolor)
    else:
        st.image(virginica)

