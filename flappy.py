from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *
import pygame.mask

# Initialize Global Variables
FPS = 35
SCREENWIDTH = 288
SCREENHEIGHT = 512
PIPEGAPSIZE = 150  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79  # position of the ground
IMAGES, HITMASKS = {}, {}  # image, sound and hitmask  dicts

# list of all wing positions of the bird
PLAYERS_LIST = (
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of all quiz questions
QUIZ_QUESTIONS = [
    {
        'question': 'Who is the current Chairperson of the Federal Reserve?',
        'options': ['Jerome Powell', 'Janet Yellen', 'Ben Bernanke', 'Alan Greenspan'],
        'correct_answer': 'Jerome Powell',
    },
    {
        'question': 'In which year was the Federal Reserve System established?',
        'options': ['1907', '1913', '1920', '1932'],
        'correct_answer': '1913',
    },
    {
        'question': 'What is the primary purpose of the Federal Reserve?',
        'options': ['Stabilize currency', 'Conduct monetary policy', 'Supervise banks', 'All of the above'],
        'correct_answer': 'All of the above',
    },
    {
        'question': 'Which Federal Reserve district is headquartered in New York?',
        'options': ['First District', 'Fifth District', 'Tenth District', 'Second District'],
        'correct_answer': 'Second District',
    },
    {
        'question': 'Which of the following is one of the tools used by the Federal Reserve to implement monetary policy?',
        'options': ['Open market operations', 'Foreign exchange intervention', 'Trade tariffs', 'Corporate tax cuts'],
        'correct_answer': 'Open market operations',
    },
    {
        'question': 'Who appoints the members of the Board of Governors of the Federal Reserve?',
        'options': ['President of the United States', 'Chairperson of the Federal Reserve', 'Secretary of the Treasury', 'Congress'],
        'correct_answer': 'President of the United States',
    },
    {
        'question': 'What is the term length for a member of the Board of Governors of the Federal Reserve?',
        'options': ['4 years', '6 years', '8 years', '10 years'],
        'correct_answer': '6 years',
    },
    {
        'question': 'Which of the following is one of the responsibilities of the Federal Reserve Banks?',
        'options': ['Issuing passports', 'Conducting monetary policy', 'Regulating telecommunications', 'Managing national parks'],
        'correct_answer': 'Conducting monetary policy',
    },
    {
        'question': 'Which of the following is NOT one of the Federal Reserve\'s dual mandates?',
        'options': ['Price stability', 'Maximum employment', 'Financial market regulation', 'Moderate long-term interest rates'],
        'correct_answer': 'Financial market regulation',
    },
    {
        'question': 'What role does the Federal Open Market Committee (FOMC) play in the Federal Reserve System?',
        'options': ['Conducting fiscal policy', 'Supervising banks', 'Making monetary policy decisions', 'Administering social security programs'],
        'correct_answer': 'Making monetary policy decisions',
    },
]

# Main Function
def main():
    global SCREEN, FPSCLOCK # Initialize the Screen and FPSCLOCK (Frames)
    pygame.init()  # Initialize pygame module
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # Sets screen size to specified dimensions
    pygame.display.set_caption('Federal Flappy') # Add Title to the

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    #elcome screen sprite
    IMAGES['message'] = pygame.image.load('assets/sprites/Fedmessage.png').convert_alpha()
    # ground sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    while True:
        #background sprite
        IMAGES['background'] = pygame.image.load('assets/sprites/federalFlappyBackground.png').convert()

        # select player sprites
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[0][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[0][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[0][2]).convert_alpha(),
        )

        # select random pipe sprites
        IMAGES['pipe'] = (
            #Flips to create top pipe
            pygame.transform.flip(pygame.image.load('assets/sprites/pipe-green.png').convert_alpha(), False, True),  
            pygame.image.load('assets/sprites/pipe-green.png').convert_alpha(),
        )

        # hitmask for pipes
        HITMASKS['pipe'] = (
            pygame.mask.from_surface(IMAGES['pipe'][0]),
            pygame.mask.from_surface(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
        pygame.mask.from_surface(IMAGES['player'][0]),
        pygame.mask.from_surface(IMAGES['player'][1]),
        pygame.mask.from_surface(IMAGES['player'][2]),
        )

        IMAGES['numbers'] = (
                pygame.image.load('assets/sprites/0.png').convert_alpha(),
                pygame.image.load('assets/sprites/1.png').convert_alpha(),
                pygame.image.load('assets/sprites/2.png').convert_alpha(),
                pygame.image.load('assets/sprites/3.png').convert_alpha(),
                pygame.image.load('assets/sprites/4.png').convert_alpha(),
                pygame.image.load('assets/sprites/5.png').convert_alpha(),
                pygame.image.load('assets/sprites/6.png').convert_alpha(),
                pygame.image.load('assets/sprites/7.png').convert_alpha(),
                pygame.image.load('assets/sprites/8.png').convert_alpha(),
                pygame.image.load('assets/sprites/9.png').convert_alpha()
            )
        
        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)

# Shows welcome screen animation of flappy bird
def showWelcomeAnimation():
    # Shows welcome screen animation of flappy bird
    # index of player to blit on the screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    # Ground Values
    basex = 0
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():

            # Handles game quit when player exits
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Handles game start when player hits the UP key
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0)) # Draws the background at the origin
        SCREEN.blit(IMAGES['player'][playerIndex],(playerx, playery + playerShmVals['val'])) # Draws the Player's Bird
        SCREEN.blit(IMAGES['message'], (messagex, messagey)) # Draws the Welcome Message
        SCREEN.blit(IMAGES['base'], (basex, BASEY)) # Draws the Ground

        pygame.display.update() # Updates Frames
        FPSCLOCK.tick(FPS)

# Main Game Loop Function
def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']
    passed_tube = False

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    dt = FPSCLOCK.tick(FPS) / 1000
    pipeVelX = -128 * dt

    # player velocity, max velocity, downward acceleration, acceleration on flap
    playerVelY = -9  # player's velocity along Y, default same as playerFlapped
    playerMaxVelY = 10  # max vel along Y, max descend speed
    playerAccY = 1  # players downward acceleration
    playerRot = 45  # player's rotation
    playerVelRot = 3  # angular speed
    playerRotThr = 20  # rotation threshold
    playerFlapAcc = -9  # players speed on flapping
    playerFlapped = False  # True when player flaps
    questionNumberCounter = 0 # Tracks Question Number

    while True:
        for event in pygame.event.get():
            # Handles game quit when player exits
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # Handles player propel when UP Key pressed
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # Conditional ensures player cannot flap wings beyond screen area
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # Check if Player passed a pipe to award points
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                passed_tube = True

        # Pushes the ground forward
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45
        if passed_tube:
            IMAGES['background'] = pygame.image.load(
                'assets/sprites/background-night.png').convert()  # Switch to quiz background
            handleQuizInput(QUIZ_QUESTIONS[questionNumberCounter])
            questionNumberCounter += 1
            if questionNumberCounter > 8:
                questionNumberCounter = 0  # Reset to Question 1 when reach end
            passed_tube = False
            IMAGES['background'] = pygame.image.load(
                'assets/sprites/federalFlappyBackground.png').convert()  # Switch back to the regular background

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to the left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add a new pipe when the first pipe is about to touch the left of the screen
        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove the first pipe if it's out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print the score so the player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


    
def displayQuizScreen(question_data, feedback=None):
    question_font = pygame.font.Font(None, 24)  # Smaller font size
    option_font = pygame.font.Font(None, 24)   # Smaller font size for options
    selected_option = 0  # Index of the selected option

    # Wrap the question text to fit within a maximum width
    max_question_width = 288
    wrapped_question = wrap_text(question_data['question'], question_font, max_question_width)

    # Wrap options to fit within a maximum width
    max_option_width = 288
    wrapped_options = wrap_text_options(question_data['options'], option_font, max_option_width)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_option = (selected_option - 1) % len(question_data['options'])
                elif event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(question_data['options'])
                elif event.key == K_RETURN:
                    # User selected an option
                    return selected_option
                elif event.key == K_SPACE and feedback is not None:
                    # User pressed space to continue after receiving feedback
                    return None

        SCREEN.blit(IMAGES['background'], (0, 0))

        # Display wrapped question
        for i, line in enumerate(wrapped_question):
            line_surface = question_font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(topleft=(SCREENWIDTH / 2 - max_question_width / 2, SCREENHEIGHT * 0.1 + i * 20))
            SCREEN.blit(line_surface, line_rect)

        # Display feedback
        if feedback is not None:
            feedback_font = pygame.font.Font(None, 28)
            feedback_surface = feedback_font.render(feedback, True, (255, 255, 255))
            feedback_rect = feedback_surface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT * 0.8))
            SCREEN.blit(feedback_surface, feedback_rect)

            # Display "Press Space to Continue" message
            continue_font = pygame.font.Font(None, 24)
            continue_surface = continue_font.render("Press Space to Continue", True, (255, 255, 255))
            continue_rect = continue_surface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT * 0.85))
            SCREEN.blit(continue_surface, continue_rect)

        # Display wrapped options with reduced space between words
        for i, line in enumerate(wrapped_options):
            option_color = (255, 255, 255) if i == selected_option else (219, 224, 58)
            option_surface = option_font.render(line, True, option_color)
            option_rect = option_surface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT * 0.4 + i * 40))
            SCREEN.blit(option_surface, option_rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

#Wrap options text to fit within the specified maximum width with reduced space between words.
def wrap_text_options(options, font, max_width):
    wrapped_options = []
    for option in options:
        wrapped_options.extend(wrap_text(option, font, max_width, word_spacing=5))  # Adjust word spacing
    return wrapped_options

#Wrap text to fit within the specified maximum width with adjustable word spacing.
def wrap_text(text, font, max_width, word_spacing=0):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        if font.size(' '.join(current_line + [word]))[0] + word_spacing <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines


def handleQuizInput(question_data):
    correct_option = question_data['correct_answer']
    selected_option = displayQuizScreen(question_data)

    if question_data['options'][selected_option] == correct_option:
        displayQuizScreen(question_data, feedback="Correct!")
        pygame.time.delay(100)  # Display the correct message for 2 seconds
        return  # Correct answer, exit the quiz loop
    else:
        displayQuizScreen(question_data, feedback="Incorrect! Try again.")
        pygame.time.delay(100)  # Display the incorrect message for 2 seconds
        handleQuizInput(question_data)  # Allow the user to try again


def showScore(score):
    #displays score in center of screen
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

#Handles when player crashes the player down and shows the gameover image
def showGameOverScreen(crashInfo):
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_PERIOD or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        
        showScore(score)
        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx, playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
    ]

def checkCrash(player, upperPipes, lowerPipes):
    """returns True if the player collides with the base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if the player crashes into the ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:
        playerRect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], IMAGES['pipe'][0].get_width(), IMAGES['pipe'][0].get_height())
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], IMAGES['pipe'][1].get_width(), IMAGES['pipe'][1].get_height())

            # player and upper/lower pipe masks
            pMask = pygame.mask.from_surface(IMAGES['player'][pi])
            uMask = pygame.mask.from_surface(IMAGES['pipe'][0])
            lMask = pygame.mask.from_surface(IMAGES['pipe'][1])

            # offset between player and pipe rects
            offset_uPipe = (uPipeRect.x - playerRect.x, uPipeRect.y - playerRect.y)
            offset_lPipe = (lPipeRect.x - playerRect.x, lPipeRect.y - playerRect.y)

            # check for collisions
            uCollide = pMask.overlap(uMask, offset_uPipe)
            lCollide = pMask.overlap(lMask, offset_lPipe)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

if __name__ == '__main__':
    main()