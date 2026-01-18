import streamlit as st
import requests
from datetime import date, timedelta
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage


# WEATHER TOOL
def get_weather_info(city: str, start_date: str, end_date: str):

    try:
        # Getting the coordinates for the place specified 
        # The JSON format keeps the requuired place lat and log in dictionary format
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
        geo_res = requests.get(geo_url).json()
        if not geo_res.get("results"): return "City not found."
        loc = geo_res["results"][0] # A double dimension array but takes the first set of dictionary
        
        # Weather Forecast Prediction after using the co ordinates and date range given
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}&longitude={loc['longitude']}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&start_date={start_date}&end_date={end_date}&timezone=auto"
        )
        
        w_data = requests.get(weather_url).json()
        daily = w_data["daily"]

        # Checking the entire date range for
        summary = f"Weather for {city} ({start_date} to {end_date}):\n"
        for i in range(len(daily["time"])):
            summary += (f"- {daily['time'][i]}: High {daily['temperature_2m_max'][i]}°C, "
                        f"Low {daily['temperature_2m_min'][i]}°C, "
                        f"Rain: {daily['precipitation_probability_max'][i]}%\n")
        return summary # Sends AI readable summary (Normal English)
    except Exception as e:
        return f"Weather data error: {e}"

# Map for tools 
# Creation of a dictonary 
tools_map = {"get_weather_info": get_weather_info}

#STREAMLIT INTERFACE
st.set_page_config(page_title="AI Travel Agent")
st.title(" AI Travel Agent")

with st.sidebar:# Perfect place to place the input interface 
    st.header("Trip Details")
    api_key = "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"
    city1=st.text_input("From Location",placeholder="e.g. Vellore")
    city = st.text_input("Destination City", placeholder="e.g. Banglore")

    # Creating the date inferface
    today = date.today()
    date_range = st.date_input(
        "Travel dates (FROM - TO)",
        value=(today, today + timedelta(days=4)),
        min_value=today,
        format="DD/MM/YYYY"
    )
    
# Saving the chat history if not saved
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Groq initialization 
if api_key:
    try:
        # Initializing LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.9,# Almost creative (has a range from 0.0 to 1.0 (and some have upto 2.0 ))
            groq_api_key=api_key 
        )
        
        llm_with_tools = llm.bind_tools([get_weather_info]) # Binding tool with AI using LangChain

        for msg in st.session_state.chat_history:# Display chat 
            if isinstance(msg, HumanMessage): # From Streamlit interface for human message
                st.chat_message("user").write(msg.content)
            elif isinstance(msg, AIMessage) and msg.content: # From Streamlit interface for AI message
                st.chat_message("assistant").write(msg.content)

        if user_query := st.chat_input("Ask about your trip!"): # Input 
            if not city or len(date_range) != 2:
                st.warning("Please enter a city and select a dates!")
            else:
                st.chat_message("user").write(user_query)
                
                # This is what AI takes as input to search its entire Data Base of info
                full_input = (
                    f"I am traveling to {city} from {city1}, from{date_range[0]} to {date_range[1]}.And you must help me by seeing all travel websites,accomodation websites with timing but only say when i ask you"
                    f"Question: {user_query}"
                )
                st.session_state.chat_history.append(HumanMessage(content=full_input)) # To store the previous input and output in display

                #####

                with st.chat_message("assistant"):
                    flow = st.session_state.chat_history.copy() # Copied in case of future reasoning 
                    
                    while True:
                        with st.spinner(""): # The buffering circle
                            response = llm_with_tools.invoke(flow) # Sending the convo to AI
                        
                        if response.tool_calls:
                            flow.append(response)
                            for tool_call in response.tool_calls: # Tool calling 
                                tool_args = tool_call["args"]
                                tool_args["start_date"] = str(date_range[0]) # Forcing DAte into tool argument
                                tool_args["end_date"] = str(date_range[1])   # Forcing DAte into tool argument
                                
                                tool_output = get_weather_info(**tool_args)
                                tool_msg = ToolMessage(content=tool_output, tool_call_id=tool_call["id"])
                                flow.append(tool_msg) # Adding the content to the memory 
                        else:
                            st.markdown(response.content)
                            st.session_state.chat_history.append(response) # after thinking it respondes and breaks  Waiting for the next input
                            break
    except Exception as e:
        st.error(f"Configuration error: {e}")
else:

    st.info("Please enter your Groq API Key in the sidebar to start.")


