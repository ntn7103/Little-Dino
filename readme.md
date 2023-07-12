
All class for object in this project are inheritated from pygame.sprite.Sprite, which has some main methods:
- .update()
- .draw()
- self.image

To display and use all sprite objects, I use 3 attributes:
- all_sprites: to display and update movement of all object
- bats: group of bats
- bullets: group of bullets
in file utils.py

# spritesheet.py
Because animation are in sprite sheet form, so a special class to handle them are needle.
- get_sprite(): to cut image from sprite sheet.

# bat.py
Bat is a basic model, other objects are mostly with same method and attributes
some type of attribute are:
- sprites group: where save frame
- position variables: to positioning the object
- speed_x, speed_y: speed (and direction) of object
- current_time, last_time: for frame cooldown (to slowdown frame speed)
- is_death: to show death sprites.

- update(): for movement, change frame, flip follow direction.
- collide(): if bat touch player, it reverese direction
- get_frame() and get_death_frame(): just like its name.


# bullet.py
- similar to bat.py
# player.py
- mostly same as bat.py, with extra attributes:

- last_short: for skill cooldown
- is_mini: to display mini 
- hurt: just like bat.is_death, to display hurt frames
- state: there are 4 state of of play:
    - 0: idle state
    - 1: running state
    - 2: running state
    - 3: hurt state

- change_mini(): change scale, and fixed position
- update(): implement some state of player, movement, skill...
    - with state, I can change frame type easily
- get_frame(): simply get frame, flip image, scaling.
- shoot(): when skill not in cooldown, create a shoot object.


# boss.py
Boss is an animal. Like its name, Cat is boss.
What can boss do? Walk and walk

- almost attributes are similar to bat.py
- I wanted to make skill for boss, some magic spells. When cat casting spell, it has to stay idle state (player can shoot easily). But with less of time, I have to remove that.

# Visualization:
<img width="707" alt="Ảnh màn hình 2023-07-12 lúc 11 38 45 SA" src="https://github.com/ntn7103/Little-Dino/assets/138243053/cda75c07-4c28-4c9f-92b5-1680e0634b71">

<img width="794" alt="Ảnh màn hình 2023-07-10 lúc 11 15 47 SA" src="https://github.com/ntn7103/Little-Dino/assets/138243053/72f5b3ef-b439-488d-bc51-462f4f2602d5">
<img width="709" alt="Ảnh màn hình 2023-07-12 lúc 11 39 17 SA" src="https://github.com/ntn7103/Little-Dino/assets/138243053/106eb2ca-f0f2-47f7-b5df-cccb7fb5715d">
<img width="710" alt="Ảnh màn hình 2023-07-12 lúc 11 39 51 SA" src="https://github.com/ntn7103/Little-Dino/assets/138243053/33efe485-dfee-42f0-9f97-011825eea4f7">



