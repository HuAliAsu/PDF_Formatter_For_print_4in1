# 🧩 PDF Formatter for Pocket Book Printing (4-in-1)

This application provides a user-friendly graphical interface to rearrange pages from any PDF file into a **4-in-1 layout** on A4 paper. It is designed to help with printing pocket-sized books (A6) on a standard A4 printer.

The tool includes advanced options such as individual margin cropping, gutter binding offsets, automatic rotation for landscape pages, and special features for home printing.

![App Screenshot](https://i.imgur.com/your-screenshot.png) <!-- Placeholder for a future screenshot -->

---

## 🚀 Features

| Feature                          | Description                                                              |
| -------------------------------- | ------------------------------------------------------------------------ |
| 🖥️ **Graphical User Interface**  | Easy-to-use interface built with CustomTkinter.                          |
| 📄 **4-in-1 Page Layout**        | Combine four PDF pages into one A4 page.                                 |
| 📚 **Page Selection**            | Process all, odd, or even pages.                                         |
| 📐 **Automatic Scaling**         | Pages are automatically scaled to fit each quadrant.                     |
| ✂️ **Individual Margin Cropping**| Trim each margin (top, right, bottom, left) independently in millimeters.|
| 🔁 **Automatic Rotation**         | Rotate landscape-oriented pages automatically.                           |
| 📏 **Binding Gutter**            | Add extra space to the inner margin for bookbinding.                     |
| 🔄 **Reverse Order Printing**   | Reverse the order of page chunks for specific printer models.            |
| 📂 **File Versioning**           | Avoids overwriting files by creating new versions (e.g., `file_v2.pdf`).   |

---

## 📦 Requirements

*   Python **3.9+**
*   Dependencies listed in `requirements.txt`.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

To run the application, execute the `app_gui.py` script:

```bash
python app_gui.py
```

This will open the graphical user interface where you can select your PDF file and configure the processing options.

---

## 🛠️ How to Create an Executable (`.exe`)

You can create a standalone executable file using `PyInstaller`. This allows you to run the application on Windows without needing a Python installation.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Build the Executable:**
    Run the following command in your terminal from the project's root directory. The `--noconsole` flag prevents the command prompt from opening when you run the app, and `--onefile` bundles everything into a single `.exe` file.

    ```bash
    pyinstaller --name "PDF_Formatter" --onefile --noconsole app_gui.py
    ```

3.  **Find the Executable:**
    The final executable file, `PDF_Formatter.exe`, will be located in the `dist` folder that PyInstaller creates.

---

## 📜 License

This project is released under the **MIT License**.
You’re free to use, modify, and distribute it.