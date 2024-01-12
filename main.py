import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from planet import Planet


# Planets Definitions

# Definition of Sun
sun_radius = 1
sun_texture = "D:/Graphics/SolarSystemSimulation/Textures/Sun.jpg"
sun_position = (0,0,0)

#Definition of mercury
mercury_radius = 0.0035
mercury_texture = "D:/Graphics/SolarSystemSimulation/Textures/mercury.jpg"
mercury_distance = 0.013
mercury_position = (mercury_distance,0,0)

#Definition of venus
venus_radius = 0.0087
venus_texture = "D:/Graphics/SolarSystemSimulation/Textures/uranus.jpg"
venus_distance = 0.024
venus_position = (venus_distance,0,0)

#Definition of earth
earth_radius = 0.0092
earth_texture = "D:/Graphics/SolarSystemSimulation/Textures/earth.jpg"
earth_distance = 0.033
earth_position = (earth_distance,0,0)


#Definition of mars
mars_radius = 0.0049
mars_texture = "D:/Graphics/SolarSystemSimulation/Textures/mars.jpg"
mars_distance = 0.051
mars_position = (mars_distance,0,0)


#Definition of jupiter
jupiter_radius = 0.103
jupiter_texture = "D:/Graphics/SolarSystemSimulation/Textures/jupiter.jpg"
jupiter_distance = 0.173
jupiter_position = (jupiter_distance,0,0)

#Definition of saturn
saturn_radius = 0.087
saturn_texture = "D:/Graphics/SolarSystemSimulation/Textures/saturn.jpg"
saturn_distance = 0.317
saturn_position = (saturn_distance,0,0)

#Definition of uranus
uranus_radius = 0.037
uranus_texture = "D:/Graphics/SolarSystemSimulation/Textures/uranus.jpg"
uranus_distance = 0.638
uranus_position = (uranus_distance,0,0)

#Definition of neptune
neptune_radius = 0.036
neptune_texture = "D:/Graphics/SolarSystemSimulation/Textures/neptune.jpg"
neptune_distance = 1.0
neptune_position = (neptune_distance,0,0)



def set_projection(display):
    # sets the current matrix mode to projection matrix. Subsequent operations will affect the projection matrix
    glMatrixMode(GL_PROJECTION)
    # Loads identity matrix to current matrix stack. Effectively resets the matrix to an inital state. 
    glLoadIdentity()
    # Configures a perspective projection. 
        # Parameters - field of view (45 degrees), aspect ratio of the window, near clipping plan distance(0.1 units), far clipping plane distance (50.0 units)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    # Switches the matrix mode back to the modelview matric for subsequent transformations
    glMatrixMode(GL_MODELVIEW)
    # Loads the identity matrix onto the modelview matrix stack. This resets the modelview matrix
    glLoadIdentity()

    camera_distance = 5.0
    camera_rotation_angle = 90.0
    
    # Set the camera position to a point slightly above the orbit
    camera_pos = np.array([camera_distance * math.cos(math.radians(camera_rotation_angle)),
                           5.0,  # Adjust the height of the camera
                           camera_distance * math.sin(math.radians(camera_rotation_angle))])

    # Set the target point to the center of the solar system
    target_point = np.array([0.0, 0.0, 0.0])

    # Set the up vector to the positive y-axis
    up_vector = np.array([0.0, 1.0, 0.0])

    # Sets the camera position, target point, and up vector specified
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              target_point[0], target_point[1], target_point[2],
              up_vector[0], up_vector[1], up_vector[2])

def main():
    pygame.init()
    display = (1250, 650)  # width, height of the display window
    pygame.display.set_caption('3D Solar System Simulation')
    # Set up the Pygame window mode for OpenGL rendering.
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    set_projection(display)

    # Planet Initializations
    sun = Planet(sun_radius, sun_texture, position = sun_position)
    mercury = Planet(mercury_radius, mercury_texture, position = mercury_position)
    venus = Planet(venus_radius, venus_texture, position = venus_position)
    earth = Planet(earth_radius, earth_texture, position = earth_position)
    mars = Planet(mars_radius, mars_texture, position = mars_position)
    jupiter = Planet(jupiter_radius, jupiter_texture, position = jupiter_position)
    saturn = Planet(saturn_radius, saturn_texture, position = saturn_position)
    uranus = Planet(uranus_radius, uranus_texture, position = uranus_position)
    neptune = Planet(neptune_radius, neptune_texture, position = neptune_position)    

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # for planet in planets:
        #     planet.update_rotation()

        # Clear the color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for planet in planets:
            glPushMatrix()
            glTranslatef(*planet.position)
            planet.apply_rotation()
            planet.shape()
            glPopMatrix()

        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL Error: {error}")

        # Flip the display to update the screen.
        pygame.display.flip()

        # Add a small delay to control the frame rate.
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
