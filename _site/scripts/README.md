# MESGRO Scripts

Utility scripts for the MESGRO (Mechanical, Electrical, Software Gallery for Robots) project.

## 📂 Where to Put Your Files

All converted models should go in the `assets/` folder:

```
assets/
├── images/projects/your-project/    # Project images
│   ├── featured.jpg                 # Main image
│   └── gallery/                     # Additional photos
├── models/your-project/             # 🤖 3D Models (GLTF/GLB)
│   ├── base.gltf                    # Converted from STL/STEP
│   └── assembly.gltf
└── schematics/your-project/         # ⚡ Circuit diagrams
    └── main-board.svg
```

---

## CAD-to-GLTF Converter

Converts CAD files (STL, STEP) to optimized GLTF format for web-based 3D viewing on GitHub Pages.

### Supported Formats

| Format | Extension | Status | Notes |
|--------|-----------|--------|-------|
| STL | `.stl` | ✅ Fully Supported | Universal mesh format |
| STEP | `.step`, `.stp` | ✅ Fully Supported | CAD exchange format |
| SolidWorks | `.sldprt`, `.sldasm` | ❌ Not Supported | Export to STL/STEP first |
| Autodesk | `.f3d`, `.iam`, `.ipt` | ❌ Not Supported | Export to STL/STEP first |

> **Why are SolidWorks and Autodesk formats not supported?**
> 
> These are proprietary, closed-source formats. No open-source Python libraries exist to read them because:
> 1. File format specifications are not publicly documented
> 2. Reading them would require reverse-engineering or licensing agreements
> 3. They contain parametric/feature data, not just geometry
>
> **Solution:** Export your models to STL or STEP from your CAD software:
> - **SolidWorks:** File → Save As → STL or STEP
> - **Fusion 360:** File → Export → STL or STEP
> - **Inventor:** File → Export → CAD Format → STL or STEP

### Installation

#### Option 1: Using Conda (Recommended)

```powershell
# Create conda environment
conda create -n mesgro python=3.11 -y

# Activate environment
conda activate mesgro

# Install dependencies
pip install -r scripts/requirements.txt
```

#### Option 2: Using pip directly

```bash
pip install trimesh numpy cadquery-ocp
```

### Usage

#### Basic Conversion

```powershell
# Activate conda environment first
conda activate mesgro

# Convert STL to GLTF
python scripts/cad_to_gltf.py -i model.stl -o output.gltf

# Convert STEP to GLTF
python scripts/cad_to_gltf.py -i assembly.step -o output.gltf
```

#### Check STEP Support

```powershell
python scripts/cad_to_gltf.py --check-step
```

#### Command Line Options

| Option | Description |
|--------|-------------|
| `-i`, `--input_file` | Input CAD file (.stl, .step, .stp) |
| `-o`, `--output_file` | Output GLTF file |
| `--check-step` | Check if STEP support is installed |
| `-h`, `--help` | Show help message |

### Examples

```powershell
# Convert a robot arm STL
python scripts/cad_to_gltf.py -i assets/models/robotic-arm/base.stl -o assets/models/robotic-arm/base.gltf

# Convert a STEP assembly
python scripts/cad_to_gltf.py -i designs/sensor-housing.step -o assets/models/iot-monitor/housing.gltf

# Batch convert multiple files (PowerShell)
Get-ChildItem -Filter "*.stl" | ForEach-Object {
    $output = $_.BaseName + ".gltf"
    python scripts/cad_to_gltf.py -i $_.FullName -o $output
}
```

### Output Format

The converter outputs GLTF files with:
- **Embedded binary data** - No external `.bin` files needed
- **Optimized mesh** - Merged vertices, removed degenerate faces
- **Web-ready** - Compatible with Google Model Viewer and three.js

### Troubleshooting

#### "STEP support not installed"

Install the OpenCASCADE bindings:
```powershell
pip install cadquery-ocp
```

#### "Module not found: trimesh"

Install core dependencies:
```powershell
pip install trimesh numpy
```

#### Large output file size

For very large models, consider:
1. Simplifying the mesh in your CAD software before export
2. Using mesh decimation tools
3. Exporting at lower resolution from CAD software

---

## SPICE-to-SVG Schematic Generator

Converts SPICE netlists to SVG schematics. See `spice_to_svg.py` for usage.

---

## Dependencies

All dependencies are listed in `requirements.txt`:

```
trimesh>=4.0.0      # Mesh loading and GLTF export
numpy>=1.24.0       # Numerical operations
cadquery-ocp>=7.8.0 # STEP file support (OpenCASCADE)
```
