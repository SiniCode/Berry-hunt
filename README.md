# Berry Hunt

This is a pygame practice project.

The player controls a bear and tries to pick as many berries as possible.
* The bear can move upwards, downwards, to the right, and to the left. Pressing the arrow keys change the direction.
* The bear has four speed options. Pressing the same arrow key repeatedly accelerates the speed.
* The game keeps score of the picked berries and saves new records. The player can set the record back to zero by clicking that option on the game display.

If the bear runs into a wall or a tiger (bear's natural predator), the game is over.

Simple but surprisingly addictive...

## Command Line

### Install dependencies before first run:
```bash
poetry install
```

### Run the application:
```bash
poetry run invoke start
```
