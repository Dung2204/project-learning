import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
def run_Language_Check_app():
# Custom CSS for professional styling
    st.markdown("""
        <style>
        .main-header {
            font-family: 'Arial', sans-serif;
            color: #1E3A8A;
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .section-header {
            font-family: 'Arial', sans-serif;
            color: #3B82F6;
            font-size: 1.5em;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .card {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #3B82F6;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
        }
        .footer {
            text-align: center;
            color: #6B7280;
            font-size: 0.9em;
            margin-top: 30px;
        }
        .stTextArea {
            border: 2px dashed #D1D5DB;
            border-radius: 5px;
            padding: 10px;
        }
        .stSuccess {
            background-color: #E7F3FE;
            color: #1E3A8A;
            border-radius: 5px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # App title
    st.markdown('<div class="main-header">🌐 Language Detection Tool</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Initialize session state
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    if 'cv' not in st.session_state:
        st.session_state.cv = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'result' not in st.session_state:
        st.session_state.result = None

    # Load and train model
    @st.cache_resource
    def train_model():
        try:
            df = pd.read_csv("https://raw.githubusercontent.com/amankharwal/Website-data/master/dataset.csv")
            X = np.array(df["Text"])
            Y = df["language"]

            cv = CountVectorizer()
            X = cv.fit_transform(X)

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=43)

            model = MultinomialNB()
            model.fit(X_train, Y_train)

            Y_pred = model.predict(X_test)
            accuracy = 100 * accuracy_score(Y_pred, Y_test)
            return cv, model, accuracy
        except Exception as e:
            st.error(f"Error training model: {str(e)}")
            return None, None, None

    # Train model if not already trained
    if not st.session_state.model_trained:
        with st.spinner("Training model..."):
            cv, model, accuracy = train_model()
            if cv and model:
                st.session_state.cv = cv
                st.session_state.model = model
                st.session_state.model_trained = True
                st.success(f"Model trained successfully! Accuracy: {accuracy:.2f}%")
            else:
                st.error("Failed to train model!")
                st.stop()

    # Input section
    with st.container():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Enter Text</div>', unsafe_allow_html=True)
            user_input = st.text_area(
                "Enter the text you want to analyze:",
                height=150,
                placeholder="Type or paste your text here..."
            )
            
            if st.button("Detect Language", key="detect_button", help="Click to detect the language"):
                if user_input.strip():
                    try:
                        # Transform input text and predict
                        test = st.session_state.cv.transform([user_input]).toarray()
                        prediction = st.session_state.model.predict(test)[0]
                        st.session_state.result = prediction
                    except Exception as e:
                        st.error(f"Error processing text: {str(e)}")
                else:
                    st.warning("Please enter some text to analyze!")
            st.markdown('</div>', unsafe_allow_html=True)

    # Result section
    if st.session_state.result:
        with st.container():
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Result</div>', unsafe_allow_html=True)
                st.success(f"Detected Language: **{st.session_state.result}**")
                if st.button("Clear Result", key="clear_button", help="Clear the result and enter new text"):
                    st.session_state.result = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="footer">Language Detection App - Powered by xAI</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    run_Language_Check_app()
