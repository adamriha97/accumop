import constants as const
import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Functions():
    def __init__(self):
        pass

    def create_coordinates_matrix():
        mx = []
        longitude_block = (const.LONGITUDE_MAX - const.LONGITUDE_MIN) / const.MX_LONG
        latitude_block = (const.LATITUDE_MAX - const.LATITUDE_MIN) / const.MX_LAT
        for i in range(const.MX_LONG):
            mx.append([])
            for j in range(const.MX_LAT):
                mx[i].append([])
                # longitude
                mx[i][j].append(const.LONGITUDE_MIN + i * longitude_block + longitude_block / 2)
                # latitude
                mx[i][j].append(const.LATITUDE_MIN + j * latitude_block + latitude_block / 2)
        return mx
    
    def create_zeros_matrix():
        return np.zeros((const.MX_LONG, const.MX_LAT))
    
    def create_ones_matrix():
        return np.ones((const.MX_LONG, const.MX_LAT))
    
    def create_demo_matrix(type = 1):
        mx = np.zeros((const.MX_LONG, const.MX_LAT))
        if type == 1:
            x = int(const.MX_LONG/2)
            y = int(const.MX_LAT/2)
            mx[x][y] = 1
        elif type == 2:
            x = int(const.MX_LONG/2)
            y = int(const.MX_LAT/2)
            mx[x-1][y-1] = 1
            mx[x-1][y+1] = 1
            mx[x+1][y-1] = 1
            mx[x+1][y+1] = 1
        elif type == 3:
            x = int(const.MX_LONG/2)
            y = int(const.MX_LAT/2)
            for i in range(-10, 11, 1):
                mx[x + i][y] = 1
        elif type == 4:
            x = int(const.MX_LONG/2)
            y = int(const.MX_LAT/2)
            for i in range(-10, 11, 1):
                for j in range(-5, 6, 1):
                    if j != 0:
                        mx[x + i][y + j] = 1.2 - 0.2*abs(j)
        return mx
    
    def convert_data_to_mx(self, data, values_column, normalize = True, x_column = 'matrix_X', y_column = 'matrix_Y', ones = False, round_values = False):
        values = data[values_column].tolist()
        if round_values:
            #values = [0 if x is None or x == math.nan or x == float('nan') or x == -1 else x for x in values]
            for i in range(len(values)):
                try:
                    values[i] = round(values[i])
                except:
                    values[i] = 0
        x = data[x_column].tolist()
        y = data[y_column].tolist()
        if ones:
            mx = np.ones((const.MX_LONG, const.MX_LAT))
        else:
            mx = np.zeros((const.MX_LONG, const.MX_LAT))
        for i in range(len(values)):
            mx[int(x[i])][int(y[i])] = values[i]
        if normalize:
            mx = self.normalize_matrix(mx)
        return mx

    def convert_mx_to_df(self, matrix, red_factor = 0):
        coordinates_matrix = self.create_coordinates_matrix()
        # Define the columns for the DataFrame
        #columns = ['value', 'longitude', 'latitude']
        # Create an empty DataFrame with the specified columns
        #df = pd.DataFrame(columns=columns)
        values = []
        longitudes = []
        latitudes = []
        x, y = matrix.shape
        for i in range(x):
            for j in range(y):
                if matrix[i][j] != 0:
                    #data = {'value': [matrix[i][j]], 'longitude': [coordinates_matrix[i][j][0]], 'latitude': [coordinates_matrix[i][j][1]]}
                    #df.append(pd.DataFrame(data), ignore_index=True)
                    values.append(matrix[i][j])
                    longitudes.append(coordinates_matrix[i][j][0])
                    latitudes.append(coordinates_matrix[i][j][1])
        df = pd.DataFrame({'value': values, 'longitude': longitudes, 'latitude': latitudes})
        cmap = plt.get_cmap('coolwarm') # 'Blues'
        norm = mcolors.Normalize(vmin=0, vmax=1*(1-red_factor))
        df['color_hex'] = df['value'].apply(lambda x: mcolors.to_hex(cmap(norm(x)))) + 'bf'
        df = df.reset_index()
        return df
    
    def product_of_matrixes(matrix1, matrix2):
        x, y = matrix1.shape
        mx = np.zeros((x, y))
        for i in range(x):
            for j in range(y):
                mx[i][j] = matrix1[i][j] * matrix2[i][j]
        return mx

    def normalize_matrix(matrix):
        max_val = np.max(matrix)
        mx = matrix / max_val
        return mx
    
    def normalize_matrix_ceil_0_1(matrix):
        max_val = np.max(matrix)
        mx = matrix / max_val
        for i in range(len(mx)):
            for j in range(len(mx[i])):
                mx[i][j] = math.ceil(mx[i][j])
        return mx

    def create_kernel_matrix(dimension = 7, power = 1):
        kmx = np.zeros((dimension, dimension))
        center = (dimension - 1) / 2
        for i in range(dimension):
            for j in range(dimension):
                pyth_distance = (abs(center-i)**2 + abs(center-j)**2) ** 0.5
                kmx[i][j] = 1 / ((1 + pyth_distance) ** power)
        return kmx

    def blur_matrix(self, matrix, distance = 3, power = 1):
        # handle input
        distance = int(distance)
        # case for blur with distance 0
        if distance < 1:
            return matrix
        # create padded matrix
        padding = distance
        padded_matrix = np.pad(matrix, ((padding, padding), (padding, padding)), mode='constant', constant_values=0)
        # create kernel matrix
        dimension = 2 * distance + 1
        kernel_matrix = self.create_kernel_matrix(dimension = dimension, power = power)
        # create new matrix
        mx_new = np.zeros((const.MX_LONG, const.MX_LAT))
        x, y = mx_new.shape
        for i in range(x):
            print(i, 'of', x)
            for j in range(y):
                for zi in range(dimension):
                    for zj in range(dimension):
                        k = i + zi
                        l = j + zj
                        mx_new[i][j] = mx_new[i][j] + padded_matrix[k][l] * kernel_matrix[zi][zj]
        mx_new = self.normalize_matrix(mx_new)
        return mx_new

    def blur_matrix_simple(self, matrix, power = 1):
        x, y = matrix.shape
        mx_new = np.zeros((const.MX_LONG, const.MX_LAT))
        for i in range(3, x - 3, 1):
            print(i, 'of', x)
            for j in range(3, y - 3, 1):
                for zi in range(-3, 4, 1):
                    for zj in range(-3, 4, 1):
                        k = i + zi
                        l = j + zj
                        mx_new[i][j] = mx_new[i][j] + matrix[k][l] * (1 / ((1 + abs(zi) + abs(zj)) ** power))
        mx_new = self.normalize_matrix(mx_new)
        return mx_new

    def blur_matrix_pythagoras(self, matrix, power = 1):
        x, y = matrix.shape
        mx_new = np.zeros((const.MX_LONG, const.MX_LAT))
        for i in range(x):
            for j in range(y):
                for zi in range(-10, 11, 1):
                    for zj in range(-10, 11, 1):
                        print(i, j)
                        k = i + zi
                        l = j + zj
                        if k >= 0 and k < x and l >= 0 and l < y:
                            # Pythagoras
                            distance = (abs(k-i)**2 + abs(l-j)**2) ** 0.5
                            mx_new[i][j] = mx_new[i][j] + matrix[k][l] * (1 / ((1 + distance) ** power))
        mx_new = self.normalize_matrix(mx_new)
        return mx_new
    
    def map_mx_to_df(self, matrix, number_of_bands = 50):
        bands = [i/number_of_bands for i in range(number_of_bands+1)]
        zeros = [0 for _ in range(number_of_bands+1)]
        df = pd.DataFrame({'upper_bound': bands, 'count': zeros})
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                df.at[round(math.ceil(matrix[i][j] * 100) / 2), 'count'] += 1
        return df
    
    def map_mx_to_df_poji(self, matrix, matrix_poji, number_of_bands = 50):
        bands = [i/number_of_bands for i in range(number_of_bands+1)]
        zeros = [0 for _ in range(number_of_bands+1)]
        df = pd.DataFrame({'upper_bound': bands, 'count': zeros, 'poji': zeros})
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                df.at[round(math.ceil(matrix[i][j] * 100) / 2), 'count'] += 1
                df.at[round(math.ceil(matrix[i][j] * 100) / 2), 'poji'] += matrix_poji[i][j]
        return df
    
    def aggregate_df(self, df, bounds = [1], aggregated_column = 'count'):
        bounds.insert(0, -1)
        intervals = []
        for i in range(1, len(bounds)):
            intervals.append((bounds[i-1], bounds[i]))
        new_data = []
        for interval in intervals:
            start, end = interval
            aggregated_count = df[(df['upper_bound'] > start) & (df['upper_bound'] <= end)][aggregated_column].sum()
            new_data.append({'upper_bound': end, aggregated_column: aggregated_count})
        new_df = pd.DataFrame(new_data)
        return new_df
    
    def map_mx_to_mx_bounds(self, matrix, bounds = [1]):
        values = [i / (len(bounds) - 1) for i in range(len(bounds))]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(bounds)):
                    if matrix[i][j] <= bounds[k]:
                        matrix[i][j] = values[k]
                        break
        return matrix
        