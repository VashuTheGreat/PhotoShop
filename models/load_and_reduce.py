import torch
from torch import quantization

import os
import sys
sys.path.append(os.getcwd())
from src.models.EmojiModel import Generator
from src.constants import DEVICE
model=Generator()
model.load_state_dict(torch.load("models/EmojiFaceGenerator.pth",map_location=torch.device(DEVICE)))

model.eval()
quantized_model = quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},      # ya (torch.nn.Linear, torch.nn.LSTM, ...)
    dtype=torch.qint8       # ya torch.float16
)
torch.save(quantized_model.state_dict(), "models/EmojiFaceGenerator_quantized.pth")
print(os.path.getsize("models/EmojiFaceGenerator_quantized.pth"))
