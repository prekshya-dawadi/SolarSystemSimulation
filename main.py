import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from planet import Planet

magnification_big = 15
magnification_small = 5


# Planets Definitions

# Definition of Sun
sun_radius = 1
sun_texture = "D:/Graphics/SolarSystemSimulation/Textures/Sun.jpg"
sun_position = (0,0,0)

#Definition of mercury
mercury_radius = 0.0035*magnification_big
mercury_texture = "D:/Graphics/SolarSystemSimulation/Textures/mercury.jpg"
mercury_distance = 2
mercury_position = (mercury_distance,0,0)
mercury_speed = 1.4

#Definition of venus
venus_radius = 0.0087*magnification_big
venus_texture = "D:/Graphics/SolarSystemSimulation/Textures/uranus.jpg"
venus_distance = 3
venus_position = (venus_distance,0,0)
venus_speed = 1.2

#Definition of earth
earth_radius = 0.0092*magnification_big
earth_texture = "D:/Graphics/SolarSystemSimulation/Textures/earth.jpg"
earth_distance = 4
earth_position = (earth_distance,0,0)
earth_speed = 1.0


#Definition of mars
mars_radius = 0.0049*magnification_big
mars_texture = "D:/Graphics/SolarSystemSimulation/Textures/mars.jpg"
mars_distance = 5
mars_position = (mars_distance,0,0)
mars_speed = 0.8


#Definition of jupiter
jupiter_radius = 0.103*magnification_small
jupiter_texture = "D:/Graphics/SolarSystemSimulation/Textures/jupiter.jpg"
jupiter_distance = 6.5
jupiter_position = (jupiter_distance,0,0)
jupiter_speed = 0.6

#Definition of saturn
saturn_radius = 0.087*magnification_small
saturn_texture = "D:/Graphics/SolarSystemSimulation/Textures/saturn.jpg"
saturn_distance = 8
saturn_position = (saturn_distance,0,0)
saturn_speed = 0.55

#Definition of uranus
uranus_radius = 0.037*magnification_small
uranus_texture = "D:/Graphics/SolarSystemSimulation/Textures/uranus.jpg"
uranus_distance = 9
uranus_position = (uranus_distance,0,0)
uranus_speed = 0.5

#Definition of neptune
neptune_radius = 0.036*magnification_small
neptune_texture = "D:/Graphics/SolarSystemSimulation/Textures/neptune.jpg"
neptune_distance = 10
neptune_position = (neptune_distance,0,0)
neptune_speed = 0.45



def set_projection(display):
    # sets the current matrix mode to projection matrix. Subsequent operations will affect the projection matrix
    glMatrixMode(GL_PROJECTION)
    # Loads identity matrix to current matrix stack. Effectively resets the matrix to an inital state. 
    glLoadIdentity()
    # Configures a perspective projection. 
        # Parameters - field of view (45 degrees), aspect ratio of the window, near clipping plan distance(0.1 units), far clipping plane distance (50.0 units)
    gluPerspective(45, (display[0]/display[1]), 0.0, 15.0)
    # Switches the matrix mode back to the modelview matric for subsequent transformations
    
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glDepthFunc(GL_LEQUAL)   # Set the depth comparison function
    
    glMatrixMode(GL_MODELVIEW)
    # Loads the identity matrix onto the modelview matrix stack. This resets the modelview matrix
    glLoadIdentity()

    camera_distance = 15
        
    # Set the camera position to a point slightly above the orbit
    camera_pos = np.array([0,
                           10, 
                           camera_distance])

    # Set the target point to the center of the solar system
    target_point = np.array([0.0, 0.0, 0.0])

    # Set the up vector to the positive y-axis
    up_vector = np.array([0.0, 1.0, 0.0])

    # Sets the camera position, target point, and up vector specified
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              target_point[0], target_point[1], target_point[2],
              up_vector[0], up_vector[1], up_vector[2])
    

def milky_way():
    glColor3f(1.0, 1.0, 1.0)  # Set star color to white
    glPointSize(2.0)  # Set the size of stars

    glBegin(GL_POINTS)  # Start drawing stars
    num_stars = 50  # Number of stars to draw

    for _ in range(num_stars):
        brightness = np.random.uniform(0.5, 1.0)
        glColor3f(brightness, brightness, brightness)
        # Generate random star positions in the range [-20, 20]
        x = np.random.uniform(-20.0, 20.0)
        y = np.random.uniform(-20.0, 20.0)
        z = np.random.uniform(-20.0, 20.0)
        glVertex3f(x, y, z)  # Draw a star at the generated position

    glEnd()  # End drawing stars



def main():
    pygame.init()
    display = (1250, 650)  # width, height of the display window
    pygame.display.set_caption('3D Solar System Simulation')
    # Set up the Pygame window mode for OpenGL rendering.
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    set_projection(display)

    # Planet Initializations
    sun = Planet(sun_radius, sun_texture, 0, position = sun_position)
    mercury = Planet(mercury_radius, mercury_texture, mercury_speed, position = mercury_position, orbital_distance=mercury_distance)
    venus = Planet(venus_radius, venus_texture, venus_speed, position = venus_position, orbital_distance=venus_distance)
    earth = Planet(earth_radius, earth_texture, earth_speed, position = earth_position, orbital_distance=earth_distance)
    mars = Planet(mars_radius, mars_texture, mars_speed, position = mars_position, orbital_distance=mars_distance)
    jupiter = Planet(jupiter_radius, jupiter_texture, jupiter_speed, position = jupiter_position, orbital_distance=jupiter_distance)
    saturn = Planet(saturn_radius, saturn_texture, saturn_speed, position = saturn_position, orbital_distance=saturn_distance)
    uranus = Planet(uranus_radius, uranus_texture, uranus_speed, position = uranus_position, orbital_distance=uranus_distance)
    neptune = Planet(neptune_radius, neptune_texture, neptune_speed, position = neptune_position, orbital_distance=neptune_distance)    

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Clear the color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        milky_way()

        for planet in planets:
            planet.update_rotation()
            planet.position = planet.calculate_orbital_position()


        for planet in planets:
            print(f"Planet {planet}: Position{planet.position}")
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
