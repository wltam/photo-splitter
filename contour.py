import cv2
import numpy as np
import os

def process_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) 
                  if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    
    total_photos = 0
    
    for image_file in image_files:
        # Read the input image
        input_image_path = os.path.join(input_folder, image_file)
        img = cv2.imread(input_image_path)
        original = img.copy()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE for enhanced contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # Apply bilateral filter to reduce noise while preserving edges
        smooth = cv2.bilateralFilter(enhanced_gray, 9, 75, 75)

        # Apply Gaussian blur to further reduce noise
        blurred = cv2.GaussianBlur(smooth, (5, 5), 0)

        # Apply Canny edge detection with appropriate thresholds
        edges = cv2.Canny(blurred, 30, 100)

        # Dilate edges to close gaps
        kernel = np.ones((5, 5), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=2)

        # Find contours in the edge image
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, 
                                      cv2.CHAIN_APPROX_SIMPLE)

        # Filter and extract rectangular regions (photos)
        min_area = 20000  # Minimum area to consider as a photo
        count = 0

        # Debug image to show detected regions
        debug_img = original.copy()

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # Get a bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Add a small margin to ensure we capture the full photo
                margin = 5
                x_with_margin = max(0, x - margin)
                y_with_margin = max(0, y - margin)
                w_with_margin = min(img.shape[1] - x_with_margin, w + 2 * margin)
                h_with_margin = min(img.shape[0] - y_with_margin, h + 2 * margin)

                # Extract the region of interest (photo)
                photo = original[y_with_margin:y_with_margin + h_with_margin, 
                               x_with_margin:x_with_margin + w_with_margin]

                # Save the extracted photo
                base_name = os.path.splitext(image_file)[0]
                output_path = os.path.join(output_folder, 
                                         f'{base_name}_photo_{count + 1}.jpg')
                cv2.imwrite(output_path, photo)
                count += 1

                # Draw rectangle on debug image
                cv2.rectangle(debug_img, (x_with_margin, y_with_margin),
                            (x_with_margin + w_with_margin, y_with_margin + h_with_margin),
                            (0, 255, 0), 3)

        # Save the visualization with detected regions
        debug_path = os.path.join(output_folder, 
                                f'{os.path.splitext(image_file)[0]}_detected_regions.jpg')
        cv2.imwrite(debug_path, debug_img)

        # Also save intermediate processing images for debugging
        cv2.imwrite(os.path.join(output_folder, 
                               f'{os.path.splitext(image_file)[0]}_enhanced_gray.jpg'), 
                   enhanced_gray)
        cv2.imwrite(os.path.join(output_folder, 
                               f'{os.path.splitext(image_file)[0]}_edges.jpg'), 
                   edges)
        cv2.imwrite(os.path.join(output_folder, 
                               f'{os.path.splitext(image_file)[0]}_dilated_edges.jpg'), 
                   dilated_edges)
        
        total_photos += count
        print(f"Processed '{image_file}': Found {count} photos")

    print(f"Processed {len(image_files)} images from '{input_folder}'")
    print(f"Total {total_photos} photos extracted and saved to '{output_folder}'")

# Example usage
# process_folder('input_folder', 'output_folder')


process_folder('C:/Users/xxxx/Documents/Scanner/', 'C:/Users/xxxx/Documents/Scanner/extracted')