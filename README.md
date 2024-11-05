# Suikapy

This is my version of a Suika game written in Python using Pygame.

If you don't know what a [Suika](https://suikagame.com/) game is, it's basically a game where you have to combine fruits together to make a bigger fruit. The objective is to get bigger fruits, with the biggest being a watermelon. When you combine two watermelons, they explode and give you more points.

I played a game called **Melon Maker** on Android, but I think the original game is called **Watermelon game**.

This is an interesting project to develop, because a Suika game relies on a physics engine. I haven't done any physics simulation in Python, so I thought this could be a good starting point. This game uses [Pymunk](http://www.pymunk.org/en/latest/index.html).

Last time I tried to get a Physics engine working in a game was a test project, and I failed miserably. This time I actually read the documentation of Pymunk and tried to make sense of how to use it.

Right now you can pretty much do the same things you do in the original Suika game, but I haven't implemented a **Game over**.

There are a few bugs here and there in this implementation (like the fact that you can combine fruits even before they get to the bottom of the container), but it's still pretty functional overall.

I might polish this in the future and give it a few sprites, a high score system, and a game over screen to make it a bit more fun to look at.

## Installation

I use [Poetry](https://python-poetry.org/) to manage dependencies. To install the game's dependencies, you need to run:

```
poetry install
```

That should install all that you need to run. Then you just run:

```
poetry run python src/game.py
```

And you can play it.


## Controls

Left mouse button - Release the fruit.
R - Reset the game.


That's it.
