#!/usr/bin/env python3
# kpi_bar_pdf.py — make a simple bar chart (PDF, 600 dpi) from the CSV summary
#e/g/ python kpi_bar_pdf.py summary.csv fr_by_file.pdf
import csv, matplotlib.pyplot as plt, sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python kpi_bar_pdf.py <summary.csv> <out.pdf>", file=sys.stderr)
        sys.exit(2)
    labels, fr_vals = [], []
    with open(sys.argv[1]) as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            labels.append(row["file"].replace(".jsonl",""))
            fr_vals.append(float(row["FR"]))
    plt.figure()
    plt.bar(labels, fr_vals)
    plt.ylabel("False-RMA Rate")
    plt.title("FR by JSONL file")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(sys.argv[2], format="pdf", dpi=600)
    plt.close()

