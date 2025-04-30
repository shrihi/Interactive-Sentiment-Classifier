# 🎯 Interactive Sentiment Classifier

An AI-powered web app that classifies the emotional tone of text messages (positive, negative, or neutral) using Hugging Face's Transformers and provides visual insights into chat history and trends.

---

## 🌟 Overview

This project is an interactive, real-time sentiment analysis application built with FastAPI, Streamlit, and Hugging Face Transformers. Users can:

- 🔐 Log in or sign up securely  
- 🔍 Analyze messages for sentiment  
- 📚 View sentiment history  
- 📊 Visualize sentiment trends over time with charts  

---

## 🚀 Features

- 🔍 **Instant Sentiment Analysis** using pre-trained NLP models  
- 📊 **Visual Charts** for sentiment distribution and time-series trends  
- 📚 **Message History** with deletion capability  
- 🔐 **User Authentication** (Sign-up/Login)  
- 🌐 **MongoDB Integration** for storing messages and users  
- 🎨 **Custom Streamlit UI** with background image and styling  

---

## 🧠 Technologies Used

- **Python**
- **FastAPI** – Backend API  
- **Hugging Face Transformers** – Pre-trained model `cardiffnlp/twitter-roberta-base-sentiment`  
- **Streamlit** – Frontend UI  
- **MongoDB** – Data storage  
- **Plotly** – Graphical visualization  
- **Torch** – Model inference  

---

## 🛠 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/sentiment-classifier.git
cd sentiment-classifier
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

###3. Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

###4. Start the Streamlit frontend:

```bash
streamlit run app.py
```

---

## 🧪 Usage

- Open your browser at [http://localhost:8501](http://localhost:8501)  
- Register or log in with your credentials  
- Go to the **"Analyze"** tab, type a message, and click **Analyze**  
- View the sentiment result and explore the **History** and **Graphs** tabs  

---

## 🔍 Model Details

- **Model**: `cardiffnlp/twitter-roberta-base-sentiment`  
- **Output**: `positive`, `neutral`, or `negative` label with confidence  
- **Custom Scoring**:  
  - Positive = `+score`  
  - Negative = `-score`  
  - Neutral = `0`  

---

## 🌱 Future Improvements

- Add user profile and theme customization  
- Improve authentication with password hashing  
- Enable comment threads or group sentiment analysis  
- Deploy to the cloud (e.g., Heroku, AWS, or Streamlit Cloud)  

---

## 👩‍💻 Contributor

**Hitashri M** – Developer
