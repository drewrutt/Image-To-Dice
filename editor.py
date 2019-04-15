from PIL import Image, ImageFilter
import math
import os

dirname = os.path.dirname(__file__)

def open_image(path):
  newImage = Image.open(path).convert('LA')
  return newImage

# Save Image
def save_image(image, path):
  image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i >= width or j >= height:
      return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


#Builds the image section by section with the dice faces.

#BRACKETS
# 6 -> 0 - 42.5
# 5 -> 42.5 - 85
# 4 -> 85 - 127.5
# 3 -> 127.5 - 170
# 2 -> 170 - 212.5
# 1 -> 212.5 - 255

def create_dice_ary(image, blur, dirname):
  one = open_image(os.path.join(dirname, 'dice_bigger', 'one.png'))
  two = open_image(os.path.join(dirname, 'dice_bigger', 'two.png'))
  three = open_image(os.path.join(dirname, 'dice_bigger', 'three.png'))
  four = open_image(os.path.join(dirname, 'dice_bigger', 'four.png'))
  five = open_image(os.path.join(dirname, 'dice_bigger', 'five.png'))
  six = open_image(os.path.join(dirname, 'dice_bigger', 'six.png'))

  blur *= 3

  factor = math.floor(int(50/blur))
  lastX = 0
  lastY = 0
  width, height = image.size

  newimage = Image.new("1", (width*factor, height*factor))

  ary = []
  for x in range(int(height/blur)):
    row = []
    for y in range(int(width/blur)):
      pix = get_pixel(image, lastX, lastY)
      if(pix != None):
        if(pix[0] <= 42.5):
          row.append(6)
          newimage.paste(six, (lastX*factor, lastY*factor))
        
        elif(pix[0] > 42.5 and pix[0] <= 85):
          row.append(5)
          newimage.paste(five, (lastX*factor, lastY*factor))

        elif(pix[0] > 85 and pix[0] <= 127.5):
          row.append(4)
          newimage.paste(four, (lastX*factor, lastY*factor))

        elif(pix[0] > 127.5 and pix[0] <= 170):
          row.append(3)
          newimage.paste(three, (lastX*factor, lastY*factor))

        elif(pix[0] > 170 and pix[0] <= 212.5):
          row.append(2)
          newimage.paste(two, (lastX*factor, lastY*factor))

        else:
          row.append(1)
          newimage.paste(one, (lastX*factor, lastY*factor))

      lastX += blur

    lastY += blur
    lastX = 0
    ary.append(row)

  return newimage

#To run:
# -Pillow must be installed
# -Put the image file path in the open_image section
# -Set the blur to determine how much detail you would like (int 1 to whatever)
# -Resulting file is saved in the same place as this file and is titled "dice.png"
if __name__ == "__main__":
  img = open_image(r"") #Put the path to the image file here.
                        #For windows you need to convert to a raw string which
                        # it is already set up for.
  blur = 1

  img = img.filter(ImageFilter.BoxBlur(blur))

  newimg = create_dice_ary(img, blur, dirname)
  newimg.save("dice.png")
