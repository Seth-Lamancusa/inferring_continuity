import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/sethl/Documents/Code/Python Scripts/test_data.csv")

possible_models = [[]]

for segment in df.iterrows():
    # For each model, construct list of new models which are compatible with old one and include segment,
    # then replace possible models with this list
    segment = segment[1].tolist()
    new_models = []
    for axis_model in possible_models:
        # If segment isn't already in model and model isn't empty, construct list of compatible positions in which segment can go,
        # then add new axis with segment included to new_models
        if not segment in axis_model:
            if len(axis_model) == 0:
                new_models.append([segment])
            else:
                segment_placements = []
                for c, characteristic in enumerate(segment):
                    # For each characteristic, build a temporary compatibility list, then use it to update model-specific one
                    segment_placements_c = []
                    if characteristic:
                        # If characteristic is in segment, build list on basis of adjacency to same characteristic
                        if any([s[c] for s in axis_model]):
                            # If characteristic is in model, use adjacency rule to build compatibility list
                            segment_placements_c.append(
                                axis_model[0][c])
                            for i in range(0, len(axis_model) - 1):
                                segment_placements_c.append(
                                    axis_model[i][c] or axis_model[i + 1][c])
                            segment_placements_c.append(
                                axis_model[len(axis_model) - 1][c])
                        else:
                            # If characteristic is not already in model, all positions are valid
                            segment_placements_c = [
                                True] * (len(axis_model) + 1)
                    else:
                        # If characteristic is not in segment, build list on basis of whether segment could break continuous
                        # characteristic strings
                        segment_placements_c.append(True)
                        for i in range(0, len(axis_model) - 1):
                            segment_placements_c.append(
                                not (axis_model[i][c] and axis_model[i + 1][c]))
                        segment_placements_c.append(True)
                    if len(segment_placements) == 0:
                        segment_placements = segment_placements_c
                    else:
                        segment_placements = [j and k for (j, k) in zip(
                            segment_placements, segment_placements_c)]
                for i, v in enumerate(segment_placements):
                    if v:
                        new_models.append(axis_model[:])
                        new_models[len(new_models) - 1].insert(i, segment[:])
    possible_models = new_models[:]

print('Possible models:')
for model in possible_models:
    print(model)

possible_models_ns = []
for model in possible_models:
    model.reverse()
    reverse_model = model[:]
    model.reverse()
    if model not in possible_models_ns and reverse_model not in possible_models_ns:
        possible_models_ns.append(model)

print('Possible models excluding symmetric ones:')
for model in possible_models_ns:
    print(model)

bar_data = []
char_data = []
for model in possible_models_ns:
    char_data.append(np.array(model).T.tolist())
print(char_data)

print(f'Found {len(possible_models_ns)} possible models. Enter index for one to plot: ', end='')
i = int(input())

plt.barh(y=[i for i in range(0, len(char_data[i]))], left=[
    char_data[i][s].index(1) for s in range(len(char_data[i]))], width=[char_data[i][s].count(1) for s in range(len(char_data[i]))])
plt.show()
