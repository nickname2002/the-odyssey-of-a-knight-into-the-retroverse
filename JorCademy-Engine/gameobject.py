from jorcademy import rect

class GameObject:

    def __init__(self, pos, w, h):
        self.x = pos[0]
        self.y = pos[1]
        self.width = w
        self.height = h


    def draw(self):
        rect((255, 50, 50), self.x, self.y, self.width, self.height)


    def collision(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2) <= (other.x + other.width / 2)
        
        # Check in range vertically
        in_y_range = (self.y + self.height / 2) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2) <= (other.y + other.height / 2)
        
        # Check horizontally and vertically in range
        return in_x_range and in_y_range
    
    
    def collision_top(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 10) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 10) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y - self.height / 2 - 10) <= (other.y + other.height / 2) and \
                     (self.y - self.height / 2 + 10) >= (other.y - other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range
    

    def collision_bottom(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 10) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 10) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 10) <= (other.y - other.height / 2) and \
                     (self.y + self.height / 2 + 10) >= (other.y - other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range


    def collision_left(self, other):
        # Check in range horizontally
        in_x_range = (self.x - self.width / 2 - 5) <= (other.x + other.width / 2) and \
                     (self.x - self.width / 2 + 5) >= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 5) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2 + 5) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range
    

    def collision_right(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 + 5) >= (other.x - other.width / 2) and \
                     (self.x + self.width / 2 - 5) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 5) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2 + 5) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    