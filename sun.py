import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

class Sun:
    def __init__(self, texture_file=None):
        self.texture = self.load_texture(texture_file)
    
    def load_texture(self, texture_file):
        img = Image.open(texture_file)
        img_data = np.array(list(img.getdata()), np.uint8)
        texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

