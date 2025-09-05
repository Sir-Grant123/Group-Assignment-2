"""Group name: CAS15
Group member1: Atulya Subedi, Student ID: S394148
Group member2: Oliver Charles Cole, Student ID: S368184
Group member3: Megh RakeshKumar Brahmbhatt, Student ID: S394095
"""
# importing turtle module required for the assignment
import turtle


# function to draw the geometric pattern using recursive function 
def koch_segment(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    #dividing the edge into three equal segments
    piece = length / 3.0
    koch_segment(piece, depth - 1)
    turtle.left(60)
    koch_segment(piece, depth - 1)
    turtle.right(120)
    koch_segment(piece, depth - 1)
    turtle.left(60)
    koch_segment(piece, depth - 1)

def draw_polygon_with_koch(n_sides, side_len, depth):
    if n_sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    turn = 360.0 / n_sides
    for _ in range(n_sides):
        koch_segment(side_len, depth)
        turtle.left(turn)

def setup():
    turtle.reset()
    turtle.penup()
    turtle.goto(0, 0)
    turtle.setheading(0)
    turtle.pendown()


# function that reads user inputs from the users
def read_user_inputs():
    try:
        n = int(input("Enter the number of sides: ").strip())
        L = float(input("Enter side length: ").strip())
        d = int(input("Enter recursion depth: ").strip())
    except ValueError:      # raises valueError if the input is other expect numbers
        print("Input error: please enter numbers.")
        return None

    if n < 3:
        print("Number of sides must be at least 3.")
        return None
    if d < 0:
        print("Depth must be >= 0.")
        return None
    return n, L, d

def main():
    params = read_user_inputs()
    if params is None:
        return
    n_sides, side_len, depth = params
    setup()
    draw_polygon_with_koch(n_sides, side_len, depth)
    turtle.hideturtle()
    turtle.done()

main()
