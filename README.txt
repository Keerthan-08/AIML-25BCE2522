The file along with this is apython program designed for the user in the form of an AI ChatBot by using streamlit template and LangChain LLMs 
The LangChain LLM is used for connecting the user input with the AI output with the help of tools
I have used Weather tool by using the coordinate of the places memtioned by the user
For OpenAI source i have used GROQ in which specifically "llama-3.3-70b-versatile" is used
The API key is also in the program because i dont think it could be misused . As it is a Open source free AI the credits arent lost 
The important thing why that is there is because i didnt want to keep it in (.secret) folder and i tried keeping it but it showed me some error like ImportError .
So i let it public.I hope it doesnt affect your impression on me.
I used two tools here i.e. Weather and AImessage tool 
I also used text inputs for place and date because i think it looks good and organised which could be removed and only the search tab could be kept 


Brief go through:

In this project, I built an AI-powered Travel Agent designed to assist users with trip planning by integrating real-time data fetching with conversational AI.
I used Streamlit to build the frontend interface and LangChain with the Groq API (specifically the Llama 3.3 model) to handle the logic and reasoning.
The core feature of this application is its Agentic capability—specifically, the ability to call external tools. I didn't want the AI to just generate generic text
I wanted it to provide accurate, real-time information. To achieve this, I wrote a custom Python function called get_weather_info.
This function interacts with the Open-Meteo API in a two-step process:
1) It geocodes the input city to retrieve latitude and longitude,
2) It fetches the daily forecast for the specific travel dates selected by the user.

To integrate this with the LLM, I used LangChain’s bind_tools method. This effectively teaches the Llama model that it has a 'Weather Tool' available. 
If a user asks, 'Will it rain on my trip?', the model knows not to hallucinate an answer but instead to pause and request the execution of that specific function.
The technical flow handles this inside a while loop within the chat interface. When a user submits a query, I first inject context—such as the origin, destination, and date range—into the prompt.
The model processes this, and if it triggers a tool call, my script intercepts that request. It executes the Python function locally using the arguments provided by the LLM, retrieves the JSON data, and feeds it back into the conversation history as a ToolMessage. The LLM is then invoked a final time to synthesize that raw data into a natural language response for the user.

I also implemented Session State management to ensure the chat history persists as the user interacts with the app, and added error handling to manage API failures gracefully.
This project demonstrates my ability to orchestrate LLM workflows, integrate REST APIs, and manage application state to build functional, data-grounded AI applications.

Package Installation processes :

Note : I was using python 3.14.2,but the version is not well compatible with langchain which is good in 3.9 to 3.12
       So i am using python 3.10 and latest langchain software

pip install streamlit
pip install requests 
pip install langchain-groq

Running the file :

Open the code in VS code and download the above packages in the terminal 
After successful compilation ,
Type the below command in VS Code terminal :
python AI Travel Agent.py runserver
