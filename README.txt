🌍 3D Terrain Generator from DEM and SAR Data

This project converts real-world geospatial data — specifically, Digital Elevation Models (DEM) and Synthetic Aperture Radar (SAR) images — into realistic 3D terrain meshes. It produces a `.obj` file suitable for use in 3D rendering software, game engines, or GIS visualization platforms.
This project was a part of the Smart India Hackathon 2024 where our problem statement was to classify man-made and natural changes using ynthetic Aperture Radar (SAR) satellite images. 
Change output file types to 'gltf' or any other format to be viewed on a webpage. Also, Change the SAR file to any satellite image file, because this will just act as a layer on the 3D model.

 ✨ Features

- Reads DEM and SAR raster images (`.tif`)
- Automatically reprojects SAR to match DEM if needed
- Normalizes and smooths elevation data
- Generates a full 3D mesh with elevation and a solid base
- Applies color data from SAR imagery
- Exports `.obj` 3D model
- Includes optional interactive 3D viewer with PyVista

📦 Dependencies
Install the required packages using:
pip install -r requirements.txt

This project is open for contribution.
