import torch
import torch.nn as nn

from dataset import HEIGHT, WIDTH


class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels, out_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


# class BasicBlock(nn.Module):
#     def __init__(self, in_channels, out_channels):
#         super().__init__()
#         '''
#         Checkpoint 2:
#             Use `nn.Sequential` to rewrite `BasicBlock`.
#         '''
#         self.main = ???

#     def forward(self, x):
#         '''
#         Checkpoint 2:
#             Use `nn.Sequential` to rewrite `BasicBlock`.
#         '''
#         return ???


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.main = nn.Sequential(
            BasicBlock(in_channels, out_channels),
            BasicBlock(out_channels, out_channels),
            BasicBlock(out_channels, out_channels),
            nn.MaxPool2d((2, 2)))

    def forward(self, x):
        return self.main(x)


class LPRModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            ConvBlock(3, 32),         # [B, H / 2, W / 2, 32]
            ConvBlock(32, 64),        # [B, H / 4, W / 4, 64]
            ConvBlock(64, 128),       # [B, H / 8, W / 8, 128]
            nn.Flatten(start_dim=1),  # [B, H / 8 x W / 8 x 128]
        )
        self.classifiers = nn.ModuleList()
        for _ in range(7):
            classifier = nn.Sequential(
                nn.Linear(HEIGHT // 8 * WIDTH // 8 * 128, 128),  # [B, 128]
                nn.ReLU(),
                nn.Linear(128, 36),                              # [B, 36]
            )
            self.classifiers.append(classifier)

    def forward(self, x):
        x = self.encoder(x)
        outputs = []
        for classifier in self.classifiers:
            output = classifier(x)          # [B, 36]
            output = output.unsqueeze(1)    # [B, 1, 36]
            outputs.append(output)
        '''
        Checkpoint 3:
            Concatenate `outputs` along the axis 1.
            The shape of the result must be [B, 7, 36].
        '''
        # output = ???
        return output


if __name__ == '__main__':
    model = ConvBlock(3, 16)
    x = model(torch.randn((8, 3, 48, 48)))
    print(x.shape)
