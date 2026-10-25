import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)


# Convert currency using live exchange rates
def convert_currency(amount, from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"

    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("result") != "success":
        return {"error": "Currency API request failed"}

    rates = data["rates"]
    to_currency = to_currency.upper()

    if to_currency not in rates:
        return {"error": f"Unsupported currency: {to_currency}"}

    rate = rates[to_currency]

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency,
        "amount": amount,
        "exchange_rate": rate,
        "converted_amount": round(amount * rate, 2)
    }


# Declare the function as a Gemini tool
convert_currency_declaration = types.FunctionDeclaration(
    name="convert_currency",
    description="Convert an amount from one currency to another using live exchange rates.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "amount": {
                "type": "NUMBER",
                "description": "Amount to convert"
            },
            "from_currency": {
                "type": "STRING",
                "description": "Source currency code, such as USD"
            },
            "to_currency": {
                "type": "STRING",
                "description": "Target currency code, such as INR"
            }
        },
        "required": ["amount", "from_currency", "to_currency"]
    }
)

currency_tool = types.Tool(
    function_declarations=[convert_currency_declaration]
)


# Ask Gemini to process the user's request
user_query = "Convert 100 USD to INR."

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_query,
    config=types.GenerateContentConfig(
        tools=[currency_tool]
    )
)


# Find the function call
function_call = next(
    (p.function_call for p in response.parts if p.function_call),
    None
)

if function_call:
    result = convert_currency(**function_call.args)

    # Package the function result for Gemini
    function_response = types.Part.from_function_response(
        name=function_call.name,
        response=result
    )

    # Ask Gemini to generate the final answer
    final_response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text=user_query)]
            ),
            response.candidates[0].content,
            types.Content(
                role="user",
                parts=[function_response]
            )
        ],
        config=types.GenerateContentConfig(
            tools=[currency_tool]
        )
    )

    print(final_response.text)

else:
    print(response.text)
