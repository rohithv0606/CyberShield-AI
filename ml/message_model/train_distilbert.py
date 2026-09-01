import os
import torch
import pandas as pd

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_NAME = "distilbert-base-uncased"

OUTPUT_DIR = "./ml/message_model/cybershield_distilbert"

MAX_LENGTH = 128


# =========================================================
# GPU CHECK
# =========================================================

print("\n========== DEVICE CHECK ==========\n")

if torch.cuda.is_available():

    print("CUDA available: TRUE")

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )

    print(
        "VRAM:",
        round(
            torch.cuda.get_device_properties(0)
            .total_memory / (1024 ** 3),
            2
        ),
        "GB"
    )

else:

    print("CUDA available: FALSE")

    raise RuntimeError(
        "CUDA is not available. "
        "Check your PyTorch installation."
    )


# =========================================================
# LOAD DATASET
# =========================================================

print("\n========== LOADING DATASET ==========\n")

DATASET_NAME = "zefang-liu/phishing-email-dataset"

from datasets import load_dataset

dataset = load_dataset(DATASET_NAME)

df = dataset["train"].to_pandas()

print("Original rows:", len(df))

print("Columns:", df.columns.tolist())


# =========================================================
# CLEAN DATASET
# =========================================================

print("\n========== CLEANING DATA ==========\n")

# Remove unnecessary index column

if "Unnamed: 0" in df.columns:

    df = df.drop(columns=["Unnamed: 0"])


# Remove missing emails

df = df.dropna(
    subset=["Email Text", "Email Type"]
)


# Convert email text to string

df["Email Text"] = df["Email Text"].astype(str)


# Remove empty emails

df = df[
    df["Email Text"].str.strip() != ""
]


# Remove duplicate emails

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["Email Text"]
)

print(
    "Duplicates removed:",
    before_duplicates - len(df)
)


# =========================================================
# CONVERT LABELS
# =========================================================

print("\n========== LABEL CONVERSION ==========\n")

df["label"] = df["Email Type"].map({
    "Safe Email": 0,
    "Phishing Email": 1
})


# Remove anything that didn't map correctly

df = df.dropna(
    subset=["label"]
)

df["label"] = df["label"].astype(int)


print(
    df["label"].value_counts()
)


# =========================================================
# CREATE TRAIN / TEST SPLIT
# =========================================================

print("\n========== TRAIN / TEST SPLIT ==========\n")

train_df, test_df = train_test_split(
    df[
        ["Email Text", "label"]
    ],
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)


print(
    "Training samples:",
    len(train_df)
)

print(
    "Testing samples:",
    len(test_df)
)


# =========================================================
# CONVERT TO HUGGING FACE DATASETS
# =========================================================

train_dataset = Dataset.from_pandas(
    train_df,
    preserve_index=False
)

test_dataset = Dataset.from_pandas(
    test_df,
    preserve_index=False
)


# =========================================================
# TOKENIZER
# =========================================================

print("\n========== LOADING TOKENIZER ==========\n")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


def tokenize_function(examples):

    return tokenizer(
        examples["Email Text"],
        truncation=True,
        max_length=MAX_LENGTH
    )


print("Tokenizing training data...")

train_dataset = train_dataset.map(
    tokenize_function,
    batched=True
)


print("Tokenizing testing data...")

test_dataset = test_dataset.map(
    tokenize_function,
    batched=True
)


# =========================================================
# LOAD DISTILBERT
# =========================================================

print("\n========== LOADING DISTILBERT ==========\n")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)


# =========================================================
# METRICS
# =========================================================

def compute_metrics(eval_pred):

    predictions, labels = eval_pred

    predictions = predictions.argmax(
        axis=-1
    )

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary"
    )

    accuracy = accuracy_score(
        labels,
        predictions
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# =========================================================
# TRAINING CONFIGURATION
# =========================================================

print("\n========== TRAINING CONFIGURATION ==========\n")

training_args = TrainingArguments(

    output_dir=OUTPUT_DIR,

    eval_strategy="epoch",

    save_strategy="epoch",

    learning_rate=2e-5,

    per_device_train_batch_size=4,

    per_device_eval_batch_size=4,

    gradient_accumulation_steps=4,

    num_train_epochs=2,

    weight_decay=0.01,

    fp16=True,

    logging_steps=50,

    load_best_model_at_end=True,

    metric_for_best_model="f1",

    greater_is_better=True,

    report_to="none"
)


# =========================================================
# TRAINER
# =========================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=test_dataset,

    processing_class=tokenizer,

    compute_metrics=compute_metrics
)


# =========================================================
# TRAIN
# =========================================================

print("\n")
print("================================================")
print("       STARTING DISTILBERT TRAINING")
print("================================================")
print("\n")

trainer.train()


# =========================================================
# FINAL EVALUATION
# =========================================================

print("\n")
print("================================================")
print("             FINAL EVALUATION")
print("================================================")
print("\n")

results = trainer.evaluate()

for key, value in results.items():

    print(
        f"{key}: {value}"
    )


# =========================================================
# SAVE MODEL
# =========================================================

print("\n========== SAVING MODEL ==========\n")

trainer.save_model(
    OUTPUT_DIR
)

tokenizer.save_pretrained(
    OUTPUT_DIR
)


print(
    "\nModel saved successfully!"
)

print(
    "Location:",
    OUTPUT_DIR
)