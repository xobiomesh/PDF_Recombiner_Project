import fitz  # PyMuPDF
from tkinter import Canvas, NW, Scrollbar, Frame, VERTICAL
from PIL import Image, ImageTk

class ThumbnailViewer:
    def __init__(self, parent, add_page_callback):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0, rowspan=10, sticky="nsew")

        self.canvas = Canvas(self.frame, width=200, height=800)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.thumbnails = []
        self.add_page_callback = add_page_callback

    def load_thumbnails(self, pdf_path):
        self.clear_thumbnails()
        doc = fitz.open(pdf_path)
        y_position = 0  # Initial y position for thumbnails
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))  # Generate a thumbnail with 20% scale
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = ImageTk.PhotoImage(img)
            self.thumbnails.append(img)
            self.canvas.create_image(0, y_position, anchor=NW, image=img, tags=(f"thumbnail_{page_num}",))
            self.canvas.tag_bind(f"thumbnail_{page_num}", "<Button-1>", lambda event, page_num=page_num: self.add_page_callback(page_num))
            y_position += pix.height + 10  # Update y position for the next thumbnail

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def clear_thumbnails(self):
        self.canvas.delete("all")
        self.thumbnails = []
