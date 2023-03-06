import os
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
from PIL import Image

class ImageScraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scraper")
        self.root.geometry("500x300")

        self.url_label = Label(root, text="Enter a URL:")
        self.url_label.pack()

        self.url_entry = Entry(root)
        self.url_entry.pack()

        self.directory_label = Label(root, text="Select a download directory:")
        self.directory_label.pack()

        self.directory_button = Button(root, text="Select Directory", command=self.choose_directory)
        self.directory_button.pack()

        self.format_label = Label(root, text="Enter a file format (e.g. jpg, png):")
        self.format_label.pack()

        self.format_entry = Entry(root)
        self.format_entry.pack()

        self.download_button = Button(root, text="Download Images", command=self.download_images)
        self.download_button.pack()

        self.rename_button = Button(root, text="Rename Images", command=self.rename_images, state=DISABLED)
        self.rename_button.pack()

        self.quit_button = Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def choose_directory(self):
        self.download_directory = filedialog.askdirectory()
        self.directory_label.config(text=f"Download directory selected: {self.download_directory}")

    def download_images(self):
        self.url = self.url_entry.get()
        self.format = self.format_entry.get()
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.images = self.soup.find_all("img")
        self.image_urls = [img["src"] for img in self.images]
        self.download_path = os.path.join(self.download_directory, "results")
        os.makedirs(self.download_path, exist_ok=True)
        self.image_filenames = []
        for i, url in enumerate(self.image_urls):
            self.image_data = requests.get(url).content
            self.image_file = os.path.join(self.download_path, f"image_{i}.{self.format}")
            with open(self.image_file, "wb") as f:
                f.write(self.image_data)
            self.image_filenames.append(self.image_file)
        self.rename_button.config(state=NORMAL)

    def rename_images(self):
        for i, filename in enumerate(self.image_filenames):
            new_filename = os.path.join(self.download_path, f"{i+1}.{self.format}")
            with Image.open(filename) as img:
                img.save(new_filename)
            os.remove(filename)
        self.rename_button.config(state=DISABLED)
        print("Images renamed successfully.")

root = Tk()
image_scraper = ImageScraper(root)
root.mainloop()
