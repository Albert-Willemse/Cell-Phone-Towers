import matplotlib.pyplot as plt
import numpy as np
import math

# Given data
# cell_data = [
#     ("A", 536660, 183800, -0.03098, 51.53657),
#     ("B", 537032, 184006, -0.02554, 51.53833),
#     ("C", 537109, 183884, -0.02448, 51.53721),
#     ("D", 537110, 184695, -0.02415, 51.5445),
#     ("E", 537206, 184685, -0.02277, 51.54439),
#     ("F", 537248, 185016, -0.02204, 51.54735),
#     ("G", 537250, 185020, -0.02201, 51.54739),
#     ("H", 537267, 184783, -0.02185, 51.54525),
#     ("I", 537269, 183451, -0.02234, 51.53328),
#     ("J", 537270, 184140, -0.02206, 51.53948),
#     ("K", 537356, 184927, -0.02052, 51.54653),
#     ("L", 537380, 184727, -0.02025, 51.54472),
#     ("M", 537458, 184495, -0.01921, 51.54262),
#     ("N", 537604, 184134, -0.01725, 51.53934),
#     ("O", 537720, 184057, -0.01561, 51.53862),
#     ("P", 537905, 184591, -0.01273, 51.54337),
#     ("Q", 537910, 184441, -0.01272, 51.54202),
#     ("R", 537953, 184295, -0.01216, 51.5407),
#     ("S", 538050, 184245, -0.01078, 51.54023),
# ]

def calculate_distance(cell1, cell2):
    distance = math.sqrt((cell1[1] - cell2[1])**2 + (cell1[2] - cell2[2])**2)
    # print( str(cell1[1]) + " " + str(cell2[2]) + " : " + str(distance))
    return distance

def find_center_cell(cells):
    # Extract coordinates into NumPy array for efficient calculations
    coordinates = np.array([cell[1:3] for cell in cells])

    # Calculate the centroid
    centroid = np.mean(coordinates, axis=0)

    # Find the cell closest to the centroid
    center_cell = min(cells, key=lambda x: np.linalg.norm(np.array(x[1:3]) - centroid))

    return center_cell

def assign_frequencies(cells):
    # center_cells = sorted(cells, key=lambda x: sum(calculate_distance(x, other) for other in cells))
    # print("Center Node:", center_cells[0])

    center_cell = find_center_cell(cells)
    print("Center Cell:", center_cell)
    

    sorted_cells = sorted(cells, key=lambda x: calculate_distance(center_cell, x))
    


    # Set the first 6 frequencies (110 - 115) to the center cell and the closest cells
    for i in range(6):
        sorted_cells[i][5] = 110 + i

    print("Sorted Cells:", sorted_cells)
    print("Sorted Cell 6:", sorted_cells[6])

    # Assign frequencies to the remaining cells based on distance from the furthest away frequency
    for current_cell in sorted_cells[6:]:
        
        furthest_away_distance = 0
        furthest_away_frequency = None
        
        neighbor_cells = sorted(sorted_cells, key=lambda x: calculate_distance(current_cell, x))
        print("Neighbor Cells: " + str(neighbor_cells))
        print("current_cell: " + str(current_cell[0]))

        # Track the frequencies that have been used
        used_frequencies = set(range(110, 116))

        for neighbor_cell in neighbor_cells:
            
            if neighbor_cell[5] != -1:
                
                if used_frequencies:
                    distance = calculate_distance(current_cell, neighbor_cell)

                    print("used_frequencies : " + str(used_frequencies))
                    # Mark the frequency as used
                    used_frequencies.discard(neighbor_cell[5])
                    

                    # Update furthest away frequency if the distance is greater
                    if distance > furthest_away_distance:
                        furthest_away_distance = distance
                        furthest_away_frequency = neighbor_cell[5]
                        
            
            
                        
        print("furthest_away_frequency : " + str(furthest_away_frequency))

        # Assign the furthest away frequency to the current cell
        current_cell[5] = furthest_away_frequency

        
    return sorted_cells




cell_data = []

with open('sample-data.txt') as file:
    for line in file:
        row = line.strip().split(',')
        cell_ids, eastings, northings, longitudes, latitudes, frequency = [i.strip() for i in row]

        # Store the data as separate lists
        cell_data.append([cell_ids, int(eastings), int(northings), float(longitudes), float(latitudes), int(frequency)])


# Frequency allocation
cell_data = assign_frequencies(cell_data)

# Extracting data into separate lists
cell_ids, eastings, northings, longitudes, latitudes, frequency = zip(*cell_data)


# Converting lists to NumPy arrays
xpoints = np.array(eastings)
ypoints = np.array(northings)
longitudes = np.array(longitudes)
latitudes = np.array(latitudes)




# Plotting the scatter plot and assigning it to 'scatter'
scatter = plt.scatter(xpoints, ypoints, c=frequency, s=1700, cmap='gist_rainbow', edgecolors='red', alpha=0.6)

# Add a colorbar
cbar = plt.colorbar(scatter, label='Frequencies')

# Label points with eastings & northings
count = 0
for (i, j) in zip(xpoints, ypoints):
    plt.text(i, j, (cell_ids[count] ), va='center', ha='center')
    count += 1

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("Cell Phone Towers", fontdict = font1)
plt.xlabel("Eastings", fontdict = font2)
plt.ylabel("Northings", fontdict = font2)

plt.show()

# Label points with longitudes & latitudes

count = 0
for (i, j) in zip(longitudes, latitudes):
    plt.text(i, j, (cell_ids[count]), va='center', ha='center')
    count += 1


plt.scatter(longitudes, latitudes, s= 1500, edgecolors = 'red',  alpha = 0.3)

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("Cell Phone Towers", fontdict = font1)
plt.xlabel("Longitudes", fontdict = font2)
plt.ylabel("Latitudes", fontdict = font2)

plt.show()

