"""
Team Member(s), ordered by contribution:
Features Added:
    1.bgm
    2.boundary for scene
    3.time limit: 
        ·Background color changes gradually, bomberman will die when it is completely dark
    4.four Elves
        ·move randomly
        ·added win symbol for Elves 
    5.Bomberman will die when it collides with Elves
    5.more power for bombs
    4.keyPressEvent for starting 
   
"""
from animations import QtGui, QtCore, QApplication, AnimatedScene, AnimatedItem, MessageItem, QSound
import random
import glob


class Bomberman(AnimatedItem):
    def __init__(self, scene, x=0, y=0, lives=2):
        super().__init__(scene, x, y)
        self.lives = lives
        self.i = 0
        """add Bomberman + 被炸flash"""
        self.animations.add("down", glob.glob("Sprites/Bomberman/Front/*"), interval=50)
        self.animations.add("up", glob.glob("Sprites/Bomberman/Back/*"), interval=50)
        self.animations.add("right", glob.glob("Sprites/Bomberman/Side/*"), interval=50)
        self.animations.add("left", glob.glob("Sprites/Bomberman/Side/*"), interval=50, horizontal_flip=True)
        self.animations.add("flash", [glob.glob("Sprites/Bomberman/Front/*")[0], None] * 4, interval=200)
        
        self.set_default_image("down")
        self.speed = 8  # how many pixels to move per frame
        # only the lower part (defined by collision_rect) of Bomberman can collide with other sprites
        self.collision_rect = QtCore.QRect(10, self.image.height() // 3 * 2,
                                            self.image.width() - 20, self.image.height() // 3)  
        self.setZValue(9999)  # bomberman is always on top of other sprites
        self.explosion_sound = QSound("bgm.wav")
        self.explosion_sound.play()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.count_down)
        self.timer.start(70000)
        
        self.destroy_timer = QtCore.QTimer()
        self.destroy_timer.timeout.connect(self.destroy)
        
    def move_left(self):
        if self.x() > 0:
            self.setX(self.x() - self.speed)
       
    def move_right(self):
        if self.x() < 640*2:
            self.setX(self.x() + self.speed)

    def move_up(self):
        if self.y() > 0:
            self.setY(self.y() - self.speed)

    def move_down(self):
        if self.y() < 640:
            self.setY(self.y() + self.speed)

    def place_bomb(self):
        Bomb(self.scene, self.x() + self.collision_rect.x(), self.y() + self.collision_rect.y())

    def keyPressEvent(self, event):  
        key = event.key()
        if key == QtCore.Qt.Key_Up:
            self.animations.play("up", on_transition=self.move_up)
        elif key == QtCore.Qt.Key_Down:
            self.animations.play("down", on_transition=self.move_down)
        elif key == QtCore.Qt.Key_Left:
            self.animations.play("left", on_transition=self.move_left)
        elif key == QtCore.Qt.Key_Right:
            self.animations.play("right", on_transition=self.move_right)
        elif key == QtCore.Qt.Key_Space:
            self.place_bomb()
        
    def on_collision(self, other):
        if isinstance(other, Flame) or isinstance(other, Creep) or isinstance(other, Grass) or isinstance(other, Potato) or isinstance(other, Wizard):
            self.destroy()

    def destroy(self):
        self.animations.play("flash", on_completion=super().destroy)
        message_item = MessageItem(scene)
        message_item.add("👻👻👻", last_for_seconds=100)
      
    def count_down(self):
        # self.animations.play("flash", on_completion=super().destroy)
        message_item = MessageItem(scene)
        message_item.add("🕖", last_for_seconds=1)
        message_item.add("🕗", last_for_seconds=1)
        message_item.add("🕘", last_for_seconds=1)
        message_item.add("🕙", last_for_seconds=1)
        message_item.add("🕚", last_for_seconds=1)
        message_item.add("🕛", last_for_seconds=1)
        self.destroy_timer.start(6000)
        
        
class Creep(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        # self.i = 0
        """add Creep + 被炸flash"""
        self.animations.add("down", glob.glob("Sprites/Creep/Front/*"), interval=50)
        self.animations.add("up", glob.glob("Sprites/Creep/Back/*"), interval=50)
        self.animations.add("right", glob.glob("Sprites/Creep/Side/*"), interval=50)
        self.animations.add("left", glob.glob("Sprites/Creep/Side/*"), interval=50, horizontal_flip=True)
        self.animations.add("flash", [glob.glob("Sprites/Creep/Front/*")[0], None] * 4, interval=200)
        self.animations.add("win", glob.glob("Sprites/Creep/Happy/*"))
        
        self.set_default_image("down")
        self.speed = 4  # how many pixels to move per frame
        # only the lower part (defined by collision_rect) of Bomberman can collide with other sprites
        self.collision_rect = QtCore.QRect(10, self.image.height() // 3 * 2,
                                            self.image.width() - 20, self.image.height() // 3)
        self.setZValue(9998)  # bomberman is always on top of other sprites
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.creep_win)
        self.timer.start(76000)
        
        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect(self.move_randomly)
        # self.move_timer.start(1000)
        
    def keyPressEvent(self, event):  
        key = event.key()
        if key == QtCore.Qt.Key_Enter:
            self.move_timer.start(1000)

    def move_left(self):
        if self.x() > 0:
            self.setX(self.x() - self.speed)

    def move_right(self):
        if self.x() < 640*2:
            self.setX(self.x() + self.speed)

    def move_up(self):
        if self.y() > 0:
            self.setY(self.y() - self.speed)

    def move_down(self):
        if self.y() < 640:
            self.setY(self.y() + self.speed)
        
    def move_randomly(self):
        random_number = random.randrange(0,4)
        
        if random_number == 0:
            self.animations.play("up", on_transition= self. move_up)
            
        elif random_number == 1:
            self.animations.play("down", on_transition= self. move_down)
            
        elif random_number == 2:
            self.animations.play("left", on_transition= self. move_left)
            
        elif random_number == 3:
            self.animations.play("right", on_transition= self. move_right)
            
    def on_collision(self, other):
        if isinstance(other, Flame):            
            self.destroy()
          
        elif isinstance(other, Bomberman):
            self.creep_win()

    def destroy(self):
        self.animations.play("flash", on_completion=super().destroy)
        
    def creep_win(self):
        
        self.animations.play("win")
            
    
class Grass(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        elves = self.animations.extract_images("Sprites/Elves/grass.png", n_rows=4, n_columns=4)
        self.animations.add("down", elves[0:4], interval=100)
        self.animations.add("left", elves[4:8], interval=100)
        self.animations.add("right", elves[8:12], interval=100)
        self.animations.add("up", elves[12:16], interval=100)
        self.animations.add("flash", [elves[0], None] * 4, interval=200)
        self.set_default_image("up")
        self.speed = 6  # how many pixels to move per frame
        # only the lower part (defined by collision_rect) of Bomberman can collide with other sprites
        self.collision_rect = QtCore.QRect(10, self.image.height() // 3 * 2,
                                            self.image.width() - 20, self.image.height() // 3)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.grasss_win)
        self.timer.start(76000)
        
        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect(self.move_randomly)
        # self.move_timer.start(1000)
        
    def keyPressEvent(self, event):  
        key = event.key()
        if key == QtCore.Qt.Key_Enter:
            self.move_timer.start(1000)
    
    def move_left(self):
        if self.x() > 0:
            self.setX(self.x() - self.speed)

    def move_right(self):
        if self.x() < 640*2:
            self.setX(self.x() + self.speed)

    def move_up(self):
        if self.y() > 0:
            self.setY(self.y() - self.speed)

    def move_down(self):
        if self.y() < 640:
            self.setY(self.y() + self.speed)
        
    def move_randomly(self):
        random_number = random.randrange(0,4)
        if random_number == 0:
            self.animations.play("up", on_transition=self.move_up)
        elif random_number == 1:
            self.animations.play("down", on_transition=self.move_down)
        elif random_number == 2:
            self.animations.play("left", on_transition=self.move_left)
        elif random_number == 3:
            self.animations.play("right", on_transition=self.move_right)
                
    def grasss_win(self):
        elves = self.animations.extract_images("Sprites/Elves/grass_w.png", n_rows=4, n_columns=4)
        self.animations.add("win", elves[0:1])
        self.animations.play("win")
       
    def on_collision(self, other):
        if isinstance(other, Flame):
            # if a Bomberman is hit by a flame, he will be destroyed
            self.destroy()
        elif isinstance(other, Bomberman):
            self.grasss_win()

    def destroy(self):
        self.animations.play("flash", on_completion=super().destroy)
        

class Potato(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        elves = self.animations.extract_images("Sprites/Elves/potato.png", n_rows=4, n_columns=4)
        self.animations.add("down", elves[0:4], interval=100)
        self.animations.add("left", elves[4:8], interval=100)
        self.animations.add("right", elves[8:12], interval=100)
        self.animations.add("up", elves[12:16], interval=100)
        self.animations.add("flash", [elves[0], None] * 4, interval=200)
        self.set_default_image("up")
        
        self.speed = 6  # how many pixels to move per frame
        # only the lower part (defined by collision_rect) of Bomberman can collide with other sprites
        self.collision_rect = QtCore.QRect(10, self.image.height() // 3 * 2,
                                            self.image.width() - 20, self.image.height() // 3)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.elves_win)
        self.timer.start(76000)
        
        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect(self.move_randomly)
        # self.move_timer.start(1000)
        
    def keyPressEvent(self, event):  
        key = event.key()
        if key == QtCore.Qt.Key_Enter:
            self.move_timer.start(1000)
    
    def move_left(self):
        if self.x() > 0:
            self.setX(self.x() - self.speed)

    def move_right(self):
        if self.x() < 640*2:
            self.setX(self.x() + self.speed)

    def move_up(self):
        if self.y() > 0:
            self.setY(self.y() - self.speed)

    def move_down(self):
        if self.y() < 640:
            self.setY(self.y() + self.speed)
        
    def move_randomly(self):
        random_number = random.randrange(0,4)
        if random_number == 0:
            self.animations.play("up", on_transition=self.move_up)
        elif random_number == 1:
            self.animations.play("down", on_transition=self.move_down)
        elif random_number == 2:
            self.animations.play("left", on_transition=self.move_left)
        elif random_number == 3:
            self.animations.play("right", on_transition=self.move_right)
                
    def elves_win(self):
        elves = self.animations.extract_images("Sprites/Elves/potato_w.png", n_rows=4, n_columns=4)
        self.animations.add("win", elves[0:1])
        self.animations.play("win", on_transition=self.move_down)
       
                
    def on_collision(self, other):
        if isinstance(other, Flame):
            # if a Bomberman is hit by a flame, he will be destroyed
            self.destroy()
        elif isinstance(other, Bomberman):
            self.elves_win()

    def destroy(self):
        self.animations.play("flash", on_completion=super().destroy)
        
        
class Wizard(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        elves = self.animations.extract_images("Sprites/Elves/wizard.png", n_rows=4, n_columns=4)
        self.animations.add("down", elves[0:4], interval=100)
        self.animations.add("left", elves[4:8], interval=100)
        self.animations.add("right", elves[8:12], interval=100)
        self.animations.add("up", elves[12:16], interval=100)
        self.animations.add("flash", [elves[0], None] * 4, interval=200)
        self.set_default_image("up")
        
        self.speed = 6  # how many pixels to move per frame
        # only the lower part (defined by collision_rect) of Bomberman can collide with other sprites
        self.collision_rect = QtCore.QRect(10, self.image.height() // 3 * 2,
                                            self.image.width() - 20, self.image.height() // 3)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.elves_win)
        self.timer.start(76000)
        
        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect(self.move_randomly)
        # self.move_timer.start(1000)
    
    def keyPressEvent(self, event):  
        key = event.key()
        if key == QtCore.Qt.Key_Enter:
            self.move_timer.start(1000)
  
    def move_left(self):
        if self.x() > 0:
            self.setX(self.x() - self.speed)

    def move_right(self):
        if self.x() < 640*2:
            self.setX(self.x() + self.speed)

    def move_up(self):
        if self.y() > 0:
            self.setY(self.y() - self.speed)

    def move_down(self):
        if self.y() < 640:
            self.setY(self.y() + self.speed)
        
    def move_randomly(self):
        random_number = random.randrange(0,4)
        if random_number == 0:
            self.animations.play("up", on_transition=self.move_up)
        elif random_number == 1:
            self.animations.play("down", on_transition=self.move_down)
        elif random_number == 2:
            self.animations.play("left", on_transition=self.move_left)
        elif random_number == 3:
            self.animations.play("right", on_transition=self.move_right)
                
    def elves_win(self):
        elves = self.animations.extract_images("Sprites/Elves/wizard_w.png", n_rows=4, n_columns=4)
        self.animations.add("win", elves[0:1])
        self.animations.play("win")
       
    def on_collision(self, other):
        if isinstance(other, Flame):
            # if a Bomberman is hit by a flame, he will be destroyed
            self.destroy()
        elif isinstance(other, Bomberman):
            self.elves_win()

    def destroy(self):
        self.animations.play("flash", on_completion=super().destroy)
        

class Bomb(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        self.animations.add("bomb", glob.glob("Sprites/Bomb/*"), repeat=3, interval=300)
        self.set_default_image("bomb")
        self.animations.play("bomb", on_completion=self.explode)
        self.explosion_sound = QSound("bomb_explosion.wav")

    def explode(self):
        self.explosion_sound.play()
        self.destroy()
        Flame(self.scene, self.x(), self.y())
        Flame(self.scene, self.x() + Flame.width(self), self.y())
        Flame(self.scene, self.x() - Flame.width(self), self.y())
        Flame(self.scene, self.x(), self.y() + Flame.height(self))
        Flame(self.scene, self.x(), self.y() - Flame.height(self))


class Flame(AnimatedItem):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y)
        images = self.animations.extract_images("Sprites/Flame/Flame.png", n_rows=1, n_columns=5)
        self.animations.add("flame", images, interval=500)
        self.set_default_image("flame")
        self.animations.play("flame", on_completion=self.destroy)
        self.collidable = False
        

class Background():
    def __init__(self):
        self.i = 175
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(2300)
    
    def update(self):
        if self.i >= 5:
            self.i -= 5 
            scene.setBackgroundBrush(QtGui.QColor(self.i, 0, 0)) 
            

if __name__ == "__main__":
    app = QApplication([])
    scene = AnimatedScene(640, 480)  
    scene.setBackgroundBrush(QtGui.QColor(190,0,0))
    background=Background()
    Bomberman(scene, 600, 400)  # put a Bomberman onto the scene at 300, 180
    Creep(scene, 800, 100)
    Creep(scene, 300, 300)
    Creep(scene, 300, 500)
    Grass(scene, 300, 100)
    Grass(scene, 800, 300)
    Grass(scene, 800, 500)
    Wizard(scene, 800, 500)
    Wizard(scene, 800, 500)
    Wizard(scene, 1200, 100)
    Potato(scene, 1200, 300)
    Potato(scene, 1200, 500)
    Potato(scene, 1200, 500)
    message_item = MessageItem(scene)
    message_item.add("Welcome to the world of Bomberman")
    message_item.add("To kill all the sprites before dark or they will kill you.", last_for_seconds=3) 
    message_item.add(" Be careful of the sprites and fire", last_for_seconds=2) 
    message_item.add("Enter: start; Arrows: move; Space: plant a bomb", last_for_seconds=7)  
    
    app.exec()
    
    
    
    