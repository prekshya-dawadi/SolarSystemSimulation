import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from planet import Planet


# Planets Initializations

# Definition of Sun
sun_radius = 0.4
sun_texture = "D:/Graphics/SolarSystemSimulation/Textures/Sun.jpg"

def set_projection(display):
    # sets the current matrix mode to projection matrix. Subsequent operations will affect the projection matrix
    glMatrixMode(GL_PROJECTION)
    # Loads identity matrix to current matrix stack. Effectively resets the matrix to an inital state. 
    glLoadIdentity()
    # Configures a perspective projection. 
        # Parameters - field of view (45 degrees), aspect ratio of the window, near clipping plan distance(0.1 units), far clipping plane distance (50.0 units)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # Switches the matrix mode back to the modelview matric for subsequent transformations
    glMatrixMode(GL_MODELVIEW)
    # Loads the identity matrix onto the modelview matrix stack. This resets the modelview matrix
    glLoadIdentity()
    # Sets the camera position, target point, and up vector specified as (0,1,0)
    # The camera is positioned at (5,5,5), looking at the origin(0,0,0), with the up vector specified as (0,1,0)
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)


def main():
    pygame.init()
    display = (1250, 650)  # width, height of the display window
    pygame.display.set_caption('3D Solar System Simulation')
    # Set up the Pygame window mode for OpenGL rendering.
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    set_projection(display)
    sun = Planet(sun_radius, sun_texture)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        glRotatef(1, 3, 1, 1)
        # Clear the color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        sun.shape()

        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL Error: {error}")

        # Flip the display to update the screen.
        pygame.display.flip()

        # Add a small delay to control the frame rate.
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
