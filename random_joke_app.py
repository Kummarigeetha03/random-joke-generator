import streamlit as st
import requests

# Set up the page title and description
st.title("Random Joke Generator")
st.write("Choose your type of joke and click the button below to get one!")

# Initialize session state for storing favorite jokes and joke history
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'current_joke' not in st.session_state:
    st.session_state['current_joke'] = None

# Function to fetch a joke from an API
def get_joke(joke_type):
    if joke_type == "Random":
        joke_api_url = "https://official-joke-api.appspot.com/random_joke"
    else:
        joke_api_url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
    
    response = requests.get(joke_api_url)
    if response.status_code == 200:
        joke_data = response.json()
        if isinstance(joke_data, list):
            joke_data = joke_data[0]  # In case of a list, get the first joke
        joke = f"{joke_data['setup']} ... {joke_data['punchline']}"
        # Add joke to history
        st.session_state.history.append(joke)
        st.session_state.current_joke = joke  # Store the current joke in session state
        return joke
    else:
        return "Oops! Couldn't fetch a joke at the moment."

# Fun Mode: Toggle for enhanced joke delivery
fun_mode = st.checkbox("Enable Fun Mode 🎉")

# Let the user choose the type of joke
joke_type = st.selectbox(
    "Select the type of joke:",
    ("Random", "general", "programming", "knock-knock")
)

# Add a button to generate a new joke
if st.button("Get a Random Joke"):
    joke = get_joke(joke_type)
    if fun_mode:
        joke = f"😂 🎉 {joke} 🎉 😂"
    st.write(joke)

# Separate "Save to Favorites" button to ensure it works independently
if st.session_state.current_joke:
    if st.button("Save to Favorites"):
        st.session_state.favorites.append(st.session_state.current_joke)
        st.write("Joke saved to favorites! ❤️")

# User can rate the joke
if st.session_state.current_joke:
    st.write("Did you like the joke?")
    rating = st.radio("Rate the joke:", ("😂 Hilarious", "🙂 It's okay", "😐 Not funny"))

    # Thank the user for rating
    if rating == "😂 Hilarious":
        st.write("Glad you loved it! 🎉")
    elif rating == "🙂 It's okay":
        st.write("Thanks for the feedback! 👍")
    else:
        st.write("We'll try harder next time! 🙃")

# Display the user's favorite jokes
st.write("### Your Favorite Jokes ❤️")
if st.session_state['favorites']:
    for favorite_joke in st.session_state['favorites']:
        st.write(f"• {favorite_joke}")
else:
    st.write("No favorite jokes yet!")

# Display joke history
st.write("### Joke History 📜")
if st.session_state['history']:
    for past_joke in st.session_state['history']:
        st.write(f"• {past_joke}")
else:
    st.write("No jokes shown yet!")

# Mock Leaderboard: Top rated jokes (static for now)
st.write("### Joke Leaderboard 🏆")
st.write("1. Why don't skeletons fight each other? ... They don't have the guts! (Rating: 😂 Hilarious)")
st.write("2. How does a penguin build its house? ... Igloos it together! (Rating: 😂 Hilarious)")
st.write("3. What do you call fake spaghetti? ... An impasta! (Rating: 🙂 It's okay)")

