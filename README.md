# Photo Extraction Tool User Guide

## Overview
This tool automatically detects and extracts photos from scanned documents or images containing multiple photographs. It uses computer vision techniques to identify distinct photo regions and save them as separate image files.

## Features
- Detects rectangular photo regions within larger images
- Filters regions based on size, aspect ratio, and other parameters
- Extracts each detected photo with optional margins
- Creates visualization of detected regions (optional)
- Customizable processing parameters

## Requirements
- Python 3.x
- OpenCV (cv2)
- NumPy

## Usage Instructions

### 1. Basic Usage
```python
process_folder('input_folder_path', 'output_folder_path')
```

Example:
```python
process_folder('C:/Users/Documents/Scanner/', 'C:/Users/Documents/Scanner/extracted')
```

### 2. Adjustable Parameters
The script includes several parameters you can modify to optimize detection for your specific images:

#### Size Filters
- `MIN_AREA`: Minimum area in pixels (default: 20,000)
- `MIN_AREA_RATIO`: Minimum ratio of region area to image area (default: 1%)
- `MAX_AREA_RATIO`: Maximum ratio of region area to image area (default: 99%)
- `MIN_DIMENSION`: Minimum width/height in pixels (default: 100)
- `MAX_ASPECT_RATIO_DIFF`: Maximum ratio between long and short sides (default: 5.0)

#### Processing Parameters
- `MARGIN`: Extra pixels to include around detected regions (default: 5)
- `CANNY_LOW_THRESHOLD`/`CANNY_HIGH_THRESHOLD`: Edge detection sensitivity
- `CLAHE_CLIP_LIMIT`/`CLAHE_TILE_SIZE`: Contrast enhancement settings
- Various filter parameters for noise reduction

#### Output Options
- `SAVE_DETECTED_REGIONS`: Save images with detection boxes (default: True)
- `SAVE_INTERMEDIATE_IMAGES`: Save processing steps for debugging (default: False)

### 3. Output Files
The tool generates:
- Individual extracted photos named `[original_filename]_photo_[number].jpg`
- Visualization images showing detected regions (if enabled)
- Intermediate processing images (if enabled)

## Tips for Best Results
- Ensure good lighting and contrast in your original scans
- Adjust `MIN_AREA` based on the size of photos you want to detect
- If detecting too many false regions, increase `MIN_AREA` or `MIN_DIMENSION`
- If missing photos, try reducing thresholds or increasing `DILATION_ITERATIONS`

## Troubleshooting
- If no photos are detected, try lowering the `MIN_AREA` and `MIN_AREA_RATIO`
- If incorrect regions are detected, try increasing `MIN_AREA` or adjusting edge detection parameters
- For blurry or low-contrast scans, adjust the `CLAHE_CLIP_LIMIT` and Canny thresholds

## Example Workflow
1. Scan multiple photos on a flatbed scanner
2. Save the scan to your input folder
3. Run the script to automatically extract individual photos
4. Check the output folder for the extracted images