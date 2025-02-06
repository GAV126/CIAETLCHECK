# copy file from my laptop
import os
import shutil

# Configuration
FOLDER_A = "C:\\Users\\kaiy\\OneDrive - Redland City Council\\Desktop\\waste"
FOLDER_B = "C:\\Users\\kaiy\\OneDrive - Redland City Council\\Desktop\\Yvevtte's files"

# Ensure destination folder exists
os.makedirs(FOLDER_B, exist_ok=True)


def copy_csv_files():
    csv_files = [f for f in os.listdir(FOLDER_A) if f.endswith(".csv")]
    copied_files = []
    skipped_files = []

    if not csv_files:
        print("Warning: No CSV files found in the source folder.")
        return

    for filename in csv_files:
        src_path = os.path.join(FOLDER_A, filename)
        dest_path = os.path.join(FOLDER_B, filename)

        if os.path.exists(dest_path):
            user_input = input(f"{filename} already exists in the destination. Replace it? (yes/no): ").strip().lower()
            if user_input != "yes":
                print(f"Skipping {filename}...")
                skipped_files.append(filename)
                continue

        print(f"Copying {filename} to {FOLDER_B}...")
        shutil.copy2(src_path, dest_path)
        copied_files.append(filename)

    print("\nSummary:")
    print("Copied files:")
    for file in copied_files:
        print(f"- {file}")

    print("Skipped files:")
    for file in skipped_files:
        print(f"- {file}")


if __name__ == "__main__":
    copy_csv_files()
