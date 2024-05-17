import fitz  # PyMuPDF
from tkinter import Canvas, NW, Scrollbar, Frame, VERTICAL, Button, HORIZONTAL
from PIL import Image, ImageTk

class PDFViewer:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=1, rowspan=10, sticky="nsew")

        self.canvas = Canvas(self.frame, width=600, height=800)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = Scrollbar(self.frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.h_scrollbar.set)

        self.current_pdf_path = None
        self.current_page_num = 0

        # Navigation buttons for PDF pages
        self.prev_page_btn = Button(parent, text="Previous Page", command=self.prev_page)
        self.prev_page_btn.grid(row=10, column=0, pady=5, sticky="e")

        self.next_page_btn = Button(parent, text="Next Page", command=self.next_page)
        self.next_page_btn.grid(row=10, column=1, pady=5, sticky="w")

    def load_pdf(self, pdf_path):
        self.current_pdf_path = pdf_path
        self.current_page_num = 0
        self.display_page()

    def display_page(self):
        if not self.current_pdf_path:
            return
        doc = fitz.open(self.current_pdf_path)
        page = doc.load_page(self.current_page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.image = img  # Keep a reference to avoid garbage collection
        self.canvas.config(scrollregion=self.canvas.bbox(NW))

    def prev_page(self):
        if self.current_page_num > 0:
            self.current_page_num -= 1
            self.display_page()

    def next_page(self):
        doc = fitz.open(self.current_pdf_path)
        if self.current_page_num < len(doc) - 1:
            self.current_page_num += 1
            self.display_page()
