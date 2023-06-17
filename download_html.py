import tkinter as tk
import urllib.request
import os

def download_html():
    url = url_entry.get()
    if url:
        try:
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
            filename = os.path.join(os.path.expanduser("~"), "Downloads", "website.html")
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html)
            print("HTML source code downloaded successfully!")
        except Exception as e:
            print("An error occurred while downloading the HTML source code:", str(e))
    else:
        print("Please enter a valid URL.")

root = tk.Tk()
root.title("Website HTML Downloader")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

enter_button = tk.Button(root, text="Enter", command=download_html)
enter_button.pack()

root.mainloop()