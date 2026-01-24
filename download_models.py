
import os
import urllib.request
import tarfile
import shutil
import zipfile

MODEL_URL = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip"
LABEL_URL = "https://dl.google.com/coral/cocomobile/coco_labels.txt"

MODEL_DIR = "models"
MODEL_FILE_NAME = "detect.tflite"
LABEL_FILE_NAME = "coco_labels.txt"

def download_file(url, output_path):
    print(f"Downloading {url}...")
    try:
        with urllib.request.urlopen(url) as response, open(output_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print(f"Saved to {output_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def setup_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # Download Model Zip (contains both model and labels)
    zip_path = os.path.join(MODEL_DIR, "model.zip")
    
    # Check if we need to download
    # We check if the final model file exists
    final_model_path = os.path.join(MODEL_DIR, MODEL_FILE_NAME)
    
    if not os.path.exists(final_model_path):
        download_file(MODEL_URL, zip_path)
        
        print("Extracting model...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(MODEL_DIR)
                
            print("Extraction complete.")
            
            # Download proper label map (The one in zip often has '???' entries)
            # We explicitly download a clean one
            target_label_map = os.path.join(MODEL_DIR, LABEL_FILE_NAME)
            download_file(LABEL_URL, target_label_map)
                
        except zipfile.BadZipFile:
            print("Error: The downloaded file is not a valid zip file.")
        except Exception as e:
            print(f"Error during extraction: {e}")
        
        # Cleanup
        if os.path.exists(zip_path):
            os.remove(zip_path)
    else:
        print("Model file already exists. Skipping model download.")

    # Always update/verify the label map to ensure we have the clean version (not the '???' one from zip)
    print("Verifying label map...")
    target_label_map = os.path.join(MODEL_DIR, LABEL_FILE_NAME)
    download_file(LABEL_URL, target_label_map)

if __name__ == "__main__":
    setup_models()
