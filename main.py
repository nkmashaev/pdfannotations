import fitz
import argparse


def extract_annotations(pdf_path, out_file):
    doc = fitz.open(pdf_path)
    
    with open(out_file, "w") as f:
        for page_num, page in enumerate(doc, 1):
            annotations = page.annots()
            if not annotations:
                continue
            for annot in annotations:
                if annot.type[0] == 8:
                    highlight_text = page.get_text("text", clip=annot.rect)
                    note_text = annot.info.get("content", "")
                    f.write(f"> {highlight_text.strip()} (pp.{page_num})\n")
                    if note_text:
                        f.write(f"- {note_text.strip()}\n")
                    f.write("-" * 80 + "\n\n")


def main():
    parser = argparse.ArgumentParser(description="Extract highlights and notes from a PDF file.")
    parser.add_argument("pdf_path", help="Path to the PDF file to extract annotations from")
    parser.add_argument(
        "-o", "--output", default="output_annotations.txt",
        help="Optional output file to save the annotations (default: output_annotations.txt)"
    )

    args = parser.parse_args()
    extract_annotations(args.pdf_path, args.output)


if __name__ == "__main__":
    main()