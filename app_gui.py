import tkinter
import customtkinter as ctk
from tkinter import filedialog
import threading
import os
from pdf_processor import create_4_in_1_pdf

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF 4-in-1 Tool")
        self.geometry("500x600")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)

        # --- File Selection ---
        self.file_path_label = ctk.CTkLabel(self, text="PDF File:")
        self.file_path_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.file_path_entry = ctk.CTkEntry(self, placeholder_text="Select a PDF file")
        self.file_path_entry.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")
        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=20, pady=(20, 5))

        # --- Page Options ---
        self.page_options_label = ctk.CTkLabel(self, text="Page Selection:")
        self.page_options_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.page_options_menu = ctk.CTkOptionMenu(self, values=["Odd", "Even"])
        self.page_options_menu.grid(row=1, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Layout Options ---
        self.layout_label = ctk.CTkLabel(self, text="Layout:")
        self.layout_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.layout_menu = ctk.CTkOptionMenu(self, values=["Layout 1 (A-B, C-D)", "Layout 2 (B-A, D-C)"])
        self.layout_menu.grid(row=2, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Auto Rotate ---
        self.rotate_label = ctk.CTkLabel(self, text="Auto Rotate:")
        self.rotate_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.rotate_checkbox = ctk.CTkCheckBox(self, text="Rotate landscape pages", onvalue=True, offvalue=False)
        self.rotate_checkbox.select() # Default to True
        self.rotate_checkbox.grid(row=3, column=1, columnspan=2, padx=20, pady=5, sticky="w")

        # --- Crop Margins ---
        self.crop_label = ctk.CTkLabel(self, text="Crop (T R B L in mm):")
        self.crop_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.crop_entry = ctk.CTkEntry(self, placeholder_text="e.g., 5 5 5 5")
        self.crop_entry.insert(0, "0 0 0 0")
        self.crop_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Gutter Settings ---
        self.gutter_side_label = ctk.CTkLabel(self, text="Binding Gutter:")
        self.gutter_side_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.gutter_side_menu = ctk.CTkOptionMenu(self, values=["None", "Right", "Left"])
        self.gutter_side_menu.grid(row=5, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        self.gutter_offset_label = ctk.CTkLabel(self, text="Gutter Offset (mm):")
        self.gutter_offset_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.gutter_offset_entry = ctk.CTkEntry(self, placeholder_text="e.g., 10")
        self.gutter_offset_entry.insert(0, "0")
        self.gutter_offset_entry.grid(row=6, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Create Button ---
        self.create_button = ctk.CTkButton(self, text="Create PDF", command=self.start_processing)
        self.create_button.grid(row=7, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # --- Status Bar ---
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=(("PDF Files", "*.pdf"), ("All files", "*.*"))
        )
        if file_path:
            self.file_path_entry.delete(0, tkinter.END)
            self.file_path_entry.insert(0, file_path)

    def start_processing(self):
        # Disable button to prevent multiple clicks
        self.create_button.configure(state="disabled", text="Processing...")
        self.status_label.configure(text="Starting process...", text_color="gray")

        # Run the PDF creation in a separate thread to avoid freezing the GUI
        thread = threading.Thread(target=self.run_pdf_creation)
        thread.daemon = True
        thread.start()

    def run_pdf_creation(self):
        try:
            # --- Get all values from the UI ---
            pdf_path = self.file_path_entry.get().strip()
            if not os.path.exists(pdf_path):
                raise ValueError("PDF file not found.")

            page_type = self.page_options_menu.get().lower()
            layout_choice = "1" if "Layout 1" in self.layout_menu.get() else "2"
            rotate_landscape = self.rotate_checkbox.get()

            crop_str = self.crop_entry.get().strip()
            crop_values = [float(v) for v in crop_str.split()]
            if len(crop_values) != 4:
                raise ValueError("Crop margins must have 4 values.")

            gutter_side_str = self.gutter_side_menu.get()
            if gutter_side_str == "Right":
                gutter_side = "1"
            elif gutter_side_str == "Left":
                gutter_side = "2"
            else:
                gutter_side = "0"

            gutter_offset = float(self.gutter_offset_entry.get().strip() or "0")

            # --- Call the processor ---
            output_path = create_4_in_1_pdf(
                pdf_path,
                page_type,
                layout_choice,
                crop_values,
                gutter_side,
                gutter_offset,
                rotate_landscape
            )

            # --- Update UI on success ---
            self.status_label.configure(text=f"✅ Success! Saved to: {os.path.basename(output_path)}", text_color="green")

        except Exception as e:
            # --- Update UI on error ---
            self.status_label.configure(text=f"❌ Error: {e}", text_color="red")

        finally:
            # --- Re-enable button ---
            self.create_button.configure(state="normal", text="Create PDF")

if __name__ == "__main__":
    app = App()
    app.mainloop()