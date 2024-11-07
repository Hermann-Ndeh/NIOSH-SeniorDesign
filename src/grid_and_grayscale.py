from PIL import Image, ImageDraw

class DefineGrayScale:
    def __init__(self, image_path, grayscale_path, grid_size=(20, 20)):
        self.image_path = image_path
        self.grayscale_path = grayscale_path
        self.grid_size = grid_size

    def process_image(self):  
        image = Image.open(self.image_path)
        gray_image = image.convert('L')
        width, height = gray_image.size
        cell_width = width // self.grid_size[1]
        cell_height = height // self.grid_size[0]
        draw = ImageDraw.Draw(gray_image)
        for i in range(1, self.grid_size[0]):
            y = i * cell_height
            draw.line([(0, y), (width, y)], fill=0, width=1) 

        for i in range(1, self.grid_size[1]):
            x = i * cell_width
            draw.line([(x, 0), (x, height)], fill=0, width=1)  

        gray_image.save(self.grayscale_path)
        # gray_image.show()

# process_image('drone-images/DJI_0647.JPG', grid_size=(20, 20))  
# process_image('drone-images/DJI_0948.JPG', grid_size=(20, 20))  
# process_image('drone-images/DJI_0978.JPG', grid_size=(20, 20), )  


