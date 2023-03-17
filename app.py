import folium
import openai
import requests
import streamlit as st
import tiktoken

import os


# Define the Overpass API endpoint URL
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# Set the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Chat template string, to be used for generating Overpass API queries
CHAT_TEMPLATE = """Assistant is an expert OpenStreetMap Overpass API assistant.

For each question that the user supplies, the assistant will reply with:
(1) A statement consenting to help.
(2) The text of a valid Overpass API query that can be used to answer the question. The query should be enclosed by three backticks on new lines, denoting that it is a code block.
(3) A fun fact relating to the question, or a very funny joke or pun related to the question. The joke or pun should also relate to maps, geospatial tech, geography or similar concepts. There is no need to label the fact, joke, or pun.

Assistant has a whimsical personality. Assistant will reply with a geospatial themed joke or a pun if the user asks a question that is not relevant to the Overpass API.

{history}
Human: {human_input}
Assistant:"""

# Reader template string, to be used for generating text responses drawing on Overpass API responses
READER_TEMPLATE = """Read the following Overpass API response carefully. Use the information in it to answer the prompt "{prompt}" Your answer should not mention the words "API" or "Overpass." Your answer should sound like it was spoken by someone with personal knowledge of the question's answer. Your answer should be very concise, but also informative and fun. Format any names or places you get from the API response as bold text in Markdown.
Overpass API Response:
Answer: {response}
"""

# Create a tokenizer
ENC = tiktoken.encoding_for_model("text-davinci-003")

# Define a function to query the Overpass API and return the JSON response
def query_overpass(query):
    payload = {"data": query}
    response = requests.post(OVERPASS_API_URL, data=payload)
    return response.json()

# Define the Streamlit app
def main():
    # Set the app title and description
    st.set_page_config(layout="wide", page_title="OSM Overpass Query App", page_icon=":earth_africa:")
    st.title("Chat:earth_africa:")
    st.write("Hello! :wave: I'm Chat:earth_africa:, a Geospatial AI assistant. For any question you ask in the textbox below, "
             "I'll generate an OpenStreetMap Overpass query to answer your question, and plot the results on a map. "
             "I'll remember our conversation, so feel free to ask follow ups. I'm also a geospatial themed joke and pun expert. :smile:")

    # Define the layout of the app
    col1, col2 = st.columns([1, 1])

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    if 'overpass_query' not in st.session_state:
        st.session_state.overpass_query = None

    if 'prompt_history' not in st.session_state:
        st.session_state.prompt_history = ""

    # Define the query input box in the left pane
    with col1:
        chat = st.text_area("What can I help you find? :thinking_face:")

        if st.button("Ask"):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=CHAT_TEMPLATE.format(history=st.session_state.chat_history, human_input=chat),
                temperature=0,
                max_tokens=516,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Display the response as pure text
            st.write(response["choices"][0]["text"])

            # Update the history string
            st.session_state.chat_history = st.session_state.chat_history + f"Human: {chat}\nAssistant: {response['choices'][0]['text']}\n"

            # Update the prompt history string
            st.session_state.prompt_history = st.session_state.prompt_history + f"{chat} "

            # Update the Overpass query. The query is enclosed by three backticks, denoting that is a code block.
            # does the response contain a query? If so, update the query
            if "```" in response["choices"][0]["text"]:
                st.session_state.overpass_query = response["choices"][0]["text"].split("```")[1]
            else:
                st.session_state.overpass_query = None

            # Define the query button in the left pane
            with col2:

                if st.session_state.overpass_query:
                    # Query the Overpass API
                    response = query_overpass(st.session_state.overpass_query)

                    # Check if the response is valid
                    if "elements" in response and len(response["elements"]) > 0:
                        # Create a new Folium map in the right pane
                        m = folium.Map(location=[response["elements"][0]["lat"], response["elements"][0]["lon"]], zoom_start=11)

                        # Add markers for each element in the response
                        for element in response["elements"]:
                            if "lat" in element and "lon" in element:
                                folium.Marker([element["lat"], element["lon"]]).add_to(m)

                        # Display the map
                        st.write(m)

                        # If the request for summary of the API response is shorter than 1500 tokens,
                        # use the Reader model to generate a response

                        query_reader_prompt  = READER_TEMPLATE.format(prompt=st.session_state.prompt_history,
                                                                      response=str(response))
                        query_reader_prompt_tokens = len(ENC.encode(query_reader_prompt))
                        if query_reader_prompt_tokens < 1500:

                            response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=query_reader_prompt,
                                temperature=0.5,
                                max_tokens=2047 - query_reader_prompt_tokens,
                                top_p=1,
                                frequency_penalty=0,
                                presence_penalty=0
                            )

                            # Display the response as pure text
                            st.write(response["choices"][0]["text"])
                        else:
                            st.write("The API response is too long for me to read. Try asking for something slightly more specific! :smile:")
                    else:
                        st.write("No results found :cry:")

if __name__ == "__main__":
    main()