# DEM + SAR to 3D Terrain Model Generator

Convert **Digital Elevation Model (DEM)** and **Synthetic Aperture Radar (SAR)** raster data into a textured **3D terrain model (.obj)** and visualize it interactively. Developed during SIH (Smart India Hackathon) 2024 for National Technical Research Organization (NTRO).

---

## Overview

This project generates a 3D terrain mesh by:

1. Reading DEM and SAR raster files.
2. Reprojecting SAR data to match the DEM coordinate system (if necessary).
3. Normalizing and smoothing elevation data.
4. Creating a triangulated 3D mesh from terrain elevation.
5. Applying SAR intensity values as vertex colors.
6. Exporting the model as an OBJ file.
7. Visualizing the generated model using PyVista.

The generated model can be used for:

* Terrain visualization
* GIS and remote sensing applications
* 3D simulation environments
* Digital twin projects
* Educational and research purposes

---

## Features

* Read DEM and SAR GeoTIFF datasets
* Automatic CRS reprojection
* Elevation normalization and scaling
* Gaussian terrain smoothing
* Closed-base 3D mesh generation
* OBJ export support
* Interactive 3D visualization using PyVista

---

## Workflow

```text
DEM (.tif) + SAR (.tif)
           │
           ▼
    Read Raster Data
           │
           ▼
   CRS Verification /
      Reprojection
           │
           ▼
 Normalize Elevation
           │
           ▼
   Gaussian Smoothing
           │
           ▼
  Generate Terrain Mesh
           │
           ▼
 Apply SAR-Based Coloring
           │
           ▼
      Export OBJ
           │
           ▼
   Interactive Viewer
```

---

## Requirements

### Python Version

* Python 3.8 or later

### Dependencies

Install all required packages:

```bash
pip install rasterio numpy trimesh scipy pyvista
```

### Libraries Used

| Library  | Purpose                                  |
| -------- | ---------------------------------------- |
| rasterio | Reading and reprojecting raster datasets |
| numpy    | Numerical computations                   |
| scipy    | DEM smoothing using Gaussian filters     |
| trimesh  | 3D mesh generation and export            |
| pyvista  | Interactive 3D visualization             |

---

## Input Data

### DEM File

Digital Elevation Model containing terrain height information.

Example:

```text
dem_file.tif
```

### SAR File

Synthetic Aperture Radar image used for surface intensity coloring.

Example:

```text
sar_file.tif
```

> Both datasets should represent the same geographic region for best results.

---

## Usage

### 1. Place Input Files

```text
project/
│
├── dem_file.tif
├── sar_file.tif
├── terrain_generator.py
```

---

### 2. Configure File Paths

Modify the file paths in the script:

```python
dem_file = "dem_file.tif"
sar_file = "sar_file.tif"
output_file = "output_file.obj"
```

---

### 3. Run the Script

```bash
python terrain_generator.py
```

---

### 4. Output

The script generates:

```text
output_file.obj
```

and automatically opens a PyVista viewer for visualization.

---

## Adjustable Parameters

### Elevation Scale

Controls vertical exaggeration of terrain.

```python
process_and_export(
    dem_file,
    sar_file,
    output_file,
    elevation_scale=3
)
```

Higher values produce more pronounced terrain features.

---

### XY Scale

Controls horizontal scaling.

```python
process_and_export(
    dem_file,
    sar_file,
    output_file,
    xy_scale=1
)
```

Useful when resizing the terrain footprint.

---

### Smoothing Strength

Modify the Gaussian filter sigma value:

```python
smooth_dem(dem_data, sigma=2)
```

Example:

```python
sigma = 4
```

Higher values create smoother terrain surfaces.

---


---

## Notes

* Large DEM files may require significant memory.
* High-resolution datasets generate large mesh files.
* OBJ format does not preserve GIS metadata.
* DEM and SAR files should be spatially aligned for accurate results.

---

## Future Improvements

* Texture mapping support
* GUI application
* Multi-band raster support
* Automatic terrain clipping

---

## License

This project is intended for educational and research purposes. Feel free to modify and extend it according to your needs.
