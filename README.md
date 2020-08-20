# fortnite_shop

**fortnite_shop** is a python project which will get the newest shop from the Fortnite game. It uses the fnbr.co fortnite api. From there it downloads all images and videos it can get from the shop items for the current day. All single images are stitched togther in one picture with the name and price of each single item. The result image and all videos for the shop items are sent to a telegram group using the telegram chat api. The project is compatible with using cron or any other job scheduler. It will only sent the image and videos if the images update to the previouse run.

Here is a example of how the output image could look like:
![example_output_image.jpg](https://github.com/sp4c38/fortnite_shop/blob/master/example_output_image.jpg)
