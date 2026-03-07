
import torch
import torch.nn as nn
class Generator(nn.Module):
  def __init__(self,z_dim=100,img_channels=3):
    super(Generator,self).__init__()
    self.netwokr = nn.Sequential(
        nn.Linear(z_dim,256),
        nn.ReLU(True),
        nn.Linear(256,512),
        nn.ReLU(True),
        nn.Linear(512,1024),
        nn.ReLU(True),
        nn.Linear(1024,img_channels*300*300),
        nn.Tanh()
    )

  def forward(self,z):
    img=self.netwokr(z)
    img=img.view(img.size(0),3,300,300)
    return img



class Discriminator(nn.Module):
  def __init__(self,img_channels=3):
    super(Discriminator,self).__init__()
    self.network=nn.Sequential(
        nn.Flatten(),
        nn.Linear(img_channels*300*300,1024),
        nn.LeakyReLU(0.2,True),
        nn.Linear(1024,512),
        nn.LeakyReLU(0.2,True),
        nn.Linear(512,256),
        nn.LeakyReLU(0.2,True),
        nn.Linear(256,1),
        nn.Sigmoid()
    )
  def forward(self,img):
    return self.network(img)
