# MUON
#### Video Demo:  https://www.youtube.com/watch?v=DJecTLhjAvY
#### Description:

  MUON is a Bullet Hell Boss fight game, where the objective is to defeat the Boss!

  The player is able to walk in all directions in a top down view, and shoot projectiles to the cursor position. Hitting the boss lowers his Hp bar and if you manage to get it to zero, you defeated the boss! But it isn't so simple, the boss has 3 Phases, in which each phase has 2 Patterns of 2 attacks, that when combined, creates Bullet Hell! If the player gets hit 6 times, lowering its hp to zero, then the boss wins.

  > Lets take a look at every script that makes the game.

# Resource

  This Script handles essential resources that the game needs to work. This includes the basics like Fonts, Screen width and Height, Base Surface where everything is rendered, mixer to handle sound, Colors, Cursor image and Frames Per Second (FPS) locking.

  As I decided that I wanted to make a pixel art style game, I needed to change a few things like Screen Height and Width. If I rendered everything in a big window size, the pixel art would be so small, and even if i just drew a bigger pixel art instead, it wouldn't be really pixel art, as it gets bigger the "block" aspect of the pixels would be missing. To fix this, in the Resource script, I have 4 Screen Height's and Width's.
The Base Surface of the game is a small window defined by SCREEN_WIDTH and SCREEN_HEIGHT, this Base Surface is used then to render the pixel art in this surface, and in main loop of the game we scale the Base Surface by two, making it then to the normal Display size of the game, but maintaining the Pixel Art aspect of the game as the Pixel art and Every element was Scaled up.


# Main

  The Main script is where the game loop happens. It has the main Loop, every Menu state of the game, and most importantly, the Player Class. This Class manages everything related to the player. It keeps track of its Position, Image/animation, Health, Size in Width and Height, Collision Rectangle and Shooting cooldown. 
  
  For its functions, we have move() that handles keyboard input to change the player position on the screen by updating its X and Y, draw() to make it so the animation/image of the player follows its X/Y position and also draws the Heart so you can see the current Player's Hp in the screen. The shoot() function handles the player projectile shooting. In summary, this function keeps track of the mouse position and mouse event (pressing Mouse1), so when the player presses Mouse1, it gets the cursor position as the direction of the bullet, and the current player position (Where the bullet is coming from), and appends to a projectile Class that makes all the drawing and updating (I will explain this later on). And lastly, the damage() just keeps track of the player's hp and hit sound.

  In the main play() loop, every class is reset as the game starts, this loop handles every projectile and moving functions of both the Boss and the Player class. It also keeps track of both entities hps, so it switches Menu based on defeat or win.

  The redraw_window() is Where all the draw() functions from entities and projectiles are sent, so it can draw, upscale and keep track of sprites/animations positions.

# Boss

  Boss.py handles everything related to the Boss functionalities. A lot in this class is the same as the Player class, so everything from position, drawing, health and shooting cooldown is the same. The main difference here is the Phase and Pattern handling. In self.patterns, we have a dictionary of nested phases and patterns, where for each phase has 2 patterns, and each pattern has 2 attacks. This attacks stores info as bullet count, delay, repetition and last shot, all of this info goes to the shoot() function, that with index handling, we can access each pattern attacks individually and decide how are we gonna send this to the Bullet class (will explain later). Basically, we just need to send 2 positions (where the bullet is coming from) and a main Direction (where the bullet is heading).

 This is where def spawn_bullets_in_circle(self, bullets, pattern) comes into play. This function receives a class object that is a Bullet, and the current pattern that this bullet must have. It then takes in account from the pattern, every info that i spoke about early in the dictionary, and by getting the Bullets count (total amount of bullets around the boss), current repetition (what repetition is shooting now), repetition (how many times will it shoot) and last shot (know if the time from last shot - the current time is greater the delay, so it can shoot next round), it calculates a circle around the boss, that is rotated every 100 milliseconds and "divided" by the amount of count, so for every bullet it updates the current position (X/Y) and direction that is heading, and again, appends to list of Bullets that each bullet has a unique spawning X/Y and unique direction. 

  So the shoot() function keeps track of current pattern and phase by its health, and by indexes, then having a current_patterns var. It creates a bullet with its current_patterns values, and it switches to the next pattern using switch_to_next_pattern(self) (updates indexes values by adding + 1 to it when done with current pattern repetitions). When a certain % of Hp from the boss is reached, it updates the phase key and resets the pattern indexes variables to zero so it can run again to the new patterns in the new phase.

# Projectiles

  This script handles the Bullets and PlayerProjectile classes. This is the object that is appended to a list every time a projectile from the boss or player is spawned, and each of these objects has a spawn position and direction, defined by cords in the X / Y.

  So every time the boss shoots, it appends a Bullet Class, and every time the Player shoots, it appends a playerprojectile class to a list. Both classes are pretty similar, I would say that they are actually the same, and that is one of the considerations that i noticed at the end of the project (More on this later). Both classes get the spawn position and direction, and with this info, it updates a bullet position every time the update is called for the object (this happens in the main loop) and also updates the sprite every time the draw() is called (this happens in the redraw_window() at main), so both are updated every tick of the game, then making the bullets update its collision shape, image and position every tick. They both have a collidepoint() that checks if it's colliding with a Player/Boss object, so it then removes certain % of the object HP.


# Final thoughts

  Overall, I'm happy with how it turned out, it was my first "big project", and I learned a lot about gaming development with it. I think the main takeaway is that I need to learn about OOP, i for sure could have coded some functionalities way better designed using OOP, I really don't like how I coded both classes pretty similar to projectiles, how i DIDNT coded a class for the boss patterns and tried making all functions, and how I didn't make a MAIN entity class for objects with movement / health. It is for sure a lot to learn, and I have a pretty good vision on what I need to improve now, but overall it was really fun developing, and I wanted to make more stuff but as I started cs50 pretty late this year, I just had 2 weeks to code this final project, but I did my best and hope you enjoyed played even if it for a bit!.


  
