import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

class Planet:

    def __init__(self, radius, texture_file=None, rotation_speed = 1.0, rotation_angle = 0.5, position= (0.0, 0.0, 0.0), orbital_distance=0):
        self.radius = radius 
        self.texture = self.load_texture(texture_file)
        self.rotation_speed = rotation_speed
        self.rotation_angle = rotation_angle   
        self.position = np.array(position)    
        self.orbital_distance = orbital_distance
    
    def load_texture(self, texture_file):

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        img = Image.open(texture_file).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(img.getdata()), np.uint8)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        return texture
    
    
    def shape(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor3f(1.0,1.0,1.0)
        # Creates a new quadric object. quadrics = spheres, cones, cylinders
        quadric = gluNewQuadric()
        # Smooth shading of the surface
        gluQuadricNormals(quadric, GLU_SMOOTH)
        # Enables texture coordinates for the quadric. Required if you want to apply textures to the shape 
        gluQuadricTexture(quadric, GL_TRUE)
        # Draws a sphere using the specified quadric object. parameters - quadric object, radius of the sphere, number of slices and stacks used for rendering the sphere
        gluSphere(quadric, self.radius, 32, 32)
        # Deletes the quadric object, freeing up resources
        gluDeleteQuadric(quadric)
        glDisable(GL_TEXTURE_2D)
    
    def update_rotation(self):
        print(f"rotation angle:{self.rotation_angle}")
        self.rotation_angle += abs(self.rotation_speed)
    
    def apply_rotation(self):
        glRotatef(self.rotation_angle, 0, 1, 0)
        # glRotatef(self.rotation_angle_x, 1, 0, 0)
        # glRotatef(self.rotation_angle_y, 0, 1, 0)
    
    # def visualizeOrbit(self, center_x=0, center_y=0, num_segments=100):
    #     glBegin(GL_TRIANGLE_FAN)
    #     glColor3f(1,1,1)
    #     glVertex2f(center_x, center_y)  # Center of the ellipse

    #     for i in range(num_segments + 1):
    #         theta = 2.0 * math.pi * float(i) / float(num_segments)
    #         x = center_x + self.orbital_distance * math.cos(theta)
    #         y = center_y + (self.orbital_distance)/2 * math.sin(theta)
    #         glVertex2f(x, y)
    #     glEnd()