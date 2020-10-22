import cocos
import random
from cocos.director import director
from pyglet.window import mouse



class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__("Money Doors")

        items = []
        items.append (cocos.menu.MenuItem("Start Game", self.on_start_game))
        items.append (cocos.menu.MenuItem("Quit", self.on_quit))
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back() )


    def on_start_game(self):
        import game_view
        director.push(game_view.on_newGame(self))
        
    def on_quit(self):
        director.window.close()


if __name__ == "__main__":
    director.init(width = 1280, height=720, caption="Money Doors")

    menu = MainMenu()
    menu_layer = cocos.scene.Scene()
    menu_layer.add(menu)

    director.run(menu_layer)
