import torch


print("\n========== GPU TEST ==========\n")

print("PyTorch version:", torch.__version__)

print("CUDA version:", torch.version.cuda)

print("CUDA available:", torch.cuda.is_available())


if torch.cuda.is_available():

    print("GPU:", torch.cuda.get_device_name(0))

    print(
        "VRAM:",
        round(
            torch.cuda.get_device_properties(0).total_memory / 1024**3,
            2
        ),
        "GB"
    )


    # Create tensors on GPU

    device = torch.device("cuda")

    a = torch.randn(
        2000,
        2000,
        device=device
    )

    b = torch.randn(
        2000,
        2000,
        device=device
    )


    # GPU matrix multiplication

    c = torch.matmul(a, b)


    print("\nGPU computation successful! ✅")

    print(
        "Result shape:",
        c.shape
    )


    print(
        "Allocated VRAM:",
        round(
            torch.cuda.memory_allocated() / 1024**2,
            2
        ),
        "MB"
    )


else:

    print("\n❌ CUDA is not available.")