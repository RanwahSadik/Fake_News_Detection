import streamlit as st
import joblib
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import contractions

# Load necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the saved model and vectorizer
model = joblib.load("svm_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Function to preprocess user input text
def text_preprocessing(text):
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    tokens = word_tokenize(text.lower())  # Tokenization & lowercase
    stop_words = set(stopwords.words('english'))  
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatization
    expanded_text = contractions.fix(" ".join(tokens))  # Expand contractions
    return " ".join(word_tokenize(expanded_text))  # Tokenize again & return

# Streamlit UI
st.title("Fake News Detection App 📰")
st.subheader("Enter a news article to check if it's real or fake")

user_input = st.text_area("Enter news text here:")

if st.button("Predict"):
    if user_input.strip():
        # Preprocess the user input text
        processed_text = text_preprocessing(user_input)
        # Transform the text to the vector space
        text_vectorized = vectorizer.transform([processed_text])
        # Predict using the pre-trained model
        prediction = model.predict(text_vectorized)[0]

        # Output prediction
        if prediction == 1:
            st.success("✅ This news appears to be **REAL**!")
        else:
            st.error("❌ This news might be **FAKE**!")
    else:
        st.warning("⚠️ Please enter some text to analyze.")
