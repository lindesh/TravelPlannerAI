import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import re
from datetime import datetime
import base64
import io

# Load environment variables
load_dotenv()

# Configure Gemini API - try to get from Streamlit secrets first, then from .env file
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables or Streamlit secrets")

# Add debug information
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Travel Planner")
st.markdown("Generate personalized travel itineraries with AI")

# Display API key status
st.sidebar.header("Debug Information")
st.sidebar.write(f"API Key (first 5 chars): {GOOGLE_API_KEY[:5]}...")

try:
    # Initial API configuration test
    genai.configure(api_key=GOOGLE_API_KEY)
    # List available models to verify API key works
    model_list = genai.list_models()
    model_names = [m.name for m in model_list]
    st.sidebar.write("API Connection: Success")
    st.sidebar.write(f"Available models: {', '.join(model_names[:3])}...")
    print("Available models:", model_names)
except Exception as e:
    error_msg = f"Error configuring API: {str(e)}"
    st.sidebar.error(f"API Connection Error: {error_msg}")
    print(error_msg)
    st.error(error_msg)
    traceback.print_exc()
    st.stop()

def test_api_key():
    try:
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-pro')

        # Try a simple test prompt
        response = model.generate_content(
            "Respond with 'API test successful' if you can read this message.",
            generation_config={'temperature': 0.1}
        )

        if response and response.text:
            return True, response.text
        return False, "No response from API"
    except Exception as e:
        error_msg = f"API Test Error: {str(e)}"
        print(error_msg)
        print(f"Full traceback: {traceback.format_exc()}")
        return False, error_msg

def get_travel_recommendations(destination, num_people, num_days, description, start_date=None, end_date=None):
    try:
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-pro')

        # Add date information to the prompt if available
        date_info = ""
        if start_date and end_date:
            date_info = f"\nTravel dates: From {start_date} to {end_date}"

        prompt = f"""
        Create a detailed {num_days}-day travel guide for {destination} for {num_people} {'person' if num_people == 1 else 'people'}.{date_info}
        Trip details: {description}

        Format the response with the following sections, using exact headers:

        1. Daily Itinerary
        For each day, use this format:
        Day X (include actual date if provided)
        • Morning (9:00): Activity/Place
        • Afternoon (14:00): Activity/Place
        • Evening (19:00): Activity/Place
        Include [Location Name](maps) for each place mentioned.

        2. Must-See Attractions
        List key attractions with their exact Google Maps names:
        • [Attraction Name](maps) - Brief description
        • [Attraction Name](maps) - Brief description

        3. Where to Stay
        • Recommended areas: [District/Area Name](maps)
        • Specific hotel suggestions in each area
        • Price ranges per night

        4. Best Time to Visit
        • Seasonal recommendations
        • Weather considerations
        • Special events or festivals

        5. Local Food to Try
        • Must-try dishes
        • [Restaurant/Food District Name](maps) - Specialties
        • Price ranges for meals

        6. Cultural Tips
        • Local customs
        • Etiquette guidelines
        • Important phrases

        7. How to Get Around
        • Public transportation options
        • [Transportation Hub Names](maps)
        • Cost estimates for different modes

        8. Budget Estimate
        • Accommodation: Price range
        • Daily meals: Price range
        • Activities: Price range
        • Transportation: Price range
        • Total estimated budget

        Keep it practical and organized with bullet points.
        For each location mentioned, use the exact name as it would appear on Google Maps using the [Name](maps) format.
        Consider the specific dates when suggesting activities and making recommendations.
        """

        print(f"Requesting travel plan for: {destination}")
        response = model.generate_content(
            prompt,
            generation_config={'temperature': 0.7}
        )

        if not response or not response.text:
            raise Exception("No response received from API")

        # Process the response to add Google Maps links
        processed_text = response.text

        def add_maps_link(match):
            location = match.group(1)
            encoded_location = location.replace(' ', '+')
            return f'[{location}](https://www.google.com/maps/search/?api=1&query={encoded_location})'

        # Replace [Location](maps) format with actual links
        processed_text = re.sub(r'\[(.*?)\]\(maps\)', add_maps_link, processed_text)

        print("Successfully generated travel plan")
        return processed_text

    except Exception as e:
        error_msg = f"Error generating recommendations: {str(e)}"
        print(error_msg)
        print(f"Full traceback: {traceback.format_exc()}")
        raise Exception(error_msg)

def create_download_link(content, filename):
    """Generate a download link for text content"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Travel Plan</a>'
    return href

def main():

    # Sidebar for API test
    with st.sidebar:
        st.header("API Status")
        if st.button("Test API Connection"):
            with st.spinner("Testing API connection..."):
                success, message = test_api_key()
                if success:
                    st.success("API connection successful!")
                else:
                    st.error(f"API connection failed: {message}")

        st.markdown("---")
        st.markdown("### About")
        st.markdown("This app uses Google's Gemini AI to create personalized travel plans.")

    # Main form
    with st.form("travel_form"):
        col1, col2 = st.columns(2)

        with col1:
            destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
            num_people = st.number_input("Number of People", min_value=1, value=2)
            num_days = st.number_input("Number of Days", min_value=1, value=3)

        with col2:
            start_date = st.date_input("Start Date (optional)")
            end_date = st.date_input("End Date (optional)")

        description = st.text_area(
            "Trip Details (optional)",
            placeholder="e.g., Family trip with kids, looking for cultural experiences and outdoor activities, budget-friendly options..."
        )

        submit_button = st.form_submit_button("Generate Travel Plan")

    # Process form submission
    if submit_button:
        if not destination:
            st.error("Please enter a destination")
        else:
            with st.spinner("Generating your personalized travel plan..."):
                try:
                    # Format dates as strings if provided
                    start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
                    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

                    travel_info = get_travel_recommendations(
                        destination,
                        num_people,
                        num_days,
                        description,
                        start_date_str,
                        end_date_str
                    )

                    # Display the travel plan
                    st.markdown("## Your Travel Plan")
                    st.markdown(travel_info)

                    # Create download option
                    safe_filename = "".join(c for c in destination if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"{safe_filename}_travel_plan.txt"

                    # Format the content with additional details
                    formatted_content = f"""
===========================================
Travel Plan for {destination}
===========================================

{travel_info}

-------------------------------------------
Generated by AI Travel Planner
Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===========================================
"""

                    st.markdown("---")
                    st.markdown(create_download_link(formatted_content, filename), unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
