import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog, messagebox, Listbox, Button, Label, Entry, Scrollbar, RIGHT, Y, END, Frame, SINGLE
from pdf_viewer import PDFViewer
from thumbnail_viewer import ThumbnailViewer

class PDFRecombiner:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Recombiner")

        self.pdf_files = []  # List of tuples (file_path, num_pages)
        self.selected_pages = {}  # Dictionary with file_path as key and list of page ranges as value

        self.viewer = PDFViewer(root)
        self.thumbnail_viewer = ThumbnailViewer(root, self.add_page_from_thumbnail)

        self.add_widgets()

    def add_widgets(self):
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_rowconfigure(9, weight=1)
        self.root.grid_rowconfigure(10, weight=1)

        frame = Frame(self.root)
        frame.grid(row=0, column=2, rowspan=9, sticky="nsew")

        # Select PDFs button
        self.select_pdfs_btn = Button(frame, text="Select PDFs", command=self.select_pdfs)
        self.select_pdfs_btn.grid(row=0, column=0, columnspan=2, pady=5)

        # PDF listbox
        self.pdf_listbox = Listbox(frame, selectmode=SINGLE, width=50, height=5)
        self.pdf_listbox.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        # Scrollbar for PDF listbox
        self.scrollbar = Scrollbar(frame, orient="vertical")
        self.scrollbar.config(command=self.pdf_listbox.yview)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.pdf_listbox.config(yscrollcommand=self.scrollbar.set)

        # Label for page selection
        self.page_selection_label = Label(frame, text="Enter page ranges (e.g., 1-3,5):")
        self.page_selection_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Page ranges entry
        self.page_ranges_entry = Entry(frame, width=50)
        self.page_ranges_entry.grid(row=3, column=0, columnspan=2, pady=5)

        # Add page ranges button
        self.add_page_ranges_btn = Button(frame, text="Add Page Ranges", command=self.add_page_ranges)
        self.add_page_ranges_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Remove page ranges button
        self.remove_page_ranges_btn = Button(frame, text="Remove Selected Range", command=self.remove_page_ranges)
        self.remove_page_ranges_btn.grid(row=5, column=0, columnspan=2, pady=5)

        # Selected ranges listbox
        self.selected_ranges_listbox = Listbox(frame, width=50, height=5)
        self.selected_ranges_listbox.grid(row=6, column=0, columnspan=2, pady=5)

        # Combine PDFs button
        self.combine_pdfs_btn = Button(frame, text="Combine selected pages", command=self.combine_pdfs, bg="#ff7e47", font=("Helvetica", 14), height=3, width=20)
        self.combine_pdfs_btn.grid(row=7, column=0, columnspan=2, pady=5)

    def select_pdfs(self):
        file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        for file_path in file_paths:
            if file_path not in [pdf[0] for pdf in self.pdf_files]:
                try:
                    pdf_reader = PdfReader(file_path)
                    num_pages = len(pdf_reader.pages)
                    self.pdf_files.append((file_path, num_pages))
                    self.pdf_listbox.insert(END, f"{os.path.basename(file_path)} ({num_pages} pages)")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not read {file_path}: {e}")

        self.pdf_listbox.bind('<<ListboxSelect>>', self.on_pdf_select)

    def on_pdf_select(self, event):
        selected_indices = self.pdf_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            pdf_path, _ = self.pdf_files[selected_index]
            self.viewer.load_pdf(pdf_path)
            self.thumbnail_viewer.load_thumbnails(pdf_path)

    def add_page_ranges(self):
        selected_indices = self.pdf_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No PDF selected. Please select at least one PDF.")
            return

        page_ranges = self.page_ranges_entry.get()
        if not page_ranges or not self.validate_page_ranges(page_ranges):
            messagebox.showerror("Error", "Invalid page ranges specified.")
            return

        for index in selected_indices:
            file_name, _ = self.pdf_files[index]
            if file_name in self.selected_pages:
                self.selected_pages[file_name].append(page_ranges)
            else:
                self.selected_pages[file_name] = [page_ranges]

            self.update_selected_ranges_listbox()

        self.page_ranges_entry.delete(0, END)

    def add_page_from_thumbnail(self, page_num):
        selected_indices = self.pdf_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No PDF selected. Please select at least one PDF.")
            return

        for index in selected_indices:
            file_name, _ = self.pdf_files[index]
            page_range = str(page_num + 1)
            if file_name in self.selected_pages:
                self.selected_pages[file_name].append(page_range)
            else:
                self.selected_pages[file_name] = [page_range]

            self.update_selected_ranges_listbox()

    def remove_page_ranges(self):
        selected_indices = self.selected_ranges_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No range selected. Please select a range to remove.")
            return

        selected_text = self.selected_ranges_listbox.get(selected_indices[0])
        display_name, ranges = selected_text.split(':')
        display_name = display_name.strip()
        range_texts = [r.strip() for r in ranges.split(', ')]

        file_name = next((file_path for file_path, _ in self.pdf_files if os.path.basename(file_path) in display_name), None)

        print(f"Attempting to remove range from {file_name}: {range_texts}")
        print(f"Current selected pages: {self.selected_pages}")

        if file_name and file_name in self.selected_pages:
            for range_text in range_texts:
                if range_text in self.selected_pages[file_name]:
                    self.selected_pages[file_name].remove(range_text)
                    print(f"Removed range {range_text} from {file_name}")
            if not self.selected_pages[file_name]:
                del self.selected_pages[file_name]
                print(f"Removed {file_name} from selected pages")
            self.update_selected_ranges_listbox()
        else:
            print(f"{file_name} not found in selected pages")

    def update_selected_ranges_listbox(self):
        self.selected_ranges_listbox.delete(0, END)
        for file_name, ranges in self.selected_pages.items():
            display_text = f"{os.path.basename(file_name)}: {', '.join(ranges)}"
            self.selected_ranges_listbox.insert(END, display_text)
        print(f"Updated selected ranges listbox: {self.selected_pages}")

    def validate_page_ranges(self, page_ranges):
        try:
            for part in page_ranges.split(','):
                if '-' in part:
                    start, end = part.split('-')
                    if int(start) < 1 or int(end) < 1:
                        return False
                else:
                    if int(part) < 1:
                        return False
            return True
        except ValueError:
            return False

    def parse_page_ranges(self, page_ranges):
        pages = set()
        for part in page_ranges.split(','):
            if '-' in part:
                start, end = part.split('-')
                pages.update(range(int(start) - 1, int(end)))
            else:
                pages.add(int(part) - 1)
        return sorted(pages)

    def combine_pdfs(self):
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Combined PDF As"
        )

        if not output_file:
            messagebox.showerror("Error", "No output file specified. Exiting.")
            return

        pdf_writer = PdfWriter()
        pages_added = 0

        for file_name, page_ranges_list in self.selected_pages.items():
            pdf_reader = PdfReader(file_name)
            for page_ranges in page_ranges_list:
                pages = self.parse_page_ranges(page_ranges)
                for page_num in pages:
                    if page_num < len(pdf_reader.pages):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                        pages_added += 1

        if pages_added > 0:
            with open(output_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            messagebox.showinfo("Success", f"Combined PDF saved as {output_file}")
        else:
            messagebox.showerror("Error", "No PDF pages found to write to the output file.")
