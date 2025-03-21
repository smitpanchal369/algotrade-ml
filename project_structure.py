import os

def create_project_structure(base_dir="StockPredictionProject"):
    structure = [
        "data/raw",
        "data/processed",
        "models",
        "notebooks",
        "src",
        "tests",
    ]

    files = {
        "src/data_loader.py": """# data_loader.py\n# Script to download stock data\n""",
        "src/preprocess.py": """# preprocess.py\n# Script for data preprocessing\n""",
        "src/split_data.py": """# split_data.py\n# Train-test split logic\n""",
        "src/train_model.py": """# train_model.py\n# Model training script\n""",
        "src/evaluate.py": """# evaluate.py\n# Model evaluation script\n""",
        "src/save_model.py": """# save_model.py\n# Save best model if effective\n""",
        "requirements.txt": "pandas\nscikit-learn\npytorch\nmatplotlib\nnumpy\n",
        "config.py": """# config.py\n# Configuration file\nDATA_PATH = 'data/'\nMODEL_PATH = 'models/'\n""",
        "main.py": """# main.py\n# Main script to execute the pipeline\n""",
        "README.md": """# Stock Prediction Project\nThis project predicts stock trends using machine learning models.\n"""
    }

    # Create directories
    for folder in structure:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    # Create files with initial content
    for file_path, content in files.items():
        file_full_path = os.path.join(base_dir, file_path)
        with open(file_full_path, "w") as f:
            f.write(content)

    print(f"Project structure created successfully at: {base_dir}")

# Run the function
create_project_structure()
