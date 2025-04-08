# Photo Splitter Script

This script detects and extracts individual photos from a scanned page containing multiple photos. It uses OpenCV for edge detection and contour analysis to identify photo regions and save them as separate files.

## Features

- Automatically detects photo regions in a scanned page.
- Extracts individual photos and saves them as separate files.
- Generates debug images showing detected regions and intermediate processing steps.

## Requirements

- Python 3.6 or higher
- Required libraries:
  - OpenCV
  - NumPy

Install the required libraries using:

```bash
pip install opencv-python numpy
```

## How to Use

### 1. Prepare Your Input Folder

Place all scanned pages (images) in a folder, e.g., `input_folder`. Ensure the images are in `.jpg`, `.jpeg`, or `.png` format.

### 2. Run the Script

Save the Python script as `photo_splitter.py`. Then, run the script with the following command:

```bash
python photo_splitter.py
```

The script processes all images in the specified input folder, extracts individual photos, and saves them in the output folder.

### 3. Example Usage

Here’s an example using the attached image (![`Scanned.jpg`](https://github.com/wltam/photo-splitter/blob/main/Scanned.jpg)):

1. Place `Scanned.jpg` in a folder named `input_folder`.
2. Run the script with:

   ```python
   process_folder('input_folder', 'output_folder')
   ```

3. The script will:
   - Extract each photo from `Scanned.jpg`.
   - Save the extracted photos in `output_folder`.
   - Generate debug images showing detected regions and intermediate processing steps.

### Example Output Structure

After running the script, your output folder will look like this:

```
output_folder/
├── Scanned_photo_1.jpg          # First extracted photo
├── Scanned_photo_2.jpg          # Second extracted photo
├── Scanned_photo_3.jpg          # Third extracted photo
├── Scanned_detected_regions.jpg # Debug image showing detected regions
├── Scanned_enhanced_gray.jpg    # Enhanced grayscale version of input image
├── Scanned_edges.jpg            # Edge detection result
└── Scanned_dilated_edges.jpg    # Dilated edges result
```

### 4. Adjust Parameters

If some photos aren't detected or extra regions are included, adjust these parameters in the script:

- **`min_area`**: Minimum area of a region to be considered a photo (default: `20000`).
- **Canny thresholds**: Adjust `30` and `100` in `cv2.Canny()` for finer edge detection.
- **Margins**: Modify the `margin` variable to include more or less space around detected photos.

## Example Input and Output

### Input Image

![Input Image] 
### Output Photos (Saved in `output_folder/`)

1. **Photo 1**:
   ![Photo 1](output_folderPhoto 2**:
   ![Photo 2](output_folderPhoto 3**:
   ![Photo 3](output_folderDebug Image**:
   ![Debug Image](output_folder/Scanned_dete free to modify this script for your specific needs!

