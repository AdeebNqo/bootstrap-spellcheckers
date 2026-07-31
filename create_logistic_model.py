import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import csv

class Dataset(Dataset):
	def __init__(self, filename):

		x_data = []
		y_data = []
		with open(filename, mode='r') as file:
			reader = csv.DictReader(file)
			for row in reader:
				correct_word_score = row['Correct word score']
				incorrect_word_score = row['Incorrect word score']

				x_data.append(float(correct_word_score))
				y_data.append(1)
				x_data.append(float(incorrect_word_score))
				y_data.append(0)

		self.x = torch.tensor(x_data, dtype=torch.float32)
		self.y = torch.tensor(y_data, dtype=torch.float32)

	def __len__(self):
		return len(self.x)

	def __getitem__(self, idx):
		return self.x[idx], self.y[idx]

class LogisticRegression(nn.Module):
	def __init__(self, input_dim):
		super(LogisticRegression, self).__init__()
		self.linear = nn.Linear(input_dim, 1)

	def forward(self, x):
		return self.linear(x)

if __name__=='__main__':
	model = LogisticRegression(input_dim=1)
	criterion = nn.BCEWithLogitsLoss()
	optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

	epochs_per_file = 5
	batch_size = 16

	folder_name = 'wrecked_scored_test_data'
	filenames = os.listdir(folder_name)
	for filename in filenames:
		filename = os.path.join(folder_name, filename)

		current_dataset = Dataset(filename)
		train_loader = DataLoader(current_dataset, batch_size=batch_size, shuffle=True)
		for epoch in range(epochs_per_file):
			total_loss = 0
			
			for inputs, labels in train_loader:
				inputs = inputs.view(-1, 1).float()
				labels = labels.view(-1, 1).float()

				outputs = model(inputs)
				loss = criterion(outputs, labels.view_as(outputs))

				optimizer.zero_grad()
				loss.backward()
				
				optimizer.step()

				total_loss += loss.item()

			avg_loss = total_loss / len(train_loader)
			print(f"Epoch [{epoch+1}/{epochs_per_file}], Loss: {avg_loss:.4f}")

		output_filename = filename.replace('wrecked_scored_test_data', 'logistic_models').replace('.csv', '.pth')
		torch.save(model, output_filename)