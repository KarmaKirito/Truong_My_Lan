import random
import pygame
import sys

pygame.init()
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
RES = (width, height - 50)
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
FPS = 60
game_bg = pygame.transform.scale(pygame.image.load('Find_treasure/background_official.jpg').convert_alpha(), RES)
ship = pygame.image.load('Find_treasure/ship_1.png').convert_alpha()
blank_wooden_board = pygame.transform.scale(pygame.image.load('Find_treasure/blank_wooden_board_official.png')
                                            .convert_alpha(), (200, 200))
cannon = pygame.transform.scale(pygame.image.load('Find_treasure/Cannon_official.png').convert_alpha(), (400, 400))
island_pic = pygame.image.load('spaceships_bullets_game/spaceship3.png').convert_alpha()
treasure_chest = pygame.transform.scale(pygame.image.load('Find_treasure/collect_treasure_chest.jpg').convert_alpha(), RES)
on_island_img = pygame.transform.scale(pygame.image.load('Find_treasure/go_on_island.jpg'), RES)
explosion_imgs = pygame.image.load('explosion_3_40_128.png').convert_alpha()
explosion_animation_steps = [8, 8, 8, 8, 7]
answer_input = ''
island_images = []
for i in range(0, 11):
    island_image = pygame.transform.scale(pygame.image.load('Find_treasure/Island_zoomed_1.{}.png'.format(i)).
                                          convert_alpha(), (600, 600))
    island_images.append(island_image)


class Button:
    def __init__(self, image, text_input, pos, font, base_color, hovering_color):
        self.image, self.text_input = image, text_input
        self.x_cor = pos[0]
        self.y_cor = pos[1]
        self.font, self.base_color, self.hovering_color = font, base_color, hovering_color
        self.text = self.font.render(self.text_input, True, (255, 255, 255))
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_cor, self.y_cor))
        self.text_rect = self.text.get_rect(center=(self.x_cor, self.y_cor))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Player:
    def __init__(self, sprite_sheet, animation_steps):
        self.explosion_image = None
        self.health = 300
        self.gold = 0
        self.point_multiplier = 1
        self.power1, self.power2, self.power3 = False, False, False
        self.FPS = 60
        self.size = 128
        self.explosion_stage = 0
        self.image_scale = 4
        self.explosion_frame_count = 0
        self.explosion_animation_speed = 3
        self.explosion_frame_index = 0
        self.explosion_animation_list = self.load_images(sprite_sheet, animation_steps)
        self.explosion_image = self.explosion_animation_list[self.explosion_stage][self.explosion_frame_index]

    def super_power(self, current_problem, power_type):
        if power_type == 1:
            self.animate_explosion()
            current_problem.answered_correctly = True
        if power_type == 2:
            self.FPS = self.FPS / 2
            self.power2 = True
        if power_type == 3:
            self.point_multiplier = 2

    def animate_explosion(self):
        self.explosion_frame_count += 1
        if self.explosion_frame_count >= self.explosion_animation_speed:
            self.explosion_frame_index += 1
            self.explosion_frame_count = 0
            if self.explosion_frame_index >= len(self.explosion_animation_list[self.explosion_stage]):
                self.explosion_frame_index = 0
                self.explosion_stage += 1
                if self.explosion_stage >= len(self.explosion_animation_list):
                    self.explosion_stage = 0

        self.explosion_image = self.explosion_animation_list[self.explosion_stage][self.explosion_frame_index]
        screen.blit(self.explosion_image, (RES[0] / 2 - 250, RES[1] / 2 - 400))

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale,
                                                                       self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


def change_update(position, list):
    for buttons in list:
        buttons.changeColor(position)
        buttons.update(screen)


def draw_health_bar(health, x, y):
    ratio = health / 300
    pygame.draw.rect(screen, (255, 255, 255), (x - 5, y - 3, 210, 36))
    pygame.draw.rect(screen, (119, 252, 3), (x, y, 200, 30))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200 * ratio, 30))


def money(gold, x, y):
    gold_text = get_font(25).render('Gold: {}'.format(gold), True, (255, 255, 0))
    screen.blit(gold_text, (x, y))


def find_divisors(num):
    divisors = [1]
    for i in range(1, int(num ** 0.5) + 1):
        if num % i == 0:
            divisors.append(i)
            if i * i != num:
                divisors.append(num // i)
    return random.choice(divisors)


def generate_expression_and_calculate_result_geacr(n_geacr):
    if n_geacr < 1:
        return None, None
    operators_geacr = ['+', '-', '*', '/']
    operators2_geacr = ['+', '-', '*']
    expression_geacr = ''
    i_geacr = 0
    while i_geacr < n_geacr:
        if i_geacr == n_geacr - 1:
            operator_geacr = random.choice(operators2_geacr)
        else:
            operator_geacr = random.choice(operators_geacr)
        if operator_geacr == '/':
            operand2_geacr = random.randint(1, 10)
            operand1_geacr = operand2_geacr * random.randint(1, 10)
            expression_geacr += f'{operand1_geacr} {operator_geacr} {operand2_geacr} '
            operator_geacr = random.choice(operators2_geacr)
            expression_geacr += f'{operator_geacr} '
            i_geacr += 2
        elif operator_geacr == '*':
            operand_geacr = random.randint(1, 10)
            expression_geacr += f'{operand_geacr} {operator_geacr} '
            i_geacr += 1
        else:
            operand_geacr = random.randint(1, 20)
            expression_geacr += f'{operand_geacr} {operator_geacr} '
            i_geacr += 1
    expression_geacr = expression_geacr.strip()
    expression_geacr = expression_geacr[:-1]
    res_geacr = random.randint(0, 5)
    tmp_res_geacr = round(eval(expression_geacr))
    rest_operand_geacr = res_geacr - tmp_res_geacr
    if rest_operand_geacr < 0:
        operator_geacr = '-'
        expression_geacr += f'{operator_geacr} {abs(rest_operand_geacr)}'
    elif rest_operand_geacr > 0:
        operator_geacr = '+'
        expression_geacr += f'{operator_geacr} {rest_operand_geacr}'
    else:
        expression_geacr += "+ 0"
    try:
        result_geacr = round(eval(expression_geacr))
        return expression_geacr, result_geacr
    except ZeroDivisionError:
        return None, None


class Problem:
    def __init__(self, stage, mult_div):
        self.answered = False
        self.stage = stage
        self.questions_count = 0
        self.answered_correctly = False
        self.mult_div = mult_div
        self.font = pygame.font.SysFont('Arial', 50)
        self.text_surface = self.font.render("", True, (0, 0, 0))  # Initialize text surface with empty string

    def display_problem_answer(self, screen, problem, answer):
        # Render problem text
        problem_text = self.font.render(problem, True, (255, 255, 255))

        # Render answer text with an equal sign
        answer_text = self.font.render(f"{problem} = {answer}", True, (0, 0, 0))

        # Get text dimensions for positioning
        problem_text_rect = problem_text.get_rect()
        answer_text_rect = answer_text.get_rect()

        # Calculate positions for centering the text
        problem_x = (screen.get_width() - problem_text_rect.width) // 2
        problem_y = (screen.get_height() // 2) - answer_text_rect.height - 200

        # Blit the texts onto the screen
        screen.blit(problem_text, (problem_x, problem_y))
        screen.blit(answer_text, (problem_x, problem_y + answer_text_rect.height))


def get_font(size):
    return pygame.font.Font('font.ttf', size)


player1 = Player(explosion_imgs, explosion_animation_steps)


def game():
    global answer_input, FPS
    PT1 = Button(blank_wooden_board, text_input='Cannon', pos=(blank_wooden_board.get_rect().width / 2, RES[1] - 110),
                 font=get_font(20), base_color=(52, 64, 235), hovering_color=(255, 255, 255))
    PT2 = Button(blank_wooden_board, text_input='Icicle', pos=(blank_wooden_board.get_rect().width / 2, RES[1] - 310),
                 font=get_font(20), base_color=(52, 64, 235), hovering_color=(255, 255, 255))
    PT3 = Button(blank_wooden_board, text_input='x2 score',
                 pos=(RES[0] - blank_wooden_board.get_rect().width / 2, RES[1] - 310),
                 font=get_font(20), base_color=(52, 64, 235), hovering_color=(255, 255, 255))
    Time_out = Button(None, text_input="Time's up", pos=(RES[0] / 2, 100),
                      font=get_font(30), base_color=(255, 0, 0), hovering_color=(255, 255, 255))
    Go_on_island = Button(None, text_input="Get on island", pos=(RES[0] / 2, 100),
                      font=get_font(30), base_color=(255, 0, 0), hovering_color=(255, 255, 255))
    Finish_challenge = Button(None, text_input="Collect treasure", pos=(RES[0] / 2, 200),
                      font=get_font(30), base_color=(255, 0, 0), hovering_color=(255, 255, 255))
    num_answers_need_to_be_answered = [15, 15, 15, 10]
    num_calculations = 1
    time_for_each_questions = [[10, 5], [9, 4], [8, 4], [7, 4], [7, 3]]
    animating_explosion = False
    animation_timer = 115
    PT1_usable, PT2_usable, PT3_usable = False, False, False
    PTS_use_time = [1, 1, 1]
    win = False
    game_over = False
    on_island = False
    collect_chest = False
    level = 'Easy'
    mode = ["Easy", "Intermediate", "Hard", "Expert"]
    surface_width = 300
    font = get_font(30)
    input_rect_alt = Button(None, '          ', (RES[0] / 2, 300), get_font(30), (0, 0, 0), (255, 255, 255))
    list_button = [input_rect_alt]
    active = False
    lose_text = font.render("You Lost", True, (255, 0, 0))
    win_text = font.render("YOU WON!!", True, (0, 255, 0))
    time_freeze_text = font.render("ICICLE!", True, (102, 222, 126))
    star_of_hope_text = font.render("2X POINTS!!", True, (232, 206, 37))
    already_used_text = font.render("This boost is already used", True, (255, 0, 0))
    list1 = [PT1, PT2, PT3]
    using_PT2 = False
    using_PT3 = False
    usage_time_left_PT3 = 3
    list2 = [Time_out]
    questions_count = 0
    frame_pass1 = 0
    frame_pass2 = 0
    frame_pass_PT2 = 0
    remaining_time_stage = 0
    final_stage = 0
    total_questions_given = 1
    problem1 = Problem(num_calculations, False)
    problem, answer = generate_expression_and_calculate_result_geacr(num_calculations)
    current_island_img = 10
    while True:
        screen.fill((100, 100, 100))
        if PTS_use_time[0] > 0:
            PT1_usable = True
        elif PTS_use_time[0] == 0:
            PT1_usable = False
        if PTS_use_time[1] > 0:
            PT2_usable = True
        elif PTS_use_time[1] == 0:
            PT2_usable = False
        if PTS_use_time[2] > 0:
            PT3_usable = True
        elif PTS_use_time[2] == 0:
            PT3_usable = False
        screen.blit(game_bg, (0, 0))
        screen.blit(island_images[current_island_img], (RES[0] / 2 - 280, RES[1] / 2 - 220))
        screen.blit(ship, (0, 30))
        screen.blit(cannon, (300, 380))
        PT1_use_time = get_font(15).render("Usage: {}".format(PTS_use_time[0]), True, (255, 255, 255))
        PT2_use_time = get_font(15).render("Usage: {}".format(PTS_use_time[1]), True, (255, 255, 255))
        PT3_use_time = get_font(15).render("Usage: {}".format(PTS_use_time[2]), True, (255, 255, 255))
        questions_left_text = get_font(15).render("Questions: {}".format(num_answers_need_to_be_answered[num_calculations - 1] - questions_count),
                                          True, (255, 255, 255))
        game_mouse = pygame.mouse.get_pos()
        if round(frame_pass1 / 60) < time_for_each_questions[remaining_time_stage][final_stage] and not game_over and not win:
            frame_pass1 += 1
        if round(frame_pass1 / 60) == time_for_each_questions[remaining_time_stage] and not game_over and not win:
            change_update(game_mouse, list2)
            active = False
        if not win:
            Time_left_text = font.render(
                "Time: {}".format(time_for_each_questions[remaining_time_stage][final_stage] - round(frame_pass1 / 60)), True,
                (255, 255, 255))
            screen.blit(Time_left_text, (RES[0] / 2 - 70, RES[1] / 2 - 400))
        if using_PT2:
            FPS = 30
            screen.blit(time_freeze_text, (RES[0] / 2 + 200, RES[1] / 2 - 400))
            if frame_pass_PT2 < 600:
                frame_pass_PT2 += 1
            if frame_pass_PT2 == 600:
                FPS = 60
                using_PT2 = False
        if using_PT3:
            screen.blit(star_of_hope_text, (RES[0] / 2 - 400, RES[1] / 2 - 400))
        level_text = get_font(15).render("Next: {}".format(level), True, (255, 255, 255))
        change_update(game_mouse, list1)
        border_surface = pygame.Surface((surface_width + 8, 83), pygame.SRCALPHA)
        input_surface = pygame.Surface((surface_width, 75), pygame.SRCALPHA)
        border_surface.fill((255, 255, 255, 150))
        input_surface.fill((145, 64, 198, 150))
        border_rect = border_surface.get_rect(center=(input_rect_alt.x_cor + 30, input_rect_alt.y_cor))
        input_rect = input_surface.get_rect(center=(input_rect_alt.x_cor + 30, input_rect_alt.y_cor))
        screen.blit(border_surface, border_rect)
        screen.blit(input_surface, input_rect)
        screen.blit(level_text, (RES[0] - 350, 60))
        text_surface = font.render(answer_input, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 15))
        surface_width = max(text_surface.get_width() + 20, 300)
        change_update(game_mouse, list_button)
        draw_health_bar(player1.health, 20, 20)
        problem1.display_problem_answer(screen, problem, answer)
        change_update(game_mouse, list_button)
        screen.blit(PT1_use_time, (blank_wooden_board.get_rect().width / 2 - 50, RES[1] - 90))
        screen.blit(PT2_use_time, (blank_wooden_board.get_rect().width / 2 - 50, RES[1] - 290))
        screen.blit(PT3_use_time, (RES[0] - blank_wooden_board.get_rect().width / 2 - 50, RES[1] - 290))
        screen.blit(questions_left_text, (RES[0] - 350, 30))
        money(player1.gold, RES[0] - 350, 100)
        if not PT1_usable and PT1.checkforInput(game_mouse):
            screen.blit(already_used_text, (RES[0] / 2 - 400, RES[1] / 2))
        if not PT2_usable and PT2.checkforInput(game_mouse):
            screen.blit(already_used_text, (RES[0] / 2 - 400, RES[1] / 2))
        if not PT3_usable and PT3.checkforInput(game_mouse):
            screen.blit(already_used_text, (RES[0] / 2 - 400, RES[1] / 2))
        if animating_explosion:
            player1.animate_explosion()
            if frame_pass2 < animation_timer:
                frame_pass2 += 1
            elif frame_pass2 == animation_timer:
                frame_pass2 = 0
                animating_explosion = False
        pygame.draw.line(screen, (255, 0, 0), (0, RES[1] / 2), (RES[0], RES[1] / 2), 3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PT1.checkforInput(game_mouse) and PT1_usable:
                    animating_explosion = True
                    frame_pass1 = 0
                    questions_count += 1
                    problem, answer = generate_expression_and_calculate_result_geacr(num_calculations)
                    problem1 = Problem(num_calculations, False)
                    PTS_use_time[0] -= 1
                if PT2.checkforInput(game_mouse) and PT2_usable:
                    using_PT2 = True
                    PTS_use_time[1] -= 1
                if PT3.checkforInput(game_mouse) and PT3_usable:
                    using_PT3 = True
                    PTS_use_time[2] -= 1
                if Go_on_island.checkforInput(game_mouse):
                    on_island = True
                if Finish_challenge.checkforInput(game_mouse):
                    collect_chest = True
                if input_rect_alt.checkforInput(game_mouse):
                    active = True
                else:
                    active = False
                if Time_out.checkforInput(game_mouse):
                    frame_pass1 = 0
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    answer_input = answer_input[:-1]
                elif event.key == pygame.K_RETURN and not win and not game_over:
                    total_questions_given += 1
                    if total_questions_given % 2 == 0 and random.randint(0, 1) == 1:
                        PTS_use_time[random.randint(0, 2)] += 1
                    if total_questions_given % 5 == 0 and current_island_img > 0:
                        current_island_img -= 1
                    questions_count += 1
                    frame_pass1 = 0
                    if int(answer_input) == int(answer):
                        if not using_PT3:
                            player1.gold += 100 * num_calculations
                        elif using_PT3:
                            player1.gold += 200 * num_calculations
                            usage_time_left_PT3 -= 1
                        if usage_time_left_PT3 == 0:
                            using_PT3 = False
                    elif int(answer_input) != int(answer):
                        player1.health -= 100
                    problem, answer = generate_expression_and_calculate_result_geacr(num_calculations)
                    problem1 = Problem(num_calculations, False)
                    answer_input = ''
                elif event.key != pygame.K_BACKSPACE:
                    answer_input += event.unicode
        if questions_count == num_answers_need_to_be_answered[0] - 5 and num_calculations == 1:
            final_stage = 1
        if questions_count == num_answers_need_to_be_answered[0] and num_calculations == 1:
            questions_count = 0
            num_calculations += 1
            level = mode[1]
            remaining_time_stage += 1
            final_stage = 0
        if questions_count == num_answers_need_to_be_answered[1] - 5 and num_calculations == 2:
            final_stage = 1
        if questions_count == num_answers_need_to_be_answered[1] and num_calculations == 2:
            questions_count = 0
            level = mode[2]
            num_calculations += 1
            remaining_time_stage += 1
            final_stage = 0
        if questions_count == num_answers_need_to_be_answered[2] - 5 and num_calculations == 3:
            final_stage = 1
        if questions_count == num_answers_need_to_be_answered[2] and num_calculations == 3:
            questions_count = 0
            num_calculations += 1
            level = mode[3]
            remaining_time_stage += 1
            final_stage = 0
        if questions_count == num_answers_need_to_be_answered[3] - 5 and num_calculations == 4:
            final_stage = 1
        if questions_count == num_answers_need_to_be_answered[3] and num_calculations == 4:
            win = True
        if player1.health <= 0:
            game_over = True
        if game_over:
            screen.blit(lose_text, (RES[0] / 2 - 100, RES[1] / 2))
        elif win:
            screen.blit(win_text, (RES[0] / 2 - 100, RES[1] / 2))
            current_island_img = 0
            Go_on_island.changeColor(game_mouse)
            Go_on_island.update(screen)
        if on_island:
            screen.blit(on_island_img, (0, 0))
            if collect_chest:
                screen.blit(treasure_chest, (0, 0))
                money(player1.gold, RES[0]/2-200, RES[1]/2-100)
            Finish_challenge.changeColor(game_mouse)
            Finish_challenge.update(screen)
        clock.tick(FPS)
        pygame.display.flip()
        pygame.display.update()


game()
