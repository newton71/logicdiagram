# -*- coding: utf-8 -*-
"""
Created on Web Mar 8 16:29:52 2024
Input: Program description in text
Output: Logic diagram of Resources -> Activities -> Output
@author: rkpal
"""

import os
#OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import(AIMessage, HumanMessage,SystemMessage)
import json
import streamlit as st

from plotLogicDiagram import*

#-------------------------------------------------------------------------------------------------------

isDevt = 0

if isDevt == 1:
   openai_api_key = os.environ["OPENAI_API_KEY"]
else:
   openai_api_key = st.secrets["OPENAI_API_KEY"]


st.set_page_config(
    page_title="Logic diagram",
    layout="wide",  # Use "wide" layout for a wider page
)

#-------------------------------------------------------------------------------------------------------

st.title("Logic diagram from Program description")

col1, col2 = st.columns([1, 2])

with col1:
    program = st.text_area("Enter your program description here:", height=500)
    isSubmit = st.button("Create logic diagram") 

# Optionally, display the inputted text
if isSubmit:
   
#--------------------------------------------------------------------------------------------------------    
        
    # Make the API call to OpenAI GPT-3 for summarization
    chat_messages = [
            SystemMessage(content = "You are an expert in breaking down a health program description and identify resources, \
                          activities and output"),
                           
            HumanMessage( content = f"From this program description: {program}, \
                         1. Identify and list the resources needed for the program \
                         2. List the activities that used the resources. They are specific actions or processes that are part of the program's implementation. Write them briefly. \
                         3. Identify the output of the activities \
                         If there are tiers according to disease severity describe them \
                         Produce your output in JSON format: (Resource, Activity) and (Activity, Output) \
                         The resource should link to the activity.  The activity should link to output. \
                         The number of resources, activities and output need not be the same    \
                         in the JSON output, the first field should be 'Link1' and the second field 'Link2' \
                         The JSON output should only have 1 level of depth i.e. Resource, Activity and Output    ")
    ]
    
                                     
    llm = ChatOpenAI(model_name = 'gpt-4-0613', temperature = 0)
    
    summary_json = llm(chat_messages).content
    summary_dict = json.loads(summary_json)
    
    
    for i in range(len(summary_dict["Link1"])):
        print(summary_dict["Link1"][i])
        
    for i in range(len(summary_dict["Link2"])):
        print(summary_dict["Link2"][i])
    
    graph_image = plotLogic(summary_dict)
    
    
    with col2:
        # Display the graph image in Streamlit
        st.image(graph_image, caption = 'Logic Diagram', use_column_width=True)
