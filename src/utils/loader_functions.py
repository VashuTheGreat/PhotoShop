import torch
from src.models.EmojiModel import Generator
from src.models.BgRemover import U2NET
from src.constants import DEVICE


def EmojiFaceGenerator(file_path):
    model=Generator()
    model.load_state_dict(torch.load(file_path,DEVICE))
    return model



def BgRemover(file_path):
    model=U2NET()
    model.load_state_dict(torch.load(file_path,DEVICE))
    return model
