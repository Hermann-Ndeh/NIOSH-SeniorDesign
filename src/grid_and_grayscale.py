from PIL import Image, ImageDraw

class DefineGrayScale:
    def __init__(self, image_path, grayscale_path, grid_size=(20, 20)):
        self.image_path = image_path
        self.grayscale_path = grayscale_path
        self.grid_size = grid_size

    def process_image(self):  
        # Open the image directly as an 8-bit grayscale (L) image for easier manipulation
        image = Image.open(self.image_path).convert('L')
        width, height = image.size

        # Calculate cell width and height based on the grid size
        cell_width = width // self.grid_size[1]
        cell_height = height // self.grid_size[0]

        # Draw grid lines directly onto the grayscale image
        draw = ImageDraw.Draw(image)
        for i in range(1, self.grid_size[0]):
            y = i * cell_height
            draw.line([(0, y), (width, y)], fill=0) 

        for i in range(1, self.grid_size[1]):
            x = i * cell_width
            draw.line([(x, 0), (x, height)], fill=0)  

        # Save the image as 16-bit grayscale to the output path
        final_image = image.convert('I;16')
        final_image.save(self.grayscale_path)
