import os
import openai
import time
from dotenv import load_dotenv
import tkinter as tk
from pywebcopy import save_webpage
import replicate

load_dotenv()

# Download HTML

def download_html():
    global url
    url = url_entry.get()
    global project_name
    project_name = "accessible_site"
    if url:
        try:
            save_webpage(
                url=url,
                project_folder=os.path.join(os.path.expanduser("~"), "Downloads"),
                project_name=project_name,
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

url = url.replace('~', '')
split_url = url.split('/')
recombined_url = '/'.join(split_url[2:-1])

# filename = os.path.join(os.path.expanduser("~"), "Downloads", project_name, recombined_url, "index.html")
filename = os.path.join(os.path.expanduser("~"), "Downloads", "website-short.html")
with open(filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Image Captioning

directory = os.path.join(os.path.expanduser("~"), "Downloads", project_name, recombined_url)

captions = {}

for file in os.listdir(directory):
    f = os.path.join(directory, file)
    if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('gif'):
        output = replicate.run(
            "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8",
            input={"image": open(f, "rb")}
        )
        captions[file] = output

print(captions)

prompt = '''Modify the following html code to be more accessible for the visually impaired, by making the font sizes bigger, fixing spacing issues by 
adding more space between visual elements. Also make red and green elements more conducive to people that are 
color-blind, by changing their color and style. You will also replace HTML tags with the tag "img" with code that will allow me to hover over images to 
show corresponding text. For each of these HTML "img" tags, it will contain a "src" that has a file, and you will look for the corresponding text in a 
dictionary I will provide. I will provide the dictionary and HTMl code now. Return just the revised html code.'''

start_time = time.time()

print("Starting query...")

print(prompt + "Dictionary: " + str(captions) +  ". HTML: " + html_content)

response = openai.ChatCompletion.create(
    model = 'gpt-4', 
    messages=[{"role": "user", "content": prompt + "Dictionary: " + str(captions) +  ". HTML: " + html_content}],
    )

end_time = time.time()
duration = end_time - start_time

revised_html = response.choices[0].message.content

print("Finished query...")

revised_filename = os.path.join(os.path.expanduser("~"), "Downloads", project_name, recombined_url, "revised-website.html")

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