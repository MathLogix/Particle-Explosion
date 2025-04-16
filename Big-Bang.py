import pygame
import random
import sys
# import time

pygame.init()
pygame.display.set_caption("Big Bang")

S_WIDTH, S_HEIGHT = 1000, 700
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()

image = pygame.image.load("Desktop/witcher-logo.png").convert()
WIDTH, HEIGHT = image.get_width(), image.get_height()
offset_x = (S_WIDTH - WIDTH) // 2
offset_y = (S_HEIGHT - HEIGHT) // 2

STEP = 3
particles = []

for y in range(0, HEIGHT, STEP):
    for x in range(0, WIDTH, STEP):
        color = image.get_at((x, y))
        size = random.randint(2, 4)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (size // 2, size // 2), size // 2)

        start_pos = [x + offset_x, y + offset_y]
        dx = random.uniform(-5, 5)
        dy = random.uniform(-2, 2)

        particles.append({
            "image": surf,
            "start_pos": start_pos[:],
            "pos": start_pos[:],
            "vel": [dx, dy],
            "alpha": 255,
            "size": size
        })

STANDBY = 0
EXPLODING = 1
FADING = 2
REGROUPING = 3

state = STANDBY
delay_timer = 60
regroup_timer = 0

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if state == STANDBY:
        screen.blit(image, (offset_x, offset_y))
        delay_timer -= 1
        if delay_timer <= 0:
            state = EXPLODING

    elif state == EXPLODING:
        for p in particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            screen.blit(p["image"], p["pos"])
        delay_timer = 60
        state = FADING

    elif state == FADING:
        all_faded = True
        for p in particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["alpha"] = max(0, p["alpha"] - 2)
            p["image"].set_alpha(p["alpha"])
            if p["alpha"] > 0:
                all_faded = False
                screen.blit(p["image"], p["pos"])
        if all_faded:
            regroup_timer = pygame.time.get_ticks()
            state = REGROUPING

    elif state == REGROUPING:
        elapsed = pygame.time.get_ticks() - regroup_timer
        if elapsed < 1:
            pass
        else:
            all_done = True
            for p in particles:
                dx = p["start_pos"][0] - p["pos"][0]
                dy = p["start_pos"][1] - p["pos"][1]
                dist = (dx**2 + dy**2) ** 0.5

                if dist > 1:
                    p["pos"][0] += dx * 0.1
                    p["pos"][1] += dy * 0.1
                    all_done = False

                p["alpha"] = min(255, p["alpha"] + 5)
                p["image"].set_alpha(p["alpha"])
                screen.blit(p["image"], p["pos"])

            if all_done:
                for p in particles:
                    p["vel"] = [random.uniform(-5, 5), random.uniform(-2, 2)]
                delay_timer = 60
                state = STANDBY

    pygame.display.flip()