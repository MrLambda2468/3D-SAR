import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
import numpy as np
import trimesh
from scipy.ndimage import gaussian_filter
import pyvista as pv

# Read Raster Data
def read_raster(file_path):
    """
    Read a raster file and return its data, transform, and coordinate reference system (CRS).
    
    Args:
        file_path (str): Path to the raster file.
    
    Returns:
        tuple: (data, transform, crs) where data is the raster data array, 
               transform is the affine transform of the raster, 
               and crs is the coordinate reference system.
    """
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Read the first band
        transform = src.transform
        crs = src.crs
        return data, transform, crs

# Reproject Raster Data
def reproject_raster(src_data, src_transform, src_crs, dst_crs, shape):
    """
    Reproject raster data from source CRS to destination CRS.
    
    Args:
        src_data (np.ndarray): Source raster data.
        src_transform (affine.Affine): Source raster affine transform.
        src_crs (rasterio.crs.CRS): Source coordinate reference system.
        dst_crs (rasterio.crs.CRS): Destination coordinate reference system.
        shape (tuple): Shape of the destination raster.
    
    Returns:
        tuple: (dst_data, dst_transform) where dst_data is the reprojected data 
               and dst_transform is the affine transform of the destination raster.
    """
    dst_data = np.empty(shape, dtype=src_data.dtype)
    dst_transform, _, _ = calculate_default_transform(src_crs, dst_crs, *shape)
    
    reproject(
        source=src_data,
        destination=dst_data,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )
    
    return dst_data, dst_transform

# Normalize Elevation Data
def normalize_elevation(dem_data, min_elevation=0, max_elevation=50):
    """
    Normalize the elevation data to a specific range.
    
    Args:
        dem_data (np.ndarray): DEM data array.
        min_elevation (float): Minimum elevation value after normalization.
        max_elevation (float): Maximum elevation value after normalization.
    
    Returns:
        np.ndarray: Normalized elevation data.
    """
    dem_min = np.min(dem_data)
    dem_max = np.max(dem_data)
    normalized_dem = (dem_data - dem_min) / (dem_max - dem_min) * (max_elevation - min_elevation) + min_elevation
    return normalized_dem

# Smooth DEM Data
def smooth_dem(dem_data, sigma=2):
    """
    Apply Gaussian smoothing to DEM data.
    
    Args:
        dem_data (np.ndarray): DEM data array.
        sigma (float): Standard deviation for Gaussian kernel.
    
    Returns:
        np.ndarray: Smoothed DEM data.
    """
    return gaussian_filter(dem_data, sigma=sigma)

# Create 3D Model with Proper Base
def create_3d_model(dem_data, sar_data, output_path, elevation_scale=3, xy_scale=1):
    """
    Create a 3D model from DEM and SAR data, and save it to a file.
    
    Args:
        dem_data (np.ndarray): DEM data array.
        sar_data (np.ndarray): SAR data array.
        output_path (str): Path to save the output 3D model file.
        elevation_scale (float): Scale factor for elevation data.
        xy_scale (float): Scale factor for XY coordinates.
    """
    # Normalize, scale, and smooth DEM data
    scaled_dem_data = normalize_elevation(dem_data, min_elevation=0, max_elevation=50) * elevation_scale
    smoothed_dem_data = smooth_dem(scaled_dem_data, sigma=2)
    
    nrows, ncols = smoothed_dem_data.shape
    x, y = np.meshgrid(np.arange(ncols) * xy_scale, np.arange(nrows) * xy_scale)
    
    # Create vertices and faces for the 3D model
    vertices = np.stack([x.ravel(), y.ravel(), smoothed_dem_data.ravel()], axis=1)
    colors = sar_data.ravel() / np.max(sar_data)
    
    faces = []
    for i in range(nrows - 1):
        for j in range(ncols - 1):
            v1 = i * ncols + j
            v2 = v1 + 1
            v3 = v1 + ncols
            v4 = v3 + 1
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
    
    # Create base faces for the 3D model
    base_height = np.min(smoothed_dem_data) - 10
    base_vertices = np.stack([x.ravel(), y.ravel(), np.full_like(x.ravel(), base_height)], axis=1)
    
    base_faces = []
    num_vertices = len(vertices)
    for i in range(nrows - 1):
        for j in range(ncols - 1):
            v1 = i * ncols + j
            v2 = v1 + 1
            v3 = v1 + ncols
            v4 = v3 + 1
            base_faces.append([v1 + num_vertices, v2 + num_vertices, v3 + num_vertices])
            base_faces.append([v2 + num_vertices, v4 + num_vertices, v3 + num_vertices])
            base_faces.append([v1, v1 + num_vertices, v3 + num_vertices])
            base_faces.append([v1, v3 + num_vertices, v3])
            base_faces.append([v1, v2, v2 + num_vertices])
            base_faces.append([v1, v2 + num_vertices, v2 + num_vertices])
    
    all_vertices = np.vstack([vertices, base_vertices])
    all_faces = np.vstack([faces, np.array(base_faces)])
    
    mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces, vertex_colors=np.vstack([colors, colors]))
    
    # Export the mesh without simplification
    mesh.export(output_path)

# Main Process
def process_and_export(dem_file, sar_file, output_file, elevation_scale=3, xy_scale=1):
    """
    Process DEM and SAR files to generate and export a 3D model.
    
    Args:
        dem_file (str): Path to the DEM file.
        sar_file (str): Path to the SAR file.
        output_file (str): Path to save the output 3D model file.
        elevation_scale (float): Scale factor for elevation data.
        xy_scale (float): Scale factor for XY coordinates.
    """
    dem_data, dem_transform, dem_crs = read_raster(dem_file)
    sar_data, sar_transform, sar_crs = read_raster(sar_file)
    
    if dem_crs != sar_crs:
        sar_data, sar_transform = reproject_raster(sar_data, sar_transform, sar_crs, dem_crs, dem_data.shape)
    
    create_3d_model(dem_data, sar_data, output_file, elevation_scale, xy_scale)

# File paths
dem_file = 'dem_file.tif' #put src dem file
sar_file = 'sar_file.tif' #put src sar file
output_file = 'output_file.obj' #name 3d file
print("Read both files")
# Run the process
process_and_export(dem_file, sar_file, output_file, elevation_scale=3, xy_scale=1)
print("3D model creation complete.")

# View the 3D Model
def view_3d_model(file_path):
    """
    Load and display a 3D model using PyVista.
    
    Args:
        file_path (str): Path to the 3D model file.
    """
    # Load the 3D model
    mesh = pv.read(file_path)
    
    # Create a plotter object
    plotter = pv.Plotter()
    
    # Add the model to the plotter
    plotter.add_mesh(mesh, color='white')
    
    # Show the plot
    plotter.show()

# Path to your 3D model
file_path = 'output_file.obj'

# View the 3D model
view_3d_model(file_path)
print("3D model visualization complete.")
