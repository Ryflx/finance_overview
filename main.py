import os
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set your API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
companyName = st.text_input("Enter the company name:")

def serpapi_search(query):
    search = GoogleSearch({
        "q": query,
        "api_key": SERPAPI_API_KEY
    })
    results = search.get_dict()
    return results.get("organic_results", [])

def generate_combined_response(queries):
    combined_results = ""

    for query in queries:
        # Perform the web search
        search_results = serpapi_search(query)

        # Format the search results for the assistant
        formatted_results = "\n".join([f"{i+1}. {result['title']}: {result['link']}" for i, result in enumerate(search_results[:5])])

        # Append to the combined results
        combined_results += f"Top search results for '{query}':\n{formatted_results}\n\n"

    # Create the prompt for the assistant
    prompt = f"""Populate this HTML with data for {companyName}, please output only HTML tags and REPLACE text data with Data for {companyName}.:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Overview</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            padding: 20px;
        }}
        .box {{
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .box h2 {{
            color: #5a5a5a;
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        .box ul {{
            list-style-type: none;
            padding: 0;
        }}
        .box ul li {{
            margin-bottom: 10px;
            font-size: 1em;
        }}
        @media (min-width: 600px) {{
            .box {{
                width: 45%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <h2>Financial Analysis</h2>
            <ul>
                <li>Revenue growth 6% (€30bn)</li>
                <li>25% Sales growth vs. 2022</li>
                <li>Steady YoY growth</li>
            </ul>
        </div>
        <div class="box">
            <h2>Operational Analysis</h2>
            <ul>
                <li>Declining open positions</li>
                <li>Digital transformation</li>
                <li>New M&A director</li>
            </ul>
        </div>
        <div class="box">
            <h2>Strategic Review</h2>
            <ul>
                <li>Operational efficiencies</li>
                <li>Digital transformation</li>
                <li>Sustainable profitability</li>
            </ul>
        </div>
        <div class="box">
            <h2>Expansion</h2>
            <ul>
                <li>Numis Corp acquisition</li>
                <li>ASIA / UK expansion</li>
                <li>Growing Payments Channel</li>
            </ul>
        </div>
        <div class="box">
            <h2>Technology</h2>
            <ul>
                <li>Tech spend growing</li>
                <li>Security investment</li>
                <li>Emulating Neo Banks</li>
            </ul>
        </div>
        <div class="box">
            <h2>Sustainability</h2>
            <ul>
                <li>Increasing ESG capability</li>
                <li>Opportunities in lending market</li>
                <li>New head of Sustainability</li>
            </ul>
        </div>
    </div>
</body>
</html>"""

    # Generate the response using OpenAI API
    response = client.chat.completions.create(model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    return response.choices[0].message.content

# Example usage
queries = [f"{companyName} financial analysis 2024", f"{companyName} operational analysis 2024", f"{companyName} strategic review 2024", f"{companyName} strategic review 2024", f"{companyName} technology investments 2024", f"{companyName} sustainability initiatives 2024"]
response = generate_combined_response(queries)
st.markdown(response, unsafe_allow_html=True)
