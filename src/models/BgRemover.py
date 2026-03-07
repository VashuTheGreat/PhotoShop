# coding u2-Net
import torch
import torch.nn as nn
import torch.nn.functional as F
class REBNCONV(nn.Module):
  def __init__(self,in_ch,out_ch,dilation=1):
    super().__init__()
    self.conv=nn.Conv2d(
        in_ch,
        out_ch,
        kernel_size=3,
        stride=1,
        padding=dilation,
        dilation=dilation,
    )
    self.bn=nn.BatchNorm2d(out_ch)
    self.relu=nn.LeakyReLU(inplace=True)
  def forward(self,x):
    return self.relu(self.bn(self.conv(x)))


class RSU7(nn.Module):
  def __init__(self,in_ch,mid_ch,out_ch):
      super().__init__()
      self.incov=REBNCONV(in_ch,out_ch)

      # Encoder
      self.enc1=REBNCONV(out_ch,mid_ch)
      self.pool1=nn.MaxPool2d(2,stride=2)

      self.enc2=REBNCONV(mid_ch,mid_ch)
      self.pool2=nn.MaxPool2d(2,stride=2)

      self.enc3=REBNCONV(mid_ch,mid_ch)
      self.pool3=nn.MaxPool2d(2,stride=2)

      self.enc4=REBNCONV(mid_ch,mid_ch)


      # Bottom neck
      self.bottleneck=REBNCONV(mid_ch,mid_ch,dilation=2)


      # Decoder
      self.dec4 = REBNCONV(mid_ch*2, mid_ch)
      self.dec3 = REBNCONV(mid_ch*2, mid_ch)
      self.dec2 = REBNCONV(mid_ch*2, mid_ch)
      self.dec1 = REBNCONV(mid_ch*2, out_ch)
  def forward(self,x):
    hx = self.incov(x)

    h1 = self.enc1(hx)
    h2 = self.enc2(self.pool1(h1))
    h3 = self.enc3(self.pool2(h2))
    h4 = self.enc4(self.pool3(h3))

    hb=self.bottleneck(h4)

    d4 = self.dec4(torch.cat((hb, h4), dim=1))
    d3 = self.dec3(torch.cat((F.interpolate(d4, scale_factor=2), h3), dim=1))
    d2 = self.dec2(torch.cat((F.interpolate(d3, scale_factor=2), h2), dim=1))
    d1 = self.dec1(torch.cat((F.interpolate(d2, scale_factor=2), h1), dim=1))
    return d1 + hx



class U2NET(nn.Module):
  def __init__(self,in_ch=3,out_ch=1):
      super().__init__()

      # Encoder
      self.stage1=RSU7(in_ch,32,64)
      self.pool1=nn.MaxPool2d(2,stride=2)
      self.stage2=RSU7(64,32,128)
      self.pool2=nn.MaxPool2d(2,stride=2)


      # Decoder
      self.stage2d=RSU7(128+128,32,64) # Input to stage2d should be hx2 (128 channels) + upsampled hx_pool2 (128 channels)
      self.stage1d=RSU7(64+64,16,64)  # Input to stage1d should be hx1 (64 channels) + upsampled d2 (64 channels)

      # Final output
      self.outconv=nn.Conv2d(64,out_ch,kernel_size=1)

  def forward(self,x):
    hx1=self.stage1(x) # (1, 64, 224, 224)
    hx_pool1=self.pool1(hx1) # (1, 64, 112, 112)

    hx2=self.stage2(hx_pool1) # (1, 128, 112, 112)
    hx_pool2=self.pool2(hx2) # (1, 128, 56, 56)

    # Decoder
    # Upsample hx_pool2 to match hx2's spatial dimensions (112x112)
    upsampled_hx_pool2 = F.interpolate(hx_pool2, scale_factor=2, mode='bilinear', align_corners=False)
    d2=self.stage2d(torch.cat((hx2,upsampled_hx_pool2),dim=1)) # Concatenate hx2 and upsampled hx_pool2

    # Upsample d2 to match hx1's spatial dimensions (224x224)
    upsampled_d2 = F.interpolate(d2, scale_factor=2, mode='bilinear', align_corners=False)
    d1=self.stage1d(torch.cat((hx1,upsampled_d2),dim=1)) # Concatenate hx1 and upsampled d2

    out=self.outconv(d1)
    out=torch.sigmoid(out)
    return out    