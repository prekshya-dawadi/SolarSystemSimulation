import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

class Planet:

    def __init__(self, radius, texture_file, rotation_speed, rotation_angle=45, position= (0.0, 0.0, 0.0), orbital_distance=0, rotation_angle_self = 0.0):
        self.radius = radius 
        self.texture = self.load_texture(texture_file)
        self.rotation_speed = rotation_speed
        self.rotation_angle = rotation_angle   
        self.position = np.array(position)    
        self.orbital_distance = orbital_distance
        self.rotation_angle_self = rotation_angle_self
        self.texture_file = texture_file
    
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
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
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

        if 'saturn' in self.texture_file.lower():  # Check if 'saturn' is in the filename
            self.add_rings(self.radius, self.radius)
        # Deletes the quadric object, freeing up resources
        gluDeleteQuadric(quadric)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)  # Disable depth testing after rendering the planet
    
    def update_rotation(self):
        print(f"rotation angle:{self.rotation_angle}")
        self.rotation_angle += abs(self.rotation_speed)
        self.rotation_angle_self += 0.5
    
    def apply_rotation(self):
        glRotatef(self.rotation_angle_self, 0, 1, 0)
        glRotatef(self.rotation_angle, 0, 1, 0)
    

    def calculate_orbital_position(self):
        y = 0.0 # Assuming planets are in the same plane for simplicity
        z = self.orbital_distance * math.sin(math.radians(self.rotation_angle))
        x = self.orbital_distance * math.cos(math.radians(self.rotation_angle))

        return np.array([x, y, z])
    
    
    def add_rings(self, inner_radius, outer_radius, thickness=0.1, distance=0.5, num_segments=100):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUAD_STRIP)

        for i in range(num_segments + 1):
            theta = i * (2.0 * math.pi / num_segments)
        
            # Outer ring
            x_outer = (outer_radius + distance) * math.cos(theta)
            y_outer = (outer_radius + distance) * math.sin(theta)
            z_outer = 0.0
            glTexCoord2f(1.0 * i / num_segments, 0.0)
            glVertex3f(x_outer, y_outer, z_outer)

            # Inner ring
            x_inner = (inner_radius + distance) * math.cos(theta)
            y_inner = (inner_radius + distance) * math.sin(theta)
            z_inner = 0.0
            glTexCoord2f(1.0 * i / num_segments, 1.0)
            glVertex3f(x_inner, y_inner, z_inner)

        glEnd()
        glDisable(GL_TEXTURE_2D)

