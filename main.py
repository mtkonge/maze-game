import os
from sys import platform
import shutil
from result import Ok, Err, Result



def clear_console():
    if platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

def print_position(one_line: int, current_position:int, maze: str):
    clear_console()
    print(f"{maze[current_position-one_line-1]}{maze[current_position-one_line]}{maze[current_position-one_line+1]}")
    print(f"{maze[current_position-1]}{maze[current_position]}{maze[current_position+1]}")
    print(f"{maze[current_position+one_line-1]}{maze[current_position+one_line]}{maze[current_position+one_line+1]}")

def get_current_position(maze:str):
    for i in range(len(maze)):
            if maze[i] == ">":
                return i
    raise Exception("No start position in maze")

def move(maze: str, current_position: int, destination: int):
    maze_list = list(maze)
    maze_list[current_position] = " "
    maze_list[destination] = ">"
    # the same but with substring instead, i chose the above because it looked cleaner
    # maze_removed_current_position = maze[:current_position] + " " + maze[current_position+1:]
    # maze_new_position = maze_removed_current_position[:destination] + ">" + maze_removed_current_position[destination+1:]
    return maze_list

def has_won(maze: str, destination: int):
    return maze[destination] == "e"

def win():
    clear_console()
    win_text = open("assets/victory.txt", "r").read()
    print(win_text)

def specific_move(maze: str, current_position: int, one_line: int, destination:int):
    if has_won(maze, destination):
        return Ok("Win")
    if maze[destination] == "#":
        return Err("Path blocked, try again")
    else:
        return Ok(move(maze, current_position, destination))

def move_logic(inp, maze: str, current_position: int, one_line: int) -> Result[str, str]:
    if inp == "w":
        destination = current_position-one_line
        return specific_move(maze, current_position, one_line, destination)
    elif inp == "s":
        destination = current_position+one_line
        return specific_move(maze, current_position, one_line, destination)
    elif inp == "a":
        destination = current_position-1
        return specific_move(maze, current_position, one_line, destination)
    elif inp == "d":
        destination = current_position+1
        return specific_move(maze, current_position, one_line, destination)
    else:
        return Err("Input invalid, use wasd to move around")

def main():
    one_line = 37
    errormsg = ""
    maze = open("assets/maze.txt", "r").read()
    while True:
        current_position = get_current_position(maze)
        print_position(one_line, current_position, maze)
        print(errormsg)
        inp = input("")
        move_result = move_logic(inp, maze, current_position, one_line)
        if isinstance(move_result, Ok):
            if move_result.ok_value == "Win":
                win()
                input("Press enter to quit >")
                clear_console()
                return
            errormsg = ""
            maze = move_result.ok_value
        else:
            errormsg = move_result.err_value
        
        

if __name__ == "__main__":
    main()

