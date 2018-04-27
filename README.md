# Bomber Man #

This is a simple "Bomber Man" game written in Python 3, based on the *PyGame* library.

![Bomber Man Snapshot](snap0.png?raw=true "snapshot")


## Download & Install ##

First clone the project available on GitHUB under GPL:

```
  $ git clone https://github.com/Zadrott/bomberman
```

To install Python (root privilege required):

```
  $ sudo apt get install python3 pip3
```

To install the *PyGame* library (user privilege enough):

```
  $ pip3 install pygame
```

To start the game:

```
  $ ./bomber_server.py 7777 maps/map0
```
Replace map0 by the map you want to use

```
  $ ./bomber_client.py localhost 7777 nick
```
Replace nick by the nickname you want to use

## Rules ##


To play, just use the following keys:
  * use *arrows* to move the current character
  * press *space* to drop a bomb at current position, that will explode after a delay of 5 seconds
  * press *escape* to quit the game

The implementation of this game follows a simple MVC architecture (Model/View/Controller).

## Known Bugs ##

* Disconnections aren't handled by the server.
* Fruits can by superimposed.
* The game isn't over if only one player remain.
* There is a [known bug](https://github.com/pygame/pygame/issues/331) in the *pygame.mixer* module, which causes high CPU usage, when calling *pygame.init()*. A workaround is to disable the mixer module, *pygame.mixer.quit()* or not to enable it, by using *pygame.display.init()* and *pygame.font.init()* instead. Consequently, there is no music, no sound :-(

## Documentation ##

  * https://www.pygame.org
  * https://openclassrooms.com/courses/interface-graphique-PyGame-pour-python/tp-dk-labyrinthe
  * http://ezide.com/games/writing-games.html
