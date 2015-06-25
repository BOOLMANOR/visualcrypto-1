import numpy as np
import cv2
import os.path

# Choose 3 images
reveal1name = 'in-reveal1.png'
reveal2name = 'in-reveal2.png'
hiddenname = 'in-hidden.png'
if not (os.path.isfile(reveal1name) and os.path.isfile(reveal2name) and os.path.isfile(hiddenname)):
    raise ValueError("Image does not exist")

# Load images in grayscale mode
reveal1 = cv2.imread(reveal1name, cv2.IMREAD_GRAYSCALE)
reveal2 = cv2.imread(reveal2name, cv2.IMREAD_GRAYSCALE)
hidden = cv2.imread(hiddenname, cv2.IMREAD_GRAYSCALE)

# Check all images have equal size
if not (reveal1.shape == reveal2.shape == hidden.shape):
    raise ValueError("Images should have equal size")
height, width = reveal1.shape

# Convert grayscale images to binary
_, reveal1bw = cv2.threshold(reveal1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, reveal2bw = cv2.threshold(reveal2, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, hiddenbw = cv2.threshold(hidden, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Create new black images twice as big as old ones
height2 = 2 * height
width2 = 2 * width
reveal1big = np.zeros((height2, width2), np.uint8)
reveal2big = np.zeros((height2, width2), np.uint8)
hiddenbig = np.zeros((height2, width2), np.uint8)

# Coordinates of pixels in new images corresponding to the original ones
# Position: lu = left-up, ld = left-down, ru = right-up, rd = right-down
def coordinates(position, x, y):
    if position == 'lu':
        return 2 * x, 2 * y
    elif position == 'ld':
        return 2 * x + 1, 2 * y
    elif position == 'ru':
        return 2 * x, 2 * y + 1
    elif position == 'rd':
        return 2 * x + 1, 2 * y + 1


positions = ['lu', 'ld', 'ru', 'rd']

for x in range(0, height):
    for y in range(0, width):
        # Permute positions
        perm = np.random.permutation(positions)
        # If the hidden image pixel is black
        if hiddenbw[x, y] == 0:
            # Both source images have a black pixel
            if (reveal1bw[x, y] == 0) and (reveal2bw[x, y] == 0):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[1], x, y)] = 255
            # First image has a black pixel and second image has a white pixel
            elif (reveal1bw[x, y] == 0) and (reveal2bw[x, y] == 255):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[1], x, y)] = 255
                reveal2big[coordinates(perm[2], x, y)] = 255
            # First image has a white pixel and second image has a black pixel
            if (reveal1bw[x, y] == 255) and (reveal2bw[x, y] == 0):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal1big[coordinates(perm[1], x, y)] = 255
                reveal2big[coordinates(perm[2], x, y)] = 255
            # Both source images have a white pixel
            if (reveal1bw[x, y] == 255) and (reveal2bw[x, y] == 255):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal1big[coordinates(perm[1], x, y)] = 255
                reveal2big[coordinates(perm[2], x, y)] = 255
                reveal2big[coordinates(perm[3], x, y)] = 255
        # If the hidden image pixel is white
        elif hiddenbw[x, y] == 255:
            # Both source images have a black pixel
            if (reveal1bw[x, y] == 0) and (reveal2bw[x, y] == 0):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[0], x, y)] = 255
            # First image has a black pixel and second image has a white pixel
            elif (reveal1bw[x, y] == 0) and (reveal2bw[x, y] == 255):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[1], x, y)] = 255
            # First image has a white pixel and second image has a black pixel
            if (reveal1bw[x, y] == 255) and (reveal2bw[x, y] == 0):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal1big[coordinates(perm[1], x, y)] = 255
                reveal2big[coordinates(perm[0], x, y)] = 255
            # Both source images have a white pixel
            if (reveal1bw[x, y] == 255) and (reveal2bw[x, y] == 255):
                reveal1big[coordinates(perm[0], x, y)] = 255
                reveal1big[coordinates(perm[1], x, y)] = 255
                reveal2big[coordinates(perm[0], x, y)] = 255
                reveal2big[coordinates(perm[2], x, y)] = 255

# Create an image that would show what the hidden image will be look like
cv2.bitwise_and(reveal1big, reveal2big, hiddenbig)

# Place reveal1 and reveal2 adjacent to each other
reveal12big = np.concatenate((reveal1big, reveal2big), axis = 1)

cv2.imwrite('out-reveal1big.png', reveal1big)
cv2.imwrite('out-reveal2big.png', reveal2big)
cv2.imwrite('out-reveal12big.png', reveal12big)
cv2.imwrite('out-hiddenbig.png', hiddenbig)
