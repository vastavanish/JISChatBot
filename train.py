import json

import numpy as np

import torch

import torch.nn as nn

import math

from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

from spacy_utils import preprocess_input_sentence, bag_of_words

#import spa




with open('sir_jis_intents.json', 'r') as f:
    intents = json.load(f)


all_words = []
tags = []
xy = []


x_train = []
y_train = []


for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        _, w, __ = preprocess_input_sentence(pattern)
        if w.__len__() > 0:
            all_words.extend(w)
            xy.append((w, tag))




tags = sorted(set(tags))

# print(xy)

for (pattern, tag) in xy:
    bag = bag_of_words(pattern, all_words)
    x_train.append(bag)
    y_train.append(tags.index(tag))


x_train = np.array(x_train)
y_train = np.array(y_train)



class ChatDataSet(Dataset):
    def __init__(self):
        super(ChatDataSet, self).__init__()
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


# Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(all_words)
learning_rate = 0.001
epochs = 1000

dataset = ChatDataSet()

train_loader = DataLoader(
    dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


for epoch in range(epochs):
    for (words, labels) in train_loader:
        words = words.to(device, dtype=torch.float)
        labels = labels.to(device, dtype=torch.int64)

        # Feedforward
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch + 1}/{epochs}, loss = {loss.item():.4f}')


print(f'final loss, loss = {loss.item():.4f}')


data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags,
}

FILE = "data.pth"

torch.save(data, FILE)


print(f'Training complete. File saved to {FILE}')
