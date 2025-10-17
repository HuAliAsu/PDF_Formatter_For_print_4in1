import os

# --- Import PyPDF2 or pypdf safely ---
try:
    from pypdf import PdfReader, PdfWriter, Transformation
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter, Transformation

# --- A4 size in millimeters ---
A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297

# Convert mm to points (1 inch = 72 points, 1 inch = 25.4 mm)
def mm_to_points(mm):
    return mm * 72 / 25.4

A4_WIDTH = mm_to_points(A4_WIDTH_MM)
A4_HEIGHT = mm_to_points(A4_HEIGHT_MM)


def create_4_in_1_pdf(pdf_path, page_type, layout_choice, crop_values, gutter_side, gutter_offset, rotate_landscape):
    """
    Creates a new 4-in-1 PDF with specified options.

    Args:
        pdf_path (str): The full path to the source PDF.
        page_type (str): 'odd' or 'even'.
        layout_choice (str): '1' or '2'.
        crop_values (list[float]): A list of 4 floats for crop margins [top, right, bottom, left] in mm.
        gutter_side (str): '1' for right, '2' for left, '0' for none.
        gutter_offset (float): The gutter offset in mm.
        rotate_landscape (bool): Whether to rotate landscape pages.

    Returns:
        str: The path to the newly created PDF file.

    Raises:
        Exception: If any error occurs during PDF processing.
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        # Select odd/even pages
        if page_type == "odd":
            page_indices = [i for i in range(total_pages) if (i + 1) % 2 != 0]
        else:
            page_indices = [i for i in range(total_pages) if (i + 1) % 2 == 0]

        if not page_indices:
            raise ValueError(f"No '{page_type}' pages found in the document.")

        page_chunks = [page_indices[i:i + 4] for i in range(0, len(page_indices), 4)]

        # Convert offsets to points
        crop_top, crop_right, crop_bottom, crop_left = [mm_to_points(v) for v in crop_values]
        gutter_shift = mm_to_points(gutter_offset)

        for chunk in page_chunks:
            a4_page = writer.add_blank_page(width=A4_WIDTH, height=A4_HEIGHT)

            positions = {
                'A': (0, A4_HEIGHT / 2),
                'B': (A4_WIDTH / 2, A4_HEIGHT / 2),
                'C': (0, 0),
                'D': (A4_WIDTH / 2, 0)
            }

            order_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3} if layout_choice == '1' else {'A': 1, 'B': 0, 'C': 3, 'D': 2}

            for pos_key, page_index_in_chunk in order_map.items():
                if page_index_in_chunk >= len(chunk):
                    continue

                src_page = reader.pages[chunk[page_index_in_chunk]]

                # --- Optional auto rotation for landscape pages ---
                width = float(src_page.mediabox.width)
                height = float(src_page.mediabox.height)
                if rotate_landscape and width > height:
                    src_page.rotate(90)
                    width, height = height, width

                # --- Apply cropping (if any) ---
                if any(crop_values):
                    src_page.mediabox.lower_left = (
                        src_page.mediabox.left + crop_left,
                        src_page.mediabox.bottom + crop_bottom
                    )
                    src_page.mediabox.upper_right = (
                        src_page.mediabox.right - crop_right,
                        src_page.mediabox.top - crop_top
                    )
                    width = float(src_page.mediabox.width)
                    height = float(src_page.mediabox.height)

                # --- Compute scaling and position ---
                tx, ty = positions[pos_key]
                target_width = A4_WIDTH / 2
                target_height = A4_HEIGHT / 2
                scale_factor = min(target_width / width, target_height / height)

                # Center within its quadrant
                offset_x = tx + (target_width - width * scale_factor) / 2
                offset_y = ty + (target_height - height * scale_factor) / 2

                # --- Apply gutter offset (binding margin) ---
                if gutter_side == "1":  # right
                    offset_x += gutter_shift
                elif gutter_side == "2":  # left
                    offset_x -= gutter_shift

                # --- Apply transformation ---
                transformation = (
                    Transformation()
                    .scale(scale_factor, scale_factor)
                    .translate(offset_x, offset_y)
                )

                try:
                    a4_page.merge_transformed_page(src_page, transformation, expand=False)
                except AttributeError:
                    src_page.add_transformation(transformation)
                    a4_page.merge_page(src_page, expand=False)

        # --- Save file ---
        base_name = os.path.basename(pdf_path)
        dir_name = os.path.dirname(pdf_path)
        file_name, _ = os.path.splitext(base_name)
        output_filename = os.path.join(
            dir_name,
            f"{file_name}_4in1_{page_type}_layout{layout_choice}.pdf"
        )

        with open(output_filename, "wb") as f:
            writer.write(f)

        return output_filename

    except Exception as e:
        raise Exception(f"An error occurred during PDF processing: {e}")