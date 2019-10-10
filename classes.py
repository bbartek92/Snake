import numpy as np
import random as rnd

class Snake():
    # stores data where Snake is, 
    # which directions it's heading
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction
    
    def take_step(self, position):
        #add position to the body, pop off last position
        self.body = np.vstack((self.body[1:], position))
    
    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.body[-1]

    def grow(self):
        self.body = np.vstack((self.body[0], self.body))


class Apple():
    # stores Apple's location
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.get_location()
    
    def get_location(self):
        rand_height = rnd.randint(0, self.height-1)
        rand_width = rnd.randint(0, self.width-1)
        self.location = rand_height, rand_width


#directions:
up = np.asarray((-1, 0))
down = np.asarray((1, 0))
left = np.asarray((0, -1))
right = np.asarray((0, 1))

class Game():
    # input from the player
    # display the board
    # keep track of points total
    # etc.
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = Snake(np.asarray([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]), down)
        self.apple = Apple(self.height, self.width)
        self.score = Score()


    def board_matrix(self):
        matrix = np.full((self.height, self.width), None)
        matrix = np.asarray(matrix)
        matrix[self.apple.location[0]][self.apple.location[1]] = '*'
        for x, y in self.snake.body[:-1]:
            matrix[x][y] = 'O'
        matrix[self.snake.head()[0]][self.snake.head()[1]] = 'X'
        return matrix

    def render(self):
        matrix = self.board_matrix()
        print('+', '-'*((self.width*2)-1), '+')
        for row in matrix:
            print('|', *self.render_support(row), '|')
        print('+', '-'*((self.width*2)-1), '+')
    
    def render_support(self, row):
        '''changes None to " "'''
        row_temp = np.copy(row)
        for cell in range(len(row_temp)):
            if row[cell] == None:
                row_temp[cell] = ' '
            else:
                row_temp[cell] = row[cell]
        return row_temp

    def take_direction(self):
        step = input()
        #direction + body = position
        if step == 'w' and not (self.snake.direction==down).all():
            self.snake.set_direction(up)
        if step == 'a' and not (self.snake.direction==right).all():
            self.snake.set_direction(left)
        if step == 's' and not (self.snake.direction==up).all():
            self.snake.set_direction(down)
        if step == 'd' and not (self.snake.direction==left).all():
            self.snake.set_direction(right)      

    def calc_position(self):
        position = np.add(self.snake.head(), self.snake.direction)
        #check if step goes into snakes body
        for part in self.snake.body:
            if (position==part).all():
                print('Dead Snake\nThe Game is Over')
                print('Your Score is:', self.score.player_score)
                position = np.array([None, None])
        #handle board edge cases 
        if position[0] == 10:
            position[0] = 0
        if position[0] == -1:
            position[0] = 9
        if position[1] == 10:
            position[1] = 0
        if position[1] == -1:
            position[1] = 9
        #check the apple
        self.eat_apple(position)
        return position
    
    def eat_apple(self, position):
        loc_apple = np.asarray([self.apple.location[0], self.apple.location[1]])
        if (position==loc_apple).all():
            #new apple
            self.apple.get_location()
            #larger snake
            self.snake.grow()
            #player gets point
            self.score.add_point()

class Score():
    def __init__(self):
        self.player_score = 0
    
    def add_point(self):
        self.player_score += 1


if __name__ == "__main__":
    print('This is classes module')