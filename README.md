# AI Travel Planner

An interactive web application that generates personalized travel itineraries using Google's Gemini AI. The application provides detailed travel recommendations including daily itineraries, must-see attractions, accommodation suggestions, and budget estimates.

This application is available in two versions:
- Flask web application (app.py)
- Streamlit application (streamlit_app.py)

## Features

- 🌍 Personalized travel recommendations
- 📅 Day-by-day itinerary planning
- 💰 Smart budget calculation and tracking
- 🏨 Accommodation suggestions
- 🍴 Local food recommendations
- 🎯 Must-see attractions with Google Maps integration
- 📥 Downloadable travel plans
- ✨ Interactive UI with animations

## Technologies Used

- Backend: Python, Flask/Streamlit
- Frontend: Vue.js, Tailwind CSS (Flask version) / Streamlit UI (Streamlit version)
- AI: Google Gemini API

## Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

4. Run the application:

For Flask version:
```bash
python app.py
```
Then open your browser and navigate to `http://localhost:5000`

For Streamlit version:
```bash
streamlit run streamlit_app.py
```
Then open your browser and navigate to `http://localhost:8501`

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key

## Usage

1. Enter your destination
2. Specify number of travelers and duration
3. Add optional trip description
4. Set your budget (manual or automatic)
5. Click "Generate Travel Plan"
6. View and download your personalized itinerary

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Testing the API Key

**Flask Version:**
You can test the API key by visiting:
```
http://127.0.0.1:5000/test
```

This will show you a simple test page where you can click the "Test API Key" button to check if your API key is working.

**Streamlit Version:**
The Streamlit app includes API testing functionality in the sidebar.