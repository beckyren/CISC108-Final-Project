import arcade
import Other_sprites_sheet

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BACKGROUND_IMG = "images/game_background.png"
GAME_TITLE = "Meteor Garden"
GAME_SPEED = 1 / 60
character_speed = 4
FACING_RIGHT = 0
FACING_LEFT = 1
VICTORY_TIME = 3600


class Character(arcade.Sprite):
    """Main character class
    code to set texture is from Paul Vincent Craven via
    http://arcade.academy/examples/sprite_face_left_or_right.html """

    def __init__(self):
        """Initialize Character Sprite"""
        super().__init__()
        self.center_x = WINDOW_WIDTH / 2
        self.center_y = WINDOW_HEIGHT / 6
        self.scale = 0.25
        texture = arcade.load_texture("images/main_facing_right.png", mirrored=True, scale=self.scale)
        self.textures.append(texture)
        texture = arcade.load_texture("images/main_facing_right.png", scale=self.scale)
        self.textures.append(texture)
        self.set_texture(FACING_RIGHT)

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates location of main character
        update_animation function is adapted from Paul Vincent Craven via
        http://arcade.academy/examples/sprite_face_left_or_right.html """
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x < 0:
            self.set_texture(FACING_RIGHT)
        if self.change_x > 0:
            self.set_texture(FACING_LEFT)
        if self.right > WINDOW_WIDTH - 1:
            self.right = WINDOW_WIDTH - 1
        if self.left < 0:
            self.left = 0
        if self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1


class Introduction(arcade.View):
    """View that is shown at the start of game"""

    def __init__(self):
        """initialize variables"""
        super().__init__()
        self.background = arcade.load_texture(BACKGROUND_IMG)
        self.character = Character()
        self.dad = Other_sprites_sheet.Dad().dad
        self.dad.center_x = 500
        self.dad.center_y = 120

    def on_draw(self):
        """make sprites and other visuals appear on screen"""
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      WINDOW_WIDTH, WINDOW_HEIGHT, self.background)
        self.character.draw()
        self.dad.draw()
        if self.dad.center_x <= 400:
            arcade.draw_text(
                "Okay honey, your objective for this 60 second test is to\n get rid of meteors before they touch the "
                "garden\n "
                "Just touch the meteors with your wand they touch the garden\n"
                "Remember to get the green potion to leap higher into the air!\n"
                "Dad has faith in you, so good luck!", 210, 210,
                arcade.color.BLACK)
        arcade.draw_text("Click to start", 50, 500, arcade.color.ALABAMA_CRIMSON, font_size=28)

    def on_update(self, delta_time: float):
        """update movement of the dad sprite"""
        if self.dad.center_x > 400:
            self.dad.center_x -= 3

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """takes in mouse input and changes views"""
        main_level = MeteorGarden()
        self.window.show_view(main_level)


class MeteorGarden(arcade.View):
    """Main game view"""

    def __init__(self):
        """ Initialize variables and set up game"""
        super().__init__()
        self.platform_list = None
        self.time = 0
        self.timer = 0
        self.seconds = 0
        self.bottle_timer = 0
        self.background = arcade.load_texture(BACKGROUND_IMG)
        self.character = Character()
        self.platform_list = arcade.SpriteList()
        '''for loop inspired by Paul Vincent Craven's setup from
         http://arcade.academy/examples/sprite_moving_platforms.html#sprite-moving-platforms'''
        for placement in range(10):
            wall = arcade.Sprite("images/main_facing_right.png", 0.1)
            wall.bottom = 0
            wall.center_x = placement * 100
            self.platform_list.append(wall)
        self.physics = arcade.PhysicsEnginePlatformer(self.character,
                                                      self.platform_list,
                                                      gravity_constant=0.15)
        self.meteor_list = arcade.SpriteList()
        self.fallen_list = arcade.SpriteList()
        self.bottle_list = arcade.SpriteList()
        self.collected_list = arcade.SpriteList()

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      WINDOW_WIDTH, WINDOW_HEIGHT, self.background)
        self.character.draw()

        arcade.draw_text("Time is now:" + str(self.seconds), 300, 500, arcade.color.BLACK, 30)
        self.meteor_list.draw()
        self.bottle_list.draw()

    def update_timer(self):
        """self.timer method adapted from Professor Bart
        keeps track of time and when to drop a meteor """
        if (VICTORY_TIME > self.timer > 1) and self.timer % 1000 == 0:
            self.bottle_list.append(Other_sprites_sheet.Bottle())
        if self.timer < VICTORY_TIME and self.timer % 50 == 0:
            self.meteor_list.append(Other_sprites_sheet.Meteor())
            self.timer += 1
        elif self.timer < VICTORY_TIME and self.timer % 50 != 0:
            self.timer += 1

        else:
            self.timer = VICTORY_TIME

    def on_update(self, delta_time):
        """ Called every frame of the game
        Manages changing variables in the main game view
        code to show passing seconds and to change time from
        http://arcade.academy/examples/timer.html?highlight=timer"""
        self.character.update_animation()
        self.physics.update()
        self.time += delta_time
        if self.time > 60:
            self.time = 60
            victory_screen = Victory()
            self.window.show_view(victory_screen)
        self.meteor_list.update()
        self.bottle_list.update()
        self.update_timer()
        self.seconds = int(self.time) % 60
        for meteor in self.meteor_list:
            collision_list1 = arcade.check_for_collision_with_list(self.character, self.meteor_list)
            if len(collision_list1) > 0 and meteor.bottom >= 50:
                meteor.remove_from_sprite_lists()
            elif len(collision_list1) > 0 and meteor.bottom < 50:
                self.fallen_list.append(meteor)
            elif len(collision_list1) == 0 and meteor.bottom < 50:
                self.fallen_list.append(meteor)
        for bottle in self.bottle_list:
            self.collision_list2 = arcade.check_for_collision_with_list(self.character, self.bottle_list)
            if len(self.collision_list2) > 0:
                bottle.remove_from_sprite_lists()
                self.collected_list.append(bottle)

        self.fallen_list.update()

        if len(self.fallen_list) > 0:
            game_over = Gameover()
            self.window.show_view(game_over)

    def on_key_press(self, key, modifiers: int):
        """takes input from keyboard and changes position of character sprite"""
        if key == arcade.key.LEFT:
            self.character.change_x = -character_speed
        elif key == arcade.key.RIGHT:
            self.character.change_x = character_speed
        elif key == arcade.key.UP:
            if self.physics.can_jump():
                self.character.change_y = character_speed
        elif key == arcade.key.SPACE and len(self.collected_list) > 0:
            self.character.center_y = 350
            self.collected_list.pop()

    def on_key_release(self, key, modifiers: int):
        """keeps track of what to do when keys are released on keyboard"""
        if key == arcade.key.UP:
            self.character.change_y = 0

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.character.change_x = 0


class Victory(arcade.View):
    """view shown when player wins game"""

    def __init__(self):
        "initialize variables and set up view"
        super().__init__()
        self.Restart_button = arcade.Sprite("images/Button.png", 0.2)
        self.background = arcade.load_texture(BACKGROUND_IMG)
        self.character = Character()
        self.dad = Other_sprites_sheet.Dad().dad
        self.dad.center_x = WINDOW_WIDTH
        self.dad.center_y = 120
        self.Restart_button.center_y = WINDOW_HEIGHT / 2
        self.Restart_button.center_x = WINDOW_WIDTH / 2
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """make sprites and other visuals appear"""
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      WINDOW_WIDTH, WINDOW_HEIGHT, self.background)
        self.character.draw()
        self.dad.draw()
        if self.dad.center_x == 400:
            arcade.draw_text("Good job, I knew you could do it!", 300, 210,
                             arcade.color.BLACK)
            self.Restart_button.draw()
        arcade.draw_text("SUCCESS", 225, 400, arcade.color.AMETHYST, font_size=40, font_name='calibri')

    def on_update(self, delta_time: float):
        """manage variable states, in this case location of the dad sprite"""
        if self.dad.center_x > 400:
            self.dad.center_x -= 2

    def on_mouse_press(self, x, y, button, _modifiers):
        """take mouse input, changes to the Introduction view"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.Restart_button.points[1][0] > x > self.Restart_button.points[0][0]) and \
                    (self.Restart_button.points[3][1] > y > self.Restart_button.points[1][1]):
                intro = Introduction()
                self.window.show_view(intro)


class Gameover(arcade.View):
    """view shown when player loses game"""
    def __init__(self):
        """initialize and set up view"""
        super().__init__()
        self.Restart_button = arcade.Sprite("images/Button.png", 0.2)
        self.Restart_button.center_y = WINDOW_HEIGHT / 2
        self.Restart_button.center_x = WINDOW_WIDTH / 2
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """make sprites and other visuals appear on screen"""
        arcade.start_render()
        arcade.draw_text("GAME OVER", 250, 400, arcade.color.WHEAT, font_size=20)
        arcade.draw_text("Oops, you let a meteor slip by", 165, 375, arcade.color.WHEAT, font_size=20)
        self.Restart_button.draw()

    def on_mouse_press(self, x, y, button, _modifiers):
        "take in mouse input and change to the Introduction view"
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.Restart_button.points[1][0] > x > self.Restart_button.points[0][0]) and \
                    (self.Restart_button.points[3][1] > y > self.Restart_button.points[1][1]):
                intro = Introduction()
                self.window.show_view(intro)


def main():
    """main function"""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Meteor Game")
    intro = Introduction()
    window.show_view(intro)
    arcade.run()


if __name__ == "__main__":
    main()
