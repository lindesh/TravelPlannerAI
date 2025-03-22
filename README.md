# AI Travel Planner

A web application that provides travel recommendations using Google's Gemini AI and Wikipedia information for destinations.

## Features

- AI-powered travel recommendations using Gemini API
- Wikipedia information integration
- Modern, responsive UI using Vue.js and Tailwind CSS
- Real-time destination search

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   You can get a Gemini API key from: https://makersuite.google.com/app/apikey

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a destination in the search box
2. Click the "Search" button or press Enter
3. View AI-generated travel recommendations and Wikipedia information about the destination

## Technologies Used

- Python/Flask
- Google Gemini AI API
- Wikipedia API
- Vue.js
- Tailwind CSS 

You can test the API key by visiting:
```
http://127.0.0.1:5000/test
```

This will show you a simple test page where you can click the "Test API Key" button to check if your API key is working. The page will show:
1. If the API key is working (Success/Error)
2. The response message from the API
3. A preview of your API key (first 5 characters)

Would you like me to restart the Flask application so you can test it? 