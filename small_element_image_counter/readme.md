# Readme

This code is projected to count small objects in pictures and yields geometric parameters

The small objects can be things such as salt grains, beans, rocks, coins...  

It was coded in python 3.8

## Content

- code
- example_images
- readme

### Images

There is a directory with example pictures of what this code intends to measure. It contains 4 pictures of salt grains and one of coins. 

Check the example_images directory for having an idea of the kind of objects it can count.

> Note: if you will take a picture, for a good picture, be sure that the background of the object is the most simple and plain as possible (single collor background is the perfect)

> the salt grains pictures are not the most perfect type of image because it has several glare in the backgound (when I took the pictures I had only that surface)

### Code

Download the code and insert it into a specific directory

If you want, insert the images you want analyze in the same directory (imgs must be .jpg)

Run the code

**input**

- images path

  > hit enter if the images are in the same directory as the code

- csv filename

  > name of the output csv filename

**output**

The output is a csv file named with the input csv filename you chose

The output csv file has the following parameters of each counted object and its respective unity, pixels

- area (pixel²)
- labels (integer number)
- perimeter (pixel)
- major axis length (pixel)
- minor axis length (pixel)
- equivalent diameter (pixel)



