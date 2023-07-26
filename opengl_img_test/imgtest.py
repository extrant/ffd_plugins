import imgui
import logging
import glfw
import requests
from PIL import Image
from PIL import PngImagePlugin
from imgui.integrations.glfw import GlfwRenderer
from ff_draw.plugins import FFDrawPlugin
import OpenGL.GL as gl
import io



class DrawIMG(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.image_texture = None
        self.image_width = None
        self.image_height = None
        
        
    def draw_panel(self):
        if self.image_texture is None:
            logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)
            image_url = "https://api.yimian.xyz/img"  # 图片的URL
            self.image_texture, self.image_width, self.image_height = self.create_texture(image_url)
        if imgui.button('Test') :
            logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)
            image_url = "https://api.yimian.xyz/img"  # 图片的URL
            self.image_texture, self.image_width, self.image_height = self.create_texture(image_url)
        imgui.image(self.image_texture, self.image_width * 0.3, self.image_height * 0.3)    
        
    def create_texture(self, image_path):
        response = requests.get(image_path)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        #image = Image.open(image_path)
        image = image.convert("RGBA")  
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = image.tobytes("raw", "RGBA", 0, -1)
        width, height = image.size

        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image_data)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        return texture, width, height 
        

        