import matplotlib.pyplot as plt
import numpy as np
import math

# Set plot titles and labels for Eastings and Northings plot
font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

#region Data Processing Functions

# Function to calculate Euclidean distance between two cells
def calculate_distance(cell1, cell2,i,j):
    distance = math.sqrt((cell1[i] - cell2[i])**2 + (cell1[j] - cell2[j])**2)
    return distance

# Function to find the cell closest to the centroid of all cells
def find_center_cell(cells):
    coordinates = np.array([cell[1:3] for cell in cells])
    centroid = np.mean(coordinates, axis=0)
    center_cell = min(cells, key=lambda x: np.linalg.norm(np.array(x[1:3]) - centroid))
    return center_cell

# Function to assign frequencies to cells based on their proximity
def assign_frequencies(cells, index_1, index_2):
    # Find the center cell
    center_cell = find_center_cell(cells)
    
    # Sort cells based on distance from the center cell
    sorted_cells = sorted(cells, key=lambda x: calculate_distance(center_cell, x, index_1, index_2))
    
    # Assign the first 6 frequencies (110 - 115) to the center cell and its closest neighbors
    for i in range(6):
        sorted_cells[i][5] = 110 + i

    # Assign frequencies to the remaining cells based on distance from the furthest away frequency
    for current_cell in sorted_cells[6:]:
        furthest_away_distance = 0
        furthest_away_frequency = None
        neighbor_cells = sorted(sorted_cells, key=lambda x: calculate_distance(current_cell, x, index_1, index_2))

        # Track the frequencies that have been used closest to the current cell
        used_frequencies = set(range(110, 116))

        for neighbor_cell in neighbor_cells:
            if neighbor_cell[5] != -1:
                if used_frequencies:
                    distance = calculate_distance(current_cell, neighbor_cell, index_1, index_2)
                    # Mark the frequency as used until furthest frequency is found
                    used_frequencies.discard(neighbor_cell[5])

                    # Update furthest away frequency if the distance is greater
                    if distance > furthest_away_distance:
                        furthest_away_distance = distance
                        furthest_away_frequency = neighbor_cell[5]

        # Assign the furthest away frequency to the current cell
        current_cell[5] = furthest_away_frequency

    return sorted_cells

#endregion


#region Data Loading

# Load cell data from a user-selected file
cell_data = []
file_choice = input("given-data-1.txt \nsample-data-2.txt \nsample-data-3.txt \nChoose a file: (type 1, 2, or 3): ")

if file_choice == '1':
    file_name = "given-data-1.txt"
elif file_choice == '2':
    file_name = "sample-data-2.txt"
elif file_choice == '3':
    file_name = "sample-data-3.txt"
else:
    print("Using default script")
    file_name = "given-data-1.txt"

with open(file_name) as file:
    for line in file:
        row = line.strip().split(',')
        cell_ids, eastings, northings, longitudes, latitudes, frequency = [i.strip() for i in row]
        cell_data.append([cell_ids, int(eastings), int(northings), float(longitudes), float(latitudes), int(frequency)])

coordinates_choice = input("Choose a coordinate's system: (type 1 (Easting and northing) or 2 (Latitude and longitude)): ")

# Assign frequencies to cells
if coordinates_choice == '1':  
    cell_data = assign_frequencies(cell_data, 1, 2)
elif coordinates_choice == '2':
    cell_data = assign_frequencies(cell_data, 3, 4)
else:
    print("Using default (Easting and northing)")
    cell_data = assign_frequencies(cell_data, 1, 2)

# Extracting data into separate lists
cell_ids, eastings, northings, longitudes, latitudes, frequency = zip(*cell_data)

# Converting lists to NumPy arrays for plotting
eastings = np.array(eastings)
northings = np.array(northings)
longitudes = np.array(longitudes)
latitudes = np.array(latitudes)

#endregion

#region Printing results

# Print the results at the end
print("\nAllocated Frequencies:")

# Sort cell_data alphabetically based on cell IDs
sorted_cell_data = sorted(cell_data, key=lambda x: x[0])

# Print only cell ID and allocated frequency
for cell in sorted_cell_data:
    print(f"{cell[0]} | {cell[5]}")

#endregion

#region Plotting Functions

# Assign frequencies to cells
if coordinates_choice == '2':
    # Plotting the scatter plot for Longitudes and Latitude
    scatter = plt.scatter(longitudes, latitudes, c=frequency, s=1700, cmap='gist_rainbow', edgecolors='red', alpha=0.6)
    cbar = plt.colorbar(scatter, label='Frequencies')

    # Label points with cell IDs for Longitudes and Latitudes plot
    count = 0
    for (i, j) in zip(longitudes, latitudes):
        plt.text(i, j, (cell_ids[count] ), va='center', ha='center')
        count += 1

    # Set plot titles and labels for Longitudes and Latitudes plot
    plt.title("Cell Phone Towers - Longitudes and Latitudes", fontdict=font1)
    plt.xlabel("Longitudes", fontdict=font2)
    plt.ylabel("Latitudes", fontdict=font2)
    plt.show()
else:
    # Plotting the scatter plot for Eastings and Northings
    scatter = plt.scatter(eastings, northings, c=frequency, s=1700, cmap='gist_rainbow', edgecolors='red', alpha=0.6)
    cbar = plt.colorbar(scatter, label='Frequencies')

    # Label points with cell IDs for Eastings and Northings plot
    count = 0
    for (i, j) in zip(eastings, northings):
        plt.text(i, j, (cell_ids[count] ), va='center', ha='center')
        count += 1

    plt.title("Cell Phone Towers - Eastings and Northings", fontdict=font1)
    plt.xlabel("Eastings", fontdict=font2)
    plt.ylabel("Northings", fontdict=font2)
    plt.show()

#endregion
