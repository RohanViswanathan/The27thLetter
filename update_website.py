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

filename = os.path.join(os.path.expanduser("~"), "Downloads", project_name, recombined_url, "index.html")
# filename = os.path.join(os.path.expanduser("~"), "Downloads", "website-short.html")
with open(filename, 'r', encoding='utf-8') as file:
    html_content = file.readlines()

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

prompt = '''Modify the following HTML code to be more accessible for the visually impaired, by making the font sizes bigger, fixing spacing issues by 
adding more space between visual elements, and increasing the contrast of images. Also make colors more accessible for people who are colorblind. 
Rearrage sections and add padding to make the website look nicer, if needed, without removing information. You will also replace HTML tags with the tag 
"img" with code that will allow me to hover over images to show corresponding text. For each of these HTML "img" tags, it will contain a "src" that has a file, and you will look for the corresponding text in a 
dictionary I will provide. I will provide the dictionary and HTMl code now. Return just the revised html code.'''

start_time = time.time()

print("Starting query...")

revised_html_parts = []
current_part = ""
character_count = 0
max_character_count = 7000

for line in html_content:
    line = line.strip()
    line_length = len(line)

    # Check if adding the line will exceed the maximum character count
    if character_count + line_length > max_character_count:
        revised_html_parts.append(current_part)
        current_part = line
        character_count = line_length
    else:
        current_part += line
        character_count += line_length

# Append the last part
if current_part:
    revised_html_parts.append(current_part)

# Process each part with the OpenAI API
revised_html = ""

i = 0
for part in revised_html_parts:
    print(i, "part ...")
    i += 1
    response = openai.ChatCompletion.create(
        model = 'gpt-4', 
        messages=[{"role": "user", "content": prompt + "Dictionary: " + str(captions) +  ". HTML: " + part}],
    )
    revised_html += response.choices[0].message.content

end_time = time.time()
duration = end_time - start_time

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