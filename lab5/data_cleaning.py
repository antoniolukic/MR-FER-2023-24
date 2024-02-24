from __future__ import annotations
import numpy as np
import pickle


def transform_data(train_x, train_y, m):
    new_train_x, new_train_y = [], []
    for j, x in enumerate(train_x):
        points_array = np.array([(point.x, point.y) for point in x])
        centroid = np.mean(points_array, axis=0)
        centered_points = points_array - centroid  # centered points
        maxi = np.max(points_array, axis=0)
        centered_points /= maxi  # scaled points
        distances = np.cumsum([
            np.linalg.norm(np.array(centered_points[i + 1]) - np.array(centered_points[i]))
            for i in range(len(centered_points) - 1)])
        distance = distances[-1] / (m - 1)  # distance step

        selected_points = []  # select the points
        for k in range(m):
            target_distance = k * distance
            closest_point_index = np.argmin(np.abs(distances - target_distance))
            selected_points.append(centered_points[closest_point_index])
        new_train_x.append(np.array(selected_points))

        one_hot_encoded = np.zeros(train_y[-1] + 1)  # one hot encode the y
        one_hot_encoded[train_y[j]] = 1
        new_train_y.append(one_hot_encoded)

    new_train_x, new_train_y = np.array(new_train_x), np.array(new_train_y)
    new_train_x = new_train_x.reshape(new_train_x.shape[0], -1)  # flatten points

    return new_train_x, new_train_y


def save_data_to_file(filename, train_x, train_y):
    data = {'train_x': train_x, 'train_y': train_y}
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_data_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            train_x = data['train_x']
            train_y = data['train_y']
            return train_x, train_y
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None, None
    except Exception as e:
        print(f"Error loading data from file '{filename}': {e}")
        return None, None
