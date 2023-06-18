import tkinter as tk
import urllib.request
import os
from pywebcopy import save_webpage

def download_html():
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

root = tk.Tk()
root.title("Website HTML Downloader")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

enter_button = tk.Button(root, text="Enter", command=download_html)
enter_button.pack()

root.mainloop()