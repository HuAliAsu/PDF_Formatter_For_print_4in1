
# 🧩 PDF_Formatter_For_print_4in1

**T_PDF_in_4_Pages_Pro** is a Python script that rearranges pages from any PDF file into a **4-in-1 layout** on A4 paper.
It includes advanced options such as cropping margins, gutter binding offsets, and automatic rotation for landscape pages.

---

## 🚀 Features

| Feature                        | Description                                                        |
| ------------------------------ | ------------------------------------------------------------------ |
| 📄 **4-in-1 Page Layout**      | Combine four PDF pages into one A4 page                            |
| 🔢 **Odd / Even Selection**    | Choose whether to include only odd or even pages                   |
| 📐 **Automatic Scaling**       | Pages are automatically scaled to fit each quadrant                |
| ✂️ **Margin Cropping**         | Trim margins before merging (top/right/bottom/left in millimeters) |
| 🔁 **Automatic Rotation**      | Rotate landscape-oriented pages automatically                      |
| 📏 **Gutter (Binding Offset)** | Shift all pages left or right to leave space for book binding      |
| 🧩 **Two Layout Styles**       | Choose between Layout 1 (A-B / C-D) or Layout 2 (B-A / D-C)        |
| ⚙️ **PyPDF Compatibility**     | Works with both `pypdf` and `PyPDF2` libraries                     |

---

## 📦 Requirements

* Python **3.9+**
* One of the following libraries:

  * [`pypdf`](https://pypi.org/project/pypdf/)
  * or [`PyPDF2`](https://pypi.org/project/PyPDF2/)

Install with:

```bash
pip install pypdf
# or
pip install PyPDF2
```

---

## 💻 Usage

Run the script in a terminal:

```bash
python T_PDF_in_4_Pages_Pro.py
```

Then follow the prompts:

```
Enter full PDF path: "C:\Users\John\Desktop\MyFile.pdf"
Select pages (1=Odd, 2=Even): 1
Choose layout (1 or 2):
Layout 1:
  A-B
  C-D

Layout 2:
  B-A
  D-C
Your choice: 1

Crop margins (top right bottom left in mm, e.g. 5 5 5 5 or 0 0 0 0): 3 3 3 3
Binding side (1=Right, 2=Left, 0=None): 2
Enter offset amount in mm: 5
Rotate landscape pages automatically? (y/n): y
```

---

## 🧾 Output

A new file will be saved in the same folder as the original PDF,
with a name like:

```
MyFile_4in1_odd_layout1.pdf
```

Each A4 page will contain up to four smaller PDF pages, arranged according to the selected layout.

---

## 🧠 Notes

* If your PDF is **encrypted**, please remove the password protection before running this script.
* All page dimensions and offsets are converted automatically from **millimeters** to PDF **points (1 inch = 72 points)**.
* The script detects whether you have `pypdf` or `PyPDF2` installed and works with either.

---

## 🧰 Example Layouts

**Layout 1:**

```
A-B
C-D
```

**Layout 2:**

```
B-A
D-C
```

---

## 📜 License

This project is released under the **MIT License**.
You’re free to use, modify, and distribute it — just keep this notice.

---

Would you like me to include **example images** of Layout 1 and Layout 2 (auto-generated diagrams) inside the README too?
