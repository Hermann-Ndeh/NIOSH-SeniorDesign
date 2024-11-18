from PIL import Image, ImageDraw

class DefineGrayScale:
    '''
    DefineGrayscale opens a given image and converts into an 16-bit grayscale image that can be used across the program. The process_image 
    method converts the image into an 8-bit grayscale image with grids drawn directly on the image to make identifying potential hazards 
    easier. Converted images are saved in the 'grayscale_drone_images' folder as .JPG files.

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, image_path, grayscale_path, grid_size=(20, 20)):
        '''
        Intialize the class with the specified image path, grayscale path, and grid size.

        Parameters:
            image_path (string): The path to the raw image.
            grayscale_path (string): The path to the grayscale image.
            grid_size (tuple): (width, height) of the entire grid area.
        '''
        
        self.image_path = image_path
        self.grayscale_path = grayscale_path
        self.grid_size = grid_size

    def process_image(self):
        '''
        Processes an image first into an 8-bit grayscale image, displays the grid directly on the image, and saves the final image into a 
        16-bit grayscale to the specified file path.
        '''
        
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
