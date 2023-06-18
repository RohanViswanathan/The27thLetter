import os
import openai
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

filename = os.path.join(os.path.expanduser("~"), "Downloads", "website-short.html")
with open(filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

prompt = "Modify the following html code to be more accessible for the visually impaired, by making the font sizes bigger, fixing spacing issues by adding more space between visual elements, and increasing the contrast of images. Return just the revised html code."

start_time = time.time()

print("Starting query...")

response = openai.ChatCompletion.create(
    model = 'gpt-4', 
    messages=[{"role": "user", "content": prompt + html_content}],
    )

end_time = time.time()
duration = end_time - start_time

revised_html = response.choices[0].message.content

print("Finished query...")

revised_filename = os.path.join(os.path.expanduser("~"), "Downloads", "revised-website.html")

with open(revised_filename, 'w', encoding='utf-8') as file:
    file.write(revised_html)

print("Revised HTML code saved successfully!")
print("Query duration:", duration, "seconds")

# API Test

# response = openai.ChatCompletion.create(
#     model = 'gpt-4', 
#     messages=[{"role": "user", "content": "Complete the text... france is famous for its"}]
#     )


# print(response.choices[0].message.content)