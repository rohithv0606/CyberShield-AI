from datasets import load_dataset


print("\n========== LOADING PHISHING DATASET ==========\n")


dataset = load_dataset(
    "zefang-liu/phishing-email-dataset"
)


print(dataset)


print("\n========== DATASET STRUCTURE ==========\n")

for split in dataset:

    print(
        "Split:",
        split
    )

    print(
        "Rows:",
        len(dataset[split])
    )

    print(
        "Columns:",
        dataset[split].column_names
    )


    print("\nFirst example:")

    print(
        dataset[split][0]
    )

    print("\n")