from tkinter import Tk
from pdf_recombiner import PDFRecombiner

def main():
    root = Tk()
    app = PDFRecombiner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
