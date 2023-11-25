from pyproj import Proj, transform

# Define the projection systems
input_proj = Proj(init='epsg:27700')  # Assuming OSGB 1936 / British National Grid
output_proj = Proj(proj='latlong', datum='WGS84')

# Coordinates in Easting, Northing format
easting = [1, 3, 5, 7, 9, 10, 8, 6, 4, 2, 15, 5, 3, 1, 10, 20, 15, 30, 21]
northing = [5, 4, 6, 8, 10, 9, 7, 5, 3, 1, 5, 15, 6, 10, 10, 20, 3, 12, 30]

# Convert coordinates 
longitude, latitude = transform(input_proj, output_proj, easting, northing)

# Frequencies
frequencies = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# Print the results
for i, (lon, lat, freq) in enumerate(zip(longitude, latitude, frequencies)):
    cell_id = chr(ord('A') + i)
    print(f"{cell_id}, {easting[i]}, {northing[i]}, {lon:.10f}, {lat:.10f}, {freq}")
