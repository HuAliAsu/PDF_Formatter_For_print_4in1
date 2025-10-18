import tkinter
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import sys
from pdf_processor import create_4_in_1_pdf

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF 4-in-1 Tool for Pocket Books")
        self.geometry("550x780")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)

        self.output_folder = "" # To store the last output folder

        # --- Help Button ---
        self.help_button = ctk.CTkButton(self, text="  Help  ", command=self.show_help)
        self.help_button.grid(row=0, column=2, padx=(0, 20), pady=(20, 5), sticky="e")

        # --- File Selection ---
        self.file_path_label = ctk.CTkLabel(self, text="PDF File:")
        self.file_path_label.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="w")
        self.file_path_entry = ctk.CTkEntry(self, placeholder_text="Select a PDF file")
        self.file_path_entry.grid(row=1, column=1, padx=20, pady=(5, 5), sticky="ew")
        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, padx=20, pady=(5, 5))

        # --- Page Options ---
        self.page_options_label = ctk.CTkLabel(self, text="Page Selection:")
        self.page_options_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.page_options_menu = ctk.CTkOptionMenu(self, values=["All", "Odd", "Even"])
        self.page_options_menu.grid(row=2, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Layout Options ---
        self.layout_label = ctk.CTkLabel(self, text="Layout:")
        self.layout_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.layout_menu = ctk.CTkOptionMenu(self, values=["Layout 1 (A-B, C-D)", "Layout 2 (B-A, D-C)"])
        self.layout_menu.grid(row=3, column=1, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- Advanced Options Frame ---
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)

        # --- Auto Rotate ---
        self.rotate_checkbox = ctk.CTkCheckBox(self.options_frame, text="Auto-rotate landscape pages", onvalue=True, offvalue=False)
        self.rotate_checkbox.select()
        self.rotate_checkbox.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # --- Reverse Order ---
        self.reverse_checkbox = ctk.CTkCheckBox(self.options_frame, text="Reverse page chunk order (for specific printers)", onvalue=True, offvalue=False)
        self.reverse_checkbox.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # --- Crop Margins Frame ---
        self.crop_frame = ctk.CTkFrame(self)
        self.crop_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.crop_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.crop_label = ctk.CTkLabel(self.crop_frame, text="Crop Margins (mm):")
        self.crop_label.grid(row=0, column=0, columnspan=4, padx=15, pady=(10, 0), sticky="w")

        # Labels for crop entries
        self.crop_top_label = ctk.CTkLabel(self.crop_frame, text="Top")
        self.crop_top_label.grid(row=1, column=0, padx=5, pady=(5,0), sticky="s")
        self.crop_right_label = ctk.CTkLabel(self.crop_frame, text="Right")
        self.crop_right_label.grid(row=1, column=1, padx=5, pady=(5,0), sticky="s")
        self.crop_bottom_label = ctk.CTkLabel(self.crop_frame, text="Bottom")
        self.crop_bottom_label.grid(row=1, column=2, padx=5, pady=(5,0), sticky="s")
        self.crop_left_label = ctk.CTkLabel(self.crop_frame, text="Left")
        self.crop_left_label.grid(row=1, column=3, padx=5, pady=(5,0), sticky="s")

        # Crop entries
        self.crop_top_entry = ctk.CTkEntry(self.crop_frame, placeholder_text="Top")
        self.crop_top_entry.grid(row=2, column=0, padx=5, pady=(0,10), sticky="ew")
        self.crop_right_entry = ctk.CTkEntry(self.crop_frame, placeholder_text="Right")
        self.crop_right_entry.grid(row=2, column=1, padx=5, pady=(0,10), sticky="ew")
        self.crop_bottom_entry = ctk.CTkEntry(self.crop_frame, placeholder_text="Bottom")
        self.crop_bottom_entry.grid(row=2, column=2, padx=5, pady=(0,10), sticky="ew")
        self.crop_left_entry = ctk.CTkEntry(self.crop_frame, placeholder_text="Left")
        self.crop_left_entry.grid(row=2, column=3, padx=5, pady=(0,10), sticky="ew")

        for entry in [self.crop_top_entry, self.crop_right_entry, self.crop_bottom_entry, self.crop_left_entry]:
            entry.insert(0, "0")

        # --- Gutter Settings Frame ---
        self.gutter_frame = ctk.CTkFrame(self)
        self.gutter_frame.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.gutter_frame.grid_columnconfigure(1, weight=1)

        self.gutter_side_label = ctk.CTkLabel(self.gutter_frame, text="Binding Gutter:")
        self.gutter_side_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.gutter_side_menu = ctk.CTkOptionMenu(self.gutter_frame, values=["None", "Right", "Left"], command=self.toggle_gutter_offset)
        self.gutter_side_menu.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        self.gutter_offset_label = ctk.CTkLabel(self.gutter_frame, text="Gutter Offset (mm):")
        self.gutter_offset_entry = ctk.CTkEntry(self.gutter_frame, placeholder_text="e.g., 10")
        self.gutter_offset_entry.insert(0, "0")
        self.toggle_gutter_offset() # Set initial state

        # --- Action Buttons Frame ---
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=7, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)

        self.create_button = ctk.CTkButton(self.action_frame, text="Create PDF", command=self.start_processing)
        self.create_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.open_folder_button = ctk.CTkButton(self.action_frame, text="Open Output Folder", command=self.open_output_folder, state="disabled")
        self.open_folder_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

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
            self.output_folder = os.path.dirname(file_path)

    def toggle_gutter_offset(self, choice=None):
        if self.gutter_side_menu.get() == "None":
            self.gutter_offset_label.grid_remove()
            self.gutter_offset_entry.grid_remove()
        else:
            self.gutter_offset_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
            self.gutter_offset_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

    def show_help(self):
        help_text = (
            "This application helps you print pocket-sized books (A6) using a standard A4 printer.\n\n"
            "It arranges four original pages onto a single A4 sheet, which you can then print, cut, and fold.\n\n"
            "Key Features:\n\n"
            "- **Layouts:** Choose how pages are ordered on the sheet.\n\n"
            "- **Page Selection:** Print all, odd, or even pages.\n\n"
            "- **Crop:** Trim unwanted margins from the original pages.\n\n"
            "- **Gutter:** Add extra space to the inner margin for binding.\n\n"
            "- **Reverse Order:** Flips the order of the output pages. Useful for printers that don't reverse the stack automatically when printing double-sided."
        )
        messagebox.showinfo("How to Use", help_text)

    def open_output_folder(self):
        if self.output_folder and os.path.isdir(self.output_folder):
            try:
                if sys.platform == "win32":
                    os.startfile(self.output_folder)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", self.output_folder])
                else:
                    subprocess.Popen(["xdg-open", self.output_folder])
            except Exception as e:
                self.status_label.configure(text=f"❌ Error opening folder: {e}", text_color="red")

    def start_processing(self):
        self.create_button.configure(state="disabled", text="Processing...")
        self.open_folder_button.configure(state="disabled")
        self.status_label.configure(text="Starting process...", text_color="gray")
        thread = threading.Thread(target=self.run_pdf_creation)
        thread.daemon = True
        thread.start()

    def run_pdf_creation(self):
        try:
            pdf_path = self.file_path_entry.get().strip()
            if not os.path.exists(pdf_path):
                raise ValueError("PDF file not found.")

            self.output_folder = os.path.dirname(pdf_path)

            page_type = self.page_options_menu.get().lower()
            layout_choice = "1" if "Layout 1" in self.layout_menu.get() else "2"
            rotate_landscape = self.rotate_checkbox.get()
            reverse_order = self.reverse_checkbox.get()

            crop_values = [
                float(self.crop_top_entry.get() or 0),
                float(self.crop_right_entry.get() or 0),
                float(self.crop_bottom_entry.get() or 0),
                float(self.crop_left_entry.get() or 0)
            ]

            gutter_side_str = self.gutter_side_menu.get()
            gutter_side = "0"
            if gutter_side_str == "Right": gutter_side = "1"
            elif gutter_side_str == "Left": gutter_side = "2"

            gutter_offset = 0
            if self.gutter_side_menu.get() != "None":
                 gutter_offset = float(self.gutter_offset_entry.get().strip() or "0")

            output_path = create_4_in_1_pdf(
                pdf_path, page_type, layout_choice, crop_values,
                gutter_side, gutter_offset, rotate_landscape, reverse_order
            )

            self.status_label.configure(text=f"✅ Success! Saved to: {os.path.basename(output_path)}", text_color="green")
            self.open_folder_button.configure(state="normal")

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}", text_color="red")

        finally:
            self.create_button.configure(state="normal", text="Create PDF")

if __name__ == "__main__":
    app = App()
    app.mainloop()