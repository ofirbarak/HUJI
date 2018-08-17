#######################################
# FILE : hello_turtle.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex1 2015-2016
# DESCRIPTION: A program that uses turtle module and contain a method that
# print to the the standard output (screen) 3 flowers.
#######################################
import turtle

"""Uses the turtle to draw a single petal"""
def draw_petal():
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)

"""Draws a flower using the turtle.
The flower is made up of 4 petals.
"""
def draw_flower():
    turtle.right(45)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(135)
    turtle.forward(150)

"""Draws a flower using the turtle.The flower is made up of 4 petals,
and move the turtle's head in order to draw more flowers.
"""
def draw_flower_advanced():
    draw_flower()
    turtle.left(90)
    turtle.up()
    turtle.forward(150)
    turtle.left(90)
    turtle.forward(150)
    turtle.right(90)
    turtle.down()

"""Draw 3 flower using other 3 methods"""
def draw_flower_bed():
    turtle.up()
    turtle.left(180)
    turtle.forward(200)
    turtle.right(180)
    turtle.down()
    draw_flower_advanced()
    draw_flower_advanced()
    draw_flower_advanced()


draw_flower_bed()

