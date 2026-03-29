#!/usr/bin/env python3
"""
CAD-to-GLTF Converter for MESGRO Project
=========================================

Converts STL and STEP files to optimized GLTF with embedded binary data
for GitHub Pages 3D visualization.

Supported Formats:
------------------
- STL (.stl) - Universal mesh format
- STEP/STP (.step, .stp) - CAD exchange format

Why Autodesk/SolidWorks formats are NOT supported:
--------------------------------------------------
Formats like .sldprt, .sldasm (SolidWorks) and .f3d, .iam, .ipt (Autodesk)
are PROPRIETARY and CLOSED-SOURCE. No open-source Python libraries exist
to read them because:
  1. File format specs are not publicly documented
  2. Reading them requires reverse-engineering or licensing
  3. They contain parametric/feature data, not just geometry

SOLUTION: Export to STL or STEP from your CAD software:
  - SolidWorks: File → Save As → STL or STEP
  - Fusion 360: File → Export → STL or STEP  
  - Inventor: File → Export → CAD Format → STL or STEP

Installation:
-------------
    pip install trimesh numpy cadquery-ocp

Usage:
------
    python cad_to_gltf.py -i model.stl -o output.gltf
    python cad_to_gltf.py -i assembly.step -o output.gltf
    python cad_to_gltf.py --check-step

Author: MESGRO Project
License: MIT
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

# =============================================================================
# Dependency Check
# =============================================================================

def check_step_support() -> Tuple[bool, Optional[str]]:
    """Check if STEP file support is available."""
    try:
        from OCP.STEPControl import STEPControl_Reader
        return True, "cadquery-ocp"
    except ImportError:
        pass
    
    try:
        from OCC.Core.STEPControl import STEPControl_Reader
        return True, "pythonocc-core"
    except ImportError:
        pass
    
    return False, None


# Check core dependencies
try:
    import numpy as np
    import trimesh
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Install with: pip install trimesh numpy")
    sys.exit(1)


# =============================================================================
# Supported Formats
# =============================================================================

SUPPORTED_FORMATS = {'.stl', '.step', '.stp'}


# =============================================================================
# Loaders
# =============================================================================

def load_stl(input_path: Path) -> trimesh.Trimesh:
    """Load an STL file."""
    print(f"  Loading STL: {input_path.name}")
    mesh = trimesh.load(str(input_path), file_type='stl', force='mesh')
    
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)
    
    return mesh


def load_step(input_path: Path) -> trimesh.Trimesh:
    """Load a STEP file using OpenCASCADE (cadquery-ocp)."""
    step_ok, library = check_step_support()
    
    if not step_ok:
        raise ImportError(
            "STEP support requires cadquery-ocp.\n"
            "Install with: pip install cadquery-ocp\n"
            "Or export your STEP to STL from CAD software."
        )
    
    print(f"  Loading STEP via {library}: {input_path.name}")
    
    # Import based on available library
    if library == "cadquery-ocp":
        from OCP.STEPControl import STEPControl_Reader
        from OCP.BRepMesh import BRepMesh_IncrementalMesh
        from OCP.TopExp import TopExp_Explorer
        from OCP.TopAbs import TopAbs_FACE
        from OCP.BRep import BRep_Tool
        from OCP.TopLoc import TopLoc_Location
    else:
        from OCC.Core.STEPControl import STEPControl_Reader
        from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
        from OCC.Core.TopExp import TopExp_Explorer
        from OCC.Core.TopAbs import TopAbs_FACE
        from OCC.Core.BRep import BRep_Tool
        from OCC.Core.TopLoc import TopLoc_Location
    
    # Read STEP
    reader = STEPControl_Reader()
    if reader.ReadFile(str(input_path)) != 1:
        raise ValueError(f"Failed to read STEP: {input_path}")
    
    reader.TransferRoots()
    shape = reader.OneShape()
    
    # Tessellate
    BRepMesh_IncrementalMesh(shape, 0.1)
    
    # Extract mesh
    vertices, faces = [], []
    offset = 0
    
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = explorer.Current()
        location = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, location)
        
        if tri:
            for i in range(1, tri.NbNodes() + 1):
                node = tri.Node(i)
                if not location.IsIdentity():
                    node = node.Transformed(location.Transformation())
                vertices.append([node.X(), node.Y(), node.Z()])
            
            for i in range(1, tri.NbTriangles() + 1):
                t = tri.Triangle(i)
                n1, n2, n3 = t.Get()
                faces.append([n1-1+offset, n2-1+offset, n3-1+offset])
            
            offset += tri.NbNodes()
        
        explorer.Next()
    
    return trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))


# =============================================================================
# Processing & Export
# =============================================================================

def optimize_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Optimize mesh for web viewing."""
    print("  Optimizing...")
    mesh.merge_vertices()
    # Use update_faces with a mask to remove degenerate/duplicate faces
    if hasattr(mesh, 'remove_degenerate_faces'):
        mesh.remove_degenerate_faces()
    if hasattr(mesh, 'remove_duplicate_faces'):
        mesh.remove_duplicate_faces()
    # Fix normals if needed
    try:
        if not mesh.is_winding_consistent:
            mesh.fix_normals()
    except Exception:
        pass  # Some meshes may not support this check
    print(f"  Result: {len(mesh.vertices):,} vertices, {len(mesh.faces):,} faces")
    return mesh


def export_gltf(mesh: trimesh.Trimesh, output_path: Path) -> None:
    """Export to GLTF with embedded binary."""
    print(f"  Exporting: {output_path.name}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    scene = trimesh.Scene(mesh)
    
    # Try GLB format first (binary GLTF) - more reliable
    try:
        glb_data = scene.export(file_type='glb')
        # Save as .glb if output ends with .glb, otherwise convert
        if output_path.suffix.lower() == '.glb':
            with open(output_path, 'wb') as f:
                f.write(glb_data)
        else:
            # For .gltf, we need to embed the binary as base64
            import json
            import base64
            
            # Export as dict and handle binary buffer
            gltf_dict = scene.export(file_type='gltf', embed_buffers=True)
            
            if isinstance(gltf_dict, dict):
                # Convert any bytes in buffers to base64 data URIs
                if 'buffers' in gltf_dict:
                    for buffer in gltf_dict['buffers']:
                        if 'uri' not in buffer and 'extras' in buffer:
                            # Buffer data might be in extras
                            pass
                        elif isinstance(buffer.get('uri'), bytes):
                            b64 = base64.b64encode(buffer['uri']).decode('ascii')
                            buffer['uri'] = f"data:application/octet-stream;base64,{b64}"
                
                with open(output_path, 'w') as f:
                    json.dump(gltf_dict, f)
            else:
                # Fallback: just write whatever we got
                with open(output_path, 'wb') as f:
                    if isinstance(gltf_dict, bytes):
                        f.write(gltf_dict)
                    else:
                        f.write(str(gltf_dict).encode('utf-8'))
    except Exception as e:
        # Ultimate fallback: save as GLB with .gltf extension (still works in viewers)
        print(f"  Note: Saving as binary GLTF (GLB format)")
        glb_data = scene.export(file_type='glb')
        with open(output_path, 'wb') as f:
            f.write(glb_data)
    
    size = output_path.stat().st_size
    print(f"  Size: {size/1024/1024:.2f} MB" if size > 1024*1024 else f"  Size: {size/1024:.2f} KB")


# =============================================================================
# Main
# =============================================================================

def convert(input_file: str, output_file: str) -> bool:
    """Convert CAD to GLTF."""
    input_path = Path(input_file).resolve()
    output_path = Path(output_file).resolve()
    
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        return False
    
    ext = input_path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"ERROR: Unsupported format: {ext}")
        print(f"Supported: {', '.join(SUPPORTED_FORMATS)}")
        if ext in {'.sldprt', '.sldasm'}:
            print("\n→ SolidWorks files: Export to STL/STEP via File → Save As")
        elif ext in {'.f3d', '.iam', '.ipt'}:
            print("\n→ Autodesk files: Export to STL/STEP via File → Export")
        return False
    
    print(f"\n{'='*50}")
    print("CAD-to-GLTF Converter")
    print(f"{'='*50}")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}\n")
    
    try:
        mesh = load_stl(input_path) if ext == '.stl' else load_step(input_path)
        mesh = optimize_mesh(mesh)
        export_gltf(mesh, output_path)
        print(f"\n✓ Success!\n")
        return True
    except ImportError as e:
        print(f"\nERROR: {e}")
        return False
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert STL/STEP to GLTF for web 3D viewing.",
        epilog="Supported: .stl, .step, .stp | NOT supported: .sldprt, .f3d (export first)"
    )
    parser.add_argument('-i', '--input_file', help="Input file (.stl/.step/.stp)")
    parser.add_argument('-o', '--output_file', help="Output GLTF file")
    parser.add_argument('--check-step', action='store_true', help="Check STEP support")
    
    args = parser.parse_args()
    
    if args.check_step:
        ok, lib = check_step_support()
        print(f"✓ STEP support: {lib}" if ok else "✗ STEP not installed\n  pip install cadquery-ocp")
        sys.exit(0 if ok else 1)
    
    if not args.input_file or not args.output_file:
        parser.error("Both -i and -o are required")
    
    sys.exit(0 if convert(args.input_file, args.output_file) else 1)


if __name__ == "__main__":
    main()
