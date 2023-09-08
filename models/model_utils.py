import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class ExponentialModel(nn.Module):
    def __init__(self, num_terms):
        super(ExponentialModel, self).__init__()
        self.coefficients = torch.distributions.dirichlet.Dirichlet(torch.ones(num_terms))
        self.A = nn.Parameter(torch.tensor([coeff for coeff in self.coefficients.sample()]), requires_grad=True)
        self.B = nn.Parameter(torch.tensor([coeff for coeff in self.coefficients.sample()]), requires_grad=True)

    def forward(self, x):
        y = torch.sum(self.A * torch.exp(-self.B * x), dim=1).unsqueeze(1)
        return y


def load_pretrained_model(model_path: str, num_terms: int):

    model = ExponentialModel(num_terms)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model



def train_model(data, num_epochs=100, lr=0.01, num_terms=5):
    # Подготавливаем данные
    data['Gradient'] = data['Gradient'].astype('float32')
    data['Expt'] = data['Expt'].astype('float32')

    x_data = torch.tensor(data['Gradient'].values, dtype=torch.float32).unsqueeze(1)
    y_data = torch.tensor(data['Expt'].values, dtype=torch.float32).unsqueeze(1)
    
    # Создание и сохранение модели
    model = ExponentialModel(num_terms)


    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'trained_model.pth')
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path))
        # model.eval()
    else:
        print(f"No pretrained model found at {model_path}")


    # Генерация предсказаний и вывод модели
    model.load_state_dict(torch.load('models/trained_model.pth'))
    model.eval()

    history_loss = []
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(num_epochs):
        optimizer.zero_grad()
        outputs = model(x_data)
        loss = criterion(outputs, y_data)
        loss_value = loss.item()
        history_loss.append(loss_value)
        loss.backward()
        optimizer.step()

    return model, history_loss

def predict_model(model, x_data):
    with torch.no_grad():
        predictions = model(x_data)
    return predictions.numpy()