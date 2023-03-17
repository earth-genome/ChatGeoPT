# ChatGeoPT
A very basic, very brittle proof of concept for an AI assistant for geospatial search [blog post]


https://user-images.githubusercontent.com/108955227/225982137-fadd31ec-1339-4d47-8483-decbbbef7ee0.mov


### What is ChatGeoPT?
ChatGeoPT is a toy demo for exploring ideas related to using Large Languge Models (LLMs) for powering geospatial datascience workflows. The app takes as input a natural language prompt, translates it into an OpenStreeMap Overpass API query, and then reads the result of the API query to answer the original prompt.

The entirety of ChatGeoPT is under 200 lines of Python code. It is built on top of some amazingly powerful libraries and tools, including OpenAI's language models, OSM's Overpass API, and Streamlit.

To run ChatGeoPT, please install the requirements in `requirements.txt` using your favorite virtual enviornment manager. You can then run the Streamlit app using the command `streamlit run app.py`. Please note that you will need to set an enviornment variable `OPENAI_API_KEY`, which should be a valid OpenAI API Key, in order to query the GPT-3 LLM.

Further note that this code is meant for demonstration purposes only -- we can almost gaurantee you will break it when using it for even basic searches.

For more information, check out our blog post here: [insert link]
