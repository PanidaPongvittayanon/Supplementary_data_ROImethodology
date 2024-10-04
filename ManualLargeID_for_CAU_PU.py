import numpy as np
import nibabel as nib
import sys
import os
#import cv2
import matplotlib.pyplot as plt


# Input
b0_image = sys.argv[1]
print(b0_image)
mask_image = sys.argv[2]
print(mask_image)
segmented_image = sys.argv[3]
print(segmented_image)
percentage = 0.7  # Adjust this value as needed

# Load the B0 MRI image, brain mask, and segmented area
b0_image = nib.load(b0_image)
b0_data = b0_image.get_fdata()
mask_image = nib.load(mask_image)
mask_data = mask_image.get_fdata()
segmented_image = nib.load(segmented_image)
segmented_data = segmented_image.get_fdata()

print (b0_data.shape)
print (mask_data.shape)

imgGray = b0_data[:,:,60]
plt.imshow(imgGray, cmap = 'gray')
plt.show() 


# Create a copy of the mask to store the new mask
new_mask_data = np.zeros_like(mask_data)

# Loop through each slice of the masked region in the coronal plane (Y direction)
for y in range(mask_data.shape[2]):
    # Select the voxels within the intersection of the segmented area and mask
    intersection_data = b0_data[:, :, y] * (mask_data[:, :, y] != 0) * (segmented_data[:, :, y] != 0)
    intersection_slice_data = intersection_data[intersection_data != 0]

    # Calculate the number of voxels to select based on the percentage
    
    num_voxels_to_select = int(len(intersection_slice_data) * percentage)
    segment = num_voxels_to_select
    lst = intersection_slice_data
    mystart = int((len(lst) - segment)/2)
    mystop = int(mystart + segment)

    # Select the lowest pixel intensities based on the percentage
    sorted_indices = np.argsort(intersection_slice_data)[mystart:mystop]
    selected_indices = np.where(intersection_data != 0)
    selected_indices = np.array(selected_indices).T[sorted_indices]

    # Set the selected voxels to 1 in the new mask
    #new_mask_data[selected_indices[:, 0], y, selected_indices[:, 1]] = 1
    new_mask_data[selected_indices[:, 0], selected_indices[:, 1], y] = 1
    
# Save the new mask as a Nifti file
output_filename = 'output_' + os.path.split(sys.argv[3])[1]
output_path = os.path.join(os.path.split(sys.argv[3])[0], output_filename)
nib.save(nib.Nifti1Image(new_mask_data, segmented_image.affine), output_path)

print('It works, Yeah')
