# Gemini Currency Converter

A Python-based currency conversion application that uses the **Google Gemini API** and live exchange rates to convert currencies.

## Features

- Converts an amount from one currency to another.
- Retrieves live exchange rates from a public currency API.
- Uses Gemini function calling to decide when to execute the currency conversion function.
- Returns the conversion rate and converted amount.
- Uses environment variables to keep API credentials out of the source code.

## Technologies Used

- Python
- Google Gemini API
- Google Gen AI SDK
- REST API
- ExchangeRate-API (Open ER API)
- python-dotenv
- Requests

## Project Structure

```text
gemini-currency-converter/
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gemini-currency-converter.git
cd gemini-currency-converter
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project directory:

```env
API_KEY=your_gemini_api_key
```

Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/).

**Security:** Never upload your real `.env` file or API key to GitHub.

### 4. Run the application

```bash
python app.py
```

The current example converts 100 USD to INR. The application retrieves the exchange rate, executes the conversion function, and asks Gemini to generate a human-readable response.

## How It Works

1. The user provides a currency conversion request.
2. Gemini receives the request and the registered `convert_currency` tool declaration.
3. Gemini can request the function call with the required arguments.
4. Python executes the conversion function using live exchange-rate data.
5. The function result is returned to Gemini.
6. Gemini generates the final response for the user.

## Key Concepts Learned

- API integration
- Environment variable configuration
- Function declarations and tool calling
- Function-call argument extraction
- Python keyword argument unpacking
- REST API requests and JSON responses
- Passing function results back to an LLM

## Future Improvements

- Accept user input dynamically instead of using a hardcoded query.
- Support multiple currency conversion requests.
- Add input validation and error handling.
- Build a web interface using Streamlit or Gradio.
- Add unit tests for currency conversion.

## Disclaimer

Exchange rates fluctuate over time. The returned rate depends on the exchange-rate API response and may not reflect the exact
