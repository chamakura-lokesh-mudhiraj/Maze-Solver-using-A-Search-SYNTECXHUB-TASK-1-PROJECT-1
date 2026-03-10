import pygame
import heapq
import random

pygame.init()

WIDTH = 900
HEIGHT = 700

GRID_SIZE = 25
ROWS = 25
COLS = 25

CELL = 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Maze Solver")

WHITE=(255,255,255)
BLACK=(30,30,30)
BLUE=(0,150,255)
YELLOW=(255,215,0)
GREEN=(0,255,0)
RED=(255,0,0)
GRAY=(200,200,200)

font = pygame.font.SysFont("Arial",20)

start=(0,0)
goal=(ROWS-1,COLS-1)

def generate_maze():

    maze=[[0]*COLS for _ in range(ROWS)]

    for r in range(ROWS):
        for c in range(COLS):

            if random.random()<0.30:
                maze[r][c]=1

    maze[start[0]][start[1]]=0
    maze[goal[0]][goal[1]]=0

    return maze


def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def draw_button(text,x,y,w,h,color):

    pygame.draw.rect(WIN,color,(x,y,w,h))
    label=font.render(text,True,(0,0,0))
    WIN.blit(label,(x+10,y+8))


def draw_maze(maze,visited,path):

    WIN.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):

            rect=pygame.Rect(c*CELL,r*CELL,CELL,CELL)

            if maze[r][c]==1:
                pygame.draw.rect(WIN,WHITE,rect)

            if (r,c) in visited:
                pygame.draw.rect(WIN,BLUE,rect)

            if (r,c) in path:
                pygame.draw.rect(WIN,YELLOW,rect)

            if (r,c)==start:
                pygame.draw.rect(WIN,GREEN,rect)

            if (r,c)==goal:
                pygame.draw.rect(WIN,RED,rect)

    draw_button("START",550,100,120,40,(100,200,100))
    draw_button("CLEAR",550,170,120,40,(220,220,100))
    draw_button("END",550,240,120,40,(200,100,100))

    pygame.display.update()


def astar(maze):

    open_set=[]
    heapq.heappush(open_set,(0,start))

    came={}
    g={start:0}

    visited=[]

    while open_set:

        current=heapq.heappop(open_set)[1]
        visited.append(current)

        if current==goal:

            path=[]

            while current in came:
                path.append(current)
                current=came[current]

            path.append(start)
            path.reverse()

            return path,visited

        for d in [(0,1),(1,0),(0,-1),(-1,0)]:

            nr=current[0]+d[0]
            nc=current[1]+d[1]

            neighbor=(nr,nc)

            if 0<=nr<ROWS and 0<=nc<COLS:

                if maze[nr][nc]==1:
                    continue

                temp_g=g[current]+1

                if neighbor not in g or temp_g<g[neighbor]:

                    came[neighbor]=current
                    g[neighbor]=temp_g

                    f=temp_g+heuristic(neighbor,goal)

                    heapq.heappush(open_set,(f,neighbor))

    return [],visited


maze=generate_maze()
visited=[]
path=[]

running=True

while running:

    draw_maze(maze,visited,path)

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN:

            x,y=pygame.mouse.get_pos()

            if 550<x<670 and 100<y<140:

                path,visited=astar(maze)

            if 550<x<670 and 170<y<210:

                maze=generate_maze()
                visited=[]
                path=[]

            if 550<x<670 and 240<y<280:

                running=False

pygame.quit()