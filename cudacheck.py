import torch
print("CUDA available:", torch.cuda.is_available())
print("Torch CUDA version:", torch.version.cuda)
print("GPU:", torch.cuda.get_device_name(0))