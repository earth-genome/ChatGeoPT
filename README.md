# ChatGeoPT
A very basic, very brittle proof of concept for an AI assistant for geospatial search [[blog post](https://medium.com/@bengmstrong/chatgeopt-exploring-the-future-of-talking-to-our-maps-b1f82903bb05)]


https://user-images.githubusercontent.com/108955227/225982137-fadd31ec-1339-4d47-8483-decbbbef7ee0.mov


### What is ChatGeoPT?
ChatGeoPT is a toy demo for exploring ideas related to using Large Languge Models (LLMs) for powering geospatial datascience workflows. The app takes as input a natural language prompt, translates it into an OpenStreeMap Overpass API query, and then reads the result of the API query to answer the original prompt.

The entirety of ChatGeoPT is under 200 lines of Python code. It is built on top of some amazingly powerful libraries and tools, including OpenAI's language models, OSM's Overpass API, and Streamlit.

**Please note** that this code is meant for demonstration purposes only -- we can almost gaurantee you will break it when using it for even basic searches.

For more information, check out our blog post [here](https://medium.com/@bengmstrong/chatgeopt-exploring-the-future-of-talking-to-our-maps-b1f82903bb05)

### Running ChatGeoPT
To run ChatGeoPT, please install the requirements in `requirements.txt` using your favorite virtual enviornment manager. You can then run the Streamlit app using the command `streamlit run app.py`. You will also need to set an enviornment variable `OPENAI_API_KEY`, which should be a valid OpenAI API Key, in order to query the GPT-3 API.

### Troubleshooting
Not getting great results? Give feedback to GPT-3 directly in the chatbox (e.g. "That searches the wrong area -- can you try again?") The more specific the feedback, the better. If that doesn't work, try restarting the app. Sometimes GPT-3 gets stuck in a loop of bad decisions, and restarting the app will refresh its state.
