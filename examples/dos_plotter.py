#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Density of States (DOS) Plotter with Automatic Band Gap Detection

Author:
    Ashen Deemantha Liyanage

Affiliation:
    Zayak's Lab
    Department of Physics and Astronomy
    Bowling Green State University (BGSU)

GitHub:
    https://github.com/ashendeema

Description:
    A Python tool for visualizing electronic Density of States (DOS)
    data from one or more .DOS files.

Features:
    - Automatic detection of all .DOS files in the working directory
    - User-defined Fermi level alignment (EF = 0 eV)
    - Automatic band gap detection
    - Support for single and multiple DOS datasets
    - Publication-quality DOS plots
    - Optional Fermi level and band edge visualization
    - High-resolution PNG output

Input Format:
    Column 1 : Energy (eV)
    Column 2 : DOS

    Additional DOS columns are automatically summed if present.

Usage:
    Place one or more .DOS files in the same folder as this script
    and run:

        python dos_plotter.py

    The script will prompt for the Fermi level and generate
    a DOS plot saved as a PNG image.

Developed for:
    Electronic structure analysis from DFT calculations
    (e.g., SIESTA, Quantum ESPRESSO, VASP, and related codes).

Version:
    1.0.0

License:
    MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Plot styling
# -----------------------
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

# -----------------------
# Step 1: Ask user for Fermi level
# -----------------------
try:
    fermi_level = float(input("Enter the Fermi level value (eV): "))
except ValueError:
    print("Invalid input. Please enter a numeric value for the Fermi level.")
    exit()

# -----------------------
# Step 2: Colors (fill color, line color)
# -----------------------
colors = [
    ('lightgreen', 'green'),
    ('lightcoral', 'red'),
    ('lightblue', 'blue'),
    ('plum', 'purple'),
    ('khaki', 'orange'),
    ('lightcyan', 'cyan'),
    ('lightpink', 'magenta')
]

# -----------------------
# Step 3: Find all .DOS files
# -----------------------
dos_files = sorted(glob.glob("*.DOS"))
if not dos_files:
    print("No .DOS files with extension .DOS found in this folder.")
    exit()

# Store gap info for each dataset
dataset_gaps = {}

# -----------------------
# Step 4: Create figure
# -----------------------
plt.figure(figsize=(8, 6))

# -----------------------
# Step 5: Loop through each DOS file
# -----------------------
for i, fname in enumerate(dos_files):
    try:
        data = np.loadtxt(fname)
    except Exception:
        # fallback for messy text files
        data_lines = []
        with open(fname, 'r') as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    vals = [float(p) for p in line.split()]
                    data_lines.append(vals)
                except ValueError:
                    continue
        if not data_lines:
            continue
        data = np.array(data_lines)

    if data.ndim == 1 or data.shape[1] < 2:
        continue

    # Energy column + DOS column(s)
    energy = data[:, 0].astype(float)
    dos = np.sum(data[:, 1:], axis=1).astype(float) if data.shape[1] > 2 else data[:, 1].astype(float)

    # Sort by energy
    sort_idx = np.argsort(energy)
    energy = energy[sort_idx]
    dos = dos[sort_idx]

    # Shift energy so Fermi level = 0
    energy_shifted = energy - fermi_level

    # -----------------------
    # Step 5a: Detect band gap (DOS ~ 0)
    # -----------------------
    max_dos = np.max(dos) if dos.size else 0.0
    tol = max(1e-8, max_dos * 1e-6)  # adaptive threshold
    mask_zero = dos <= tol
    zero_idx = np.where(mask_zero)[0]

    gap_width = None
    lower_edge = None
    upper_edge = None

    if zero_idx.size > 0:
        runs = np.split(zero_idx, np.where(np.diff(zero_idx) != 1)[0] + 1)
        # Choose run spanning EF if possible
        chosen_run = None
        for run in runs:
            if energy_shifted[run[0]] <= 0 <= energy_shifted[run[-1]]:
                chosen_run = run
                break
        if chosen_run is None:
            chosen_run = max(runs, key=lambda r: r.size)

        lower_edge = energy_shifted[chosen_run[0]]
        upper_edge = energy_shifted[chosen_run[-1]]
        gap_width = upper_edge - lower_edge

    dataset_gaps[os.path.splitext(os.path.basename(fname))[0]] = (
        (lower_edge, upper_edge) if gap_width is not None else None
    )

    # -----------------------
    # Step 5b: Plot DOS curve
    # -----------------------
    fill_color, line_color = colors[i % len(colors)]
    label = os.path.splitext(os.path.basename(fname))[0]

    plt.fill_between(energy_shifted, dos, color=fill_color, alpha=0.45)
    plt.plot(energy_shifted, dos, color=line_color, linewidth=1.5, label=label)

    # -----------------------
    # Step 5c: OPTIONAL dashed lines
    # -----------------------
    if gap_width is not None:
        # Optional: Fermi level dashed line
         plt.axvline(0.0, color='black', linestyle='--', linewidth=1.2, label="Fermi Level")       
        # Optional: Lower and upper band edge dashed lines
#         plt.axvline(lower_edge, color='gray', linestyle='--', linewidth=1.2, label="Lower Band Edge")
#         plt.axvline(upper_edge, color='brown', linestyle='--', linewidth=1.2, label="Upper Band Edge")

# -----------------------
# Step 5d: OPTIONAL band gap arrow with value
# -----------------------
#for dataset_name, edges in dataset_gaps.items():
#     if edges is None:
#         continue
#     lo_edge, hi_edge = edges
#     gap = hi_edge - lo_edge
#
#     # vertical placement of the arrow (90% of max DOS)
#     mid_y = max(dos) * 0.3
#     # Draw the double-headed arrow
#     plt.annotate(
#         '', xy=(hi_edge, mid_y), xytext=(lo_edge, mid_y),
#         arrowprops=dict(arrowstyle='<->', color='red', lw=1.5)
#     )
#
#     # Place the gap text in a box above the arrow
#     plt.text(
#         0.5 * (lo_edge + hi_edge), mid_y + max(dos) * 0.02,
#         f"Band Gap = {gap:.2f} eV",
#         ha='center', va='bottom', fontsize=12,
#         fontname="Times New Roman", color='red',
#         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7)
#     )

# -----------------------
# Step 6: Print band gap width
# -----------------------
#print("\nDetected band gap widths (per dataset):")
#for name, edges in dataset_gaps.items():
#    if edges is None:
#        print(f"  {name}: No band gap detected")
#    else:
#        lo_edge, hi_edge = edges
#        print(f"  {name}: Band gap = {hi_edge - lo_edge:.6f} eV")

# -----------------------
# Step 7: Labels and title
# -----------------------
if len(dos_files) == 1:
    title_name = f"Density of States of {os.path.splitext(dos_files[0])[0]}"
else:
    names = [os.path.splitext(os.path.basename(f))[0] for f in dos_files]
    title_name = "Density of States of " + " VS ".join(names)

plt.title(title_name, fontname="Times New Roman", fontsize=16, fontweight="bold")
plt.xlabel("Energy - E$_F$ (eV)", fontname="Times New Roman", fontsize=14)
plt.ylabel("DOS (states/eV)", fontname="Times New Roman", fontsize=14)

# Optional: Manual axis limits
plt.xlim(-5, 5)
#plt.ylim(0, 7)

# -----------------------
# Step 8: Legend, save, show
# -----------------------
plt.legend(fontsize=11)
png_name = title_name.replace(" ", "_") + ".png"
plt.tight_layout()
plt.savefig(png_name, dpi=300, bbox_inches='tight')
plt.show()

print(f"\nPlot saved as: {png_name}")

print("\n----------------------------------------")
print("Density of States (DOS) Plotter v1.0.0")
print("Developed by Ashen Deemantha Liyanage")
print("Zayak's Lab, Department of Physics and Astronomy, BGSU")
print("GitHub: https://github.com/ashendeema")
print("----------------------------------------")

