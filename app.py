import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def fetch_website_contents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

system_prompt = """
Provide a concise and accurate summary of the website.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary.
"""

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

def summarize(url):
    website = fetch_website_contents(url)

    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages_for(website)
    )

    return response.choices[0].message.content

print(summarize("https://blog.samaltman.com"))