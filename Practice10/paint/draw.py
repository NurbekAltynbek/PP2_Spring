import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    tool = 'pen'

    points = []
    shapes = []

    drawing = False
    start_pos = (0, 0)
    current_pos = (0, 0)

    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # determine color
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # determine tool
                elif event.key == pygame.K_p:
                    tool = 'pen'
                elif event.key == pygame.K_o:
                    tool = 'circle'
                elif event.key == pygame.K_t:
                    tool = 'rect'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tool == 'pen':
                        drawing = True
                        points.append((event.pos, mode, radius))
                    else:
                        drawing = True
                        start_pos = event.pos
                        current_pos = event.pos

                elif event.button == 3:  # right click shrinks radius
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if tool == 'pen':
                        drawing = False
                    elif tool == 'rect':
                        end_pos = event.pos
                        rect = make_rect(start_pos, end_pos)
                        shapes.append(('rect', get_color(mode), rect, radius))
                        drawing = False
                    elif tool == 'circle':
                        end_pos = event.pos
                        center, rad = make_circle(start_pos, end_pos)
                        shapes.append(('circle', get_color(mode), center, rad, radius))
                        drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    current_pos = event.pos
                    if tool == 'pen':
                        position = event.pos
                        points = points + [(position, mode, radius)]
                        points = points[-256:]

        screen.fill((0, 0, 0))

        # draw saved pen points
        i = 0
        while i < len(points) - 1:
            drawLineBetween(
                screen,
                i,
                points[i][0],
                points[i + 1][0],
                points[i][2],
                points[i][1]
            )
            i += 1

        # draw saved shapes
        for shape in shapes:
            if shape[0] == 'rect':
                _, color, rect, width = shape
                pygame.draw.rect(screen, color, rect, width)
            elif shape[0] == 'circle':
                _, color, center, rad, width = shape
                pygame.draw.circle(screen, color, center, rad, width)

        # preview while drawing shape
        if drawing and tool == 'rect':
            rect = make_rect(start_pos, current_pos)
            pygame.draw.rect(screen, get_color(mode), rect, radius)

        if drawing and tool == 'circle':
            center, rad = make_circle(start_pos, current_pos)
            pygame.draw.circle(screen, get_color(mode), center, rad, radius)

        pygame.display.flip()
        clock.tick(60)


def get_color(color_mode):
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)
    elif color_mode == 'eraser':
        return (0, 0, 0)


def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return pygame.Rect(left, top, width, height)


def make_circle(start, end):
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    rad = int((((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) / 2)
    return center, rad


def drawLineBetween(screen, index, start, end, width, color_mode):
    if color_mode == 'eraser':
        color = (0, 0, 0)
    else:
        c1 = max(0, min(255, 2 * index - 256))
        c2 = max(0, min(255, 2 * index))

        if color_mode == 'blue':
            color = (c1, c1, c2)
        elif color_mode == 'red':
            color = (c2, c1, c1)
        elif color_mode == 'green':
            color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


main()