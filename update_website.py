import os
import openai
import time
from dotenv import load_dotenv
import tkinter as tk
from pywebcopy import save_webpage

load_dotenv()

# Download HTML

def download_html():
    global url
    url = url_entry.get()
    if url:
        try:
            folder_name = os.path.join(os.path.expanduser("~"), "Downloads")
            save_webpage(
                url=url,
                project_folder=folder_name,
                project_name="my_site",
                bypass_robots=True,
                debug=True,
                open_in_browser=True,
                delay=None,
                threaded=False,
            )
            print("HTML source code downloaded successfully!")
        except Exception as e:
            print("An error occurred while downloading the HTML source code:", str(e))
    else:
        print("Please enter a valid URL.")
    root.destroy()

root = tk.Tk()
root.title("Website HTML Downloader")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

enter_button = tk.Button(root, text="Enter", command=download_html)
enter_button.pack()

root.mainloop()

# Update Website

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

filename = os.path.join(os.path.expanduser("~"), "Downloads", "website-short.html")
with open(filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

prompt = "Modify the following html code to be more accessible for the visually impaired, by making the font sizes bigger, fixing spacing issues by adding more space between visual elements, and increasing the contrast of images. Also make red and green elements more conducive to people that are color-blind, by changing their color and style. Return just the revised html code."

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