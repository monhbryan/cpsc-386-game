import cocos
import random
import pyglet
from cocos.director import director
from pyglet.window import mouse
       
moneyCount = 10000 #Displays current money
currentBet = 1000 #Current Betting Amount
doorSelect = -1 # Player selected door (1-3)
doorCorrect = 0 # Randomized Correct Door (1-3)
doorPos= [(0,0),(320,400), (640,400), (960,400)] #Locations of door, 0 is error
doubleCounter = 1 #Exponent of 2 (2^doubleCounter)

def on_newGame(self):
        global doorCorrect
        global doorSelect
        global moneyCount
        global currentBet
        if moneyCount < currentBet:
            currentBet = moneyCount
            print("Current money is less than bet")
        if moneyCount <= 0: #Lose 
            print("Lost")
            lose_scene = cocos.scene.Scene()
            menu_layer = RestartMenu()
            label_layer = LoseLabel()
            lose_scene.add(menu_layer)
            lose_scene.add(label_layer)
            return lose_scene

        elif moneyCount >= 1000000: #Win
            print("Win")
            win_scene = cocos.scene.Scene()
            menu_layer = RestartMenu()
            label_layer = WinLabel()
            win_scene.add(menu_layer)
            win_scene.add(label_layer)
            return win_scene

        else:
            scene = cocos.scene.Scene()
            doorCorrect = random.randint(1,3)
            #Debugging correct door.
            # print (str(doorCorrect)) 
            doorSelect = 0 #initializes selection 

            money1 = MoneyCounter()
            bet1 = Bet_Button()

            sprite1 = Sprite_Door(1)
            sprite1.spr.position = doorPos[1]
            sprite1.spr.num = 1

            sprite2 = Sprite_Door(1)
            sprite2.spr.position = doorPos[2]
            sprite2.spr.num = 2

            sprite3 = Sprite_Door(1)
            sprite3.spr.position = doorPos[3]
            sprite3.spr.num = 3

            scene.add(sprite1)
            scene.add(sprite2)
            scene.add(sprite3)
            scene.add(money1)
            scene.add(bet1)

            return scene


class MoneyCounter(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        moneyString = "$" + str(moneyCount)
        label = cocos.text.Label(moneyString, font_name ="Times New Roman", font_size=32, anchor_x ="center", anchor_y="center")
        label.position = (640,200)
        self.add(label)

        doubleString = "Current Double-Downs: " + str(doubleCounter) + " times"
        label2 = cocos.text.Label(doubleString, font_name ="Times New Roman", font_size=32, anchor_x ="center", anchor_y="center")
        label2.position = (640, 100)
        self.add(label2)
        
        betString = "Bet Money: $" + str(currentBet)
        label3 = cocos.text.Label(betString, font_name = "Times New Roman", font_size=32, anchor_x="center", anchor_y="center")
        label3.position = (640,675)
        self.add(label3)


class textConfirm(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        confirmLabel = "One of the false doors have been removed, do you want pick the other door?"
        label = cocos.text.Label(confirmLabel, font_name = "Times New Roman", font_size=16, anchor_x="center", anchor_y="center")
        label.position = (650,540)
        self.add(label)


class Sprite_Door(cocos.layer.Layer):
    is_event_handler = True #allows for mouse operations

    def __init__(self,selectable): #selectable is 1 for true, 0 for false
        self.selectable = selectable
        super().__init__()
        self.spr = cocos.sprite.Sprite("resources/Door.png")
        self.add(self.spr,0,"door")
        self.num = 0

    def on_mouse_press(self,x,y, button, modifiers):
        global doorSelect
        if button & mouse.LEFT & self.selectable == 1:
            if self.get("door").contains(x,y):
                print("Clicked door: " + str(self.spr.num))
                doorSelect = self.spr.num
                print("Selected a door")
                
                if doorSelect == doorCorrect:
                    idoorList = [1,2,3]
                    idoorList.remove(doorCorrect) 
                    falseDoor = random.choice(idoorList) #Randomized false door
                    doorList = [doorCorrect, falseDoor]

                else: #picked the wrong door 
                    doorList = [doorCorrect, doorSelect]
                #Build next scene
                confirm_Layer = cocos.scene.Scene()
                if 1 in doorList:
                    sprite1 = Sprite_Door(0)
                    sprite1.spr.position = doorPos[1]
                    sprite1.spr.num = 1
                    confirm_Layer.add(sprite1)
                if 2 in doorList:
                    sprite2 = Sprite_Door(0)
                    sprite2.spr.position = doorPos[2]
                    sprite2.spr.num = 2
                    confirm_Layer.add(sprite2)
                if 3 in doorList:
                    sprite3 = Sprite_Door(0)
                    sprite3.spr.position = doorPos[3]
                    sprite3.spr.num = 3
                    confirm_Layer.add(sprite3)

                sprite4 = Door_Select()
                sprite4.spr.position = doorPos[doorSelect]
                confirm_Layer.add(sprite4)

                confirmScene = Confirmation(doorList)
                textScene = textConfirm()

                confirm_Layer.add(confirmScene)
                confirm_Layer.add(textScene)
                director.pop()
                director.push(confirm_Layer)

class Confirmation(cocos.menu.Menu):
     def __init__(self, dlist):
        super().__init__("Confirmation Menu")
        self.dlist = dlist

        
        items = []
        items.append (cocos.menu.MenuItem("Yes", self.on_yes))
        items[0].y = -100
        items.append (cocos.menu.MenuItem("No", self.on_no))
        items[1].y = -200
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back() )
     def on_yes(self):
         global doorSelect
         print("yes")
         self.dlist.remove(doorSelect)
         doorSelect = self.dlist[0]

         if doorSelect == doorCorrect:
             self.correct()

         else:
             self.incorrect()


     def on_no(self):
         print("no")
         if doorSelect == doorCorrect:
             self.correct()
         else:
             self.incorrect()

     def correct(self):
        double_Layer = cocos.scene.Scene()
        print("correct choice")

        sprite1= True_Door()
        sprite1.spr.position = doorPos[doorSelect]
        double_Layer.add(sprite1)
        DoubleMenuScene = DoubleDownMenu()
        DoubleDownScene = DoubleDown()
        double_Layer.add(DoubleMenuScene)
        double_Layer.add(DoubleDownScene)

        director.pop()
        director.push(double_Layer)

     def incorrect(self):
        print("wrong choice")
        wrong_Layer= cocos.scene.Scene()

        sprite1=False_Door()
        sprite1.spr.position = doorPos[doorSelect]
        wrong_Layer.add(sprite1)
        
        sprite2=Door_Select()
        sprite2.spr.position= doorPos[doorSelect]
        wrong_Layer.add(sprite2)

        sprite3=WrongChoice()
        wrong_Layer.add(sprite3)

        sprite4=WrongMenu()
        wrong_Layer.add(sprite4)

        director.pop()
        director.push(wrong_Layer)

class True_Door(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.spr = cocos.sprite.Sprite("resources/TrueDoor.png")
        self.spr.position = (0,0)
        self.add(self.spr)

class False_Door(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.spr = cocos.sprite.Sprite("resources/FalseDoor.png")
        self.spr.position = (0,0)
        self.add(self.spr)

class Door_Select(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.spr = cocos.sprite.Sprite("resources/DoorSelect.png")
        self.spr.position = (0,0)
        self.add(self.spr)

class DoubleDown(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        confirmLabel = "Would you like to double down?"
        label = cocos.text.Label(confirmLabel, font_name = "Times New Roman", font_size=16, anchor_x="center", anchor_y="center")
        label.position = (650,540)
        self.add(label)

class DoubleDownMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__("Double Down Menu")
        items = []
        items.append (cocos.menu.MenuItem("Yes", self.on_dyes))
        items[0].y = -100
        items.append (cocos.menu.MenuItem("No", self.on_dno))
        items[1].y = -200
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back() )
    def on_dyes(self):
        global doubleCounter
        doubleCounter +=1 
        director.pop()
        director.push(on_newGame(self))
    def on_dno(self):
        global doubleCounter
        global currentBet
        global moneyCount
        moneyCount += currentBet * (2 ** doubleCounter)
        doubleCounter = 1 #resets counter
        director.pop()
        director.push(on_newGame(self))

class WrongChoice(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        loseMoney = "You lost $" + str(currentBet) #Lose bet
        label = cocos.text.Label (loseMoney, font_name="Times New Roman", font_size=16, anchor_x="center", anchor_y="center")
        label.position = (650,540)
        self.add(label)

class WrongMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__("Incorrect Choice")
        items =[]
        items.append (cocos.menu.MenuItem("OK", self.on_ok))
        items[0].y = -200
        self.create_menu(items)
    def on_ok(self):
        global doubleCounter
        global moneyCount
        moneyCount -= currentBet # Lose bet but not double downed money
        doubleCounter = 1 #reset double down
        director.pop()
        director.push(on_newGame(self))

class BetMoney(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        label = cocos.text.Label("Input Betting Amount (Press Enter to continue): ", font_name="Times New Roman", font_size = 16, anchor_x="center", anchor_y="center")
        label.position = (640,360)
        self.add(label)
        label2 = cocos.text.Label("Raw Positive Integers only!", font_name="Times New Roman", font_size = 16, anchor_x="center", anchor_y="center")
        label2.position = (640, 460)
        self.add(label2)

        label3 = cocos.text.Label("You cannot bet more than your current amount!", font_name="Times New Roman", font_size=16, anchor_x="center", anchor_y="center")
        label3.position = (640, 560)
        self.add(label3)

        self.text = cocos.text.Label("", x=640, y=260)
        self.keys_pressed = ""
        self.update_text()
        self.add(self.text)
        

    def update_text(self):
        self.text.element.text = self.keys_pressed

    def on_key_press(self, key,modifiers):
        print(key)
        global currentBet
        if key == pyglet.window.key.ENTER:
            print ("You Entered: {}".format(self.keys_pressed))
            if(int(self.keys_pressed) <= moneyCount):
                currentBet = int(self.keys_pressed)
            else:
                print("Invalid Entry")
                currentBet = 1000
            director.pop()
            director.push(on_newGame(self))
        else:
            kk = pyglet.window.key.symbol_string(key)
            if kk == "BACKSPACE":
                self.keys_pressed = self.keys_pressed[:-1]
            else:
                kk = kk[1:] #Removes the _ from the raw input...
                self.keys_pressed = self.keys_pressed + kk
        self.update_text()

class Bet_Button(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.spr = cocos.sprite.Sprite("resources/BetButton.png")
        self.spr.position = (640,600)
        self.add(self.spr,0,"bet")

    def on_mouse_press(self,x,y, button, modifiers):
         if button & mouse.LEFT:
             if self.get("bet").contains(x,y):
                 bet_scene = cocos.scene.Scene()
                 bet_layer= BetMoney()
                 bet_scene.add(bet_layer)
                 director.pop()
                 director.push(bet_scene)

class LoseLabel(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        label = cocos.text.Label("You have lost all your money! You lose!", font_name= "Times New Roman",font_size = 32, anchor_x="center", anchor_y="center" )
        label.position = 640,460
        self.add(label)

class WinLabel(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        label1 = cocos.text.Label("You are now a millionaire! You win!", font_name = "Times New Roman", font_size = 32, anchor_x="center", anchor_y="center")
        label1.position = 640,460
        self.add(label1)

class RestartMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__("Restart Menu")
        items = []
        items.append(cocos.menu.MenuItem("Restart", self.on_restart))
        items[0].y = -100
        items.append(cocos.menu.MenuItem("Quit", self.on_quit))
        items[1].y = -200
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back() )

    def on_restart(self): #set global variables to default
        global doubleCounter
        global moneyCount
        global currentBet
        global doorSelect
        global doorCorrect
        moneyCount = 10000 
        currentBet = 1000
        doubleCounter = 1 
        doorSelect = -1
        doorCorrect = 0

        director.pop()
        director.push(on_newGame(self))

    def on_quit(self):
        director.window.close()

