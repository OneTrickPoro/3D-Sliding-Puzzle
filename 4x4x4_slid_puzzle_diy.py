import pygame, sys, random
a = 3
b = 3
c = 3
nums = [i+1 for i in range(a*b*c)]
nums[-1] = " "
grid= [nums[i:i+b] for i in range(0,len(nums),b)]
grid= [grid[i:i+a] for i in range(0,len(grid),a)]

game_g = grid

nums = [i+1 for i in range(a*b*c)]
nums[-1] = " "
grid= [nums[i:i+b] for i in range(0,len(nums),b)]
grid= [grid[i:i+a] for i in range(0,len(grid),a)]

 
dires = {"u":(0,1,0), "d":(0,-1,0), "r": (1,0,0), "l":(-1,0,0), "t":(0,0,1), "b":(0,0,-1) }

moveu = False
moved = False
mover = False
movel = False
movet = False
moveb = False

done = False
timer = False
time_started = False
movecount = 0



pygame.init()
clock = pygame.time.Clock()
width, height = 900,800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('63puzzle3D')
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 100, 200)
RED = (255,0,0)
YELLOW = (255,255,102)
GREEN = (0,255,0)
SFONDO = (84, 194, 227)

font_timer = pygame.font.SysFont(None, 24)
font = pygame.font.Font(pygame.font.match_font('courier'), 30)
dim_boxx = 90
dim_boxy = 30

def color_num( numco):
    if numco == " ":
        return (255,255,255)
    else:
        numco = int(numco)
    if 0< numco < a*b+1:
        return (84, 194, 227)
    elif a*b< numco < 2*a*b+1:
        return (255,255,102)
    elif 2*a*b< numco < 3*a*b+1:
        return (0,255,0)
    elif 3*a*b< numco < 4*a*b+1:
        return (255,0,0)
    elif 4*a*b< numco < 5*a*b:
        return (0,0,255)
   

def draw_grid_lvl(tab,k, xi, yi):
    for i in range(b):
        for ii in range(a):
            rect_g = pygame.Rect(xi+dim_boxx*(4-ii)//2+ dim_boxx*i , yi+ 10 + dim_boxy * ii, dim_boxx, dim_boxy)
            rect_p = pygame.Rect(rect_g.centerx-dim_boxx//4, rect_g.centery-dim_boxy//4, dim_boxx//4,dim_boxy//4)
            col = color_num(tab[k][ii][i] )
            if col != WHITE:
                text_g = font.render(str(tab[k][ii][i] % (a*b) if tab[k][ii][i] % (a*b) != 0 else (a*b)), True, col )
                screen.blit(text_g, rect_p)
            else:
                pygame.draw.ellipse(screen, WHITE, pygame.Rect(rect_g.centerx - dim_boxx//4, rect_g.centery + dim_boxy//4, dim_boxx//2,dim_boxy//2), 0)
                

def draw_grid(tab):
    for k in range(c):
        draw_grid_lvl(tab, k, 50, 50+180*k)
    
    for i in range(5):
        rect_col = pygame.Rect(700 , 100+i*50 , 50, 50)
        match i:
            case 0:
                col = (84, 194, 227)
            case 1:
                col = (255,255,102)
            case 2:
                col = (0,255,0)
            case 3:
                col = (255,0,0)
            case 4:
                col = (0,0,255)
        pygame.draw.rect(screen, col, rect_col, 0)

def get_hole(tab):
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            for k in range(len(tab[0][0])):
                if tab[i][j][k] == " ":
                    return i,j,k
                
def get_dires(tab):
    ha, hb,hc = get_hole(tab)
    res = []
    if 0 < ha:
        res.append(dires["t"])
    if ha < c-1:
        res.append(dires["b"])
    if 0 < hb:
        res.append(dires["u"])
    if hb < b-1:
        res.append(dires["d"]) 
    if 0 < hc:
        res.append(dires["l"])
    if hc < a-1:
        res.append(dires["r"])
    return res
            
def get_moves(tab, mover, movel, moveu, moved, movet, moveb):
    res = get_dires(tab)
    mover = True if dires["r"] in res else False
    movel = True if dires["l"] in res else False
    moveu = True if dires["u"] in res else False
    moved = True if dires["d"] in res else False
    movet = True if dires["t"] in res else False
    moveb = True if dires["b"] in res else False
    return tab, mover, movel, moveu, moved, movet, moveb

def move_left(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc] =tab[ha][hb][hc-1]
    tab[ha][hb][hc-1] = " "
    return tab 

def move_right(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc] = tab[ha][hb][hc+1]
    tab[ha][hb][hc+1] = " "
    return tab 

def move_upp(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc]= tab[ha][hb-1][hc]
    tab[ha][hb-1][hc] = " "
    return tab 

def move_down(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc] = tab[ha][hb+1][hc]
    tab[ha][hb+1][hc] = " "
    return tab 

def move_top(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc] = tab[ha-1][hb][hc]
    tab[ha-1][hb][hc] = " "
    return tab 

def move_bot(tab):
    ha, hb,hc = get_hole(tab)
    tab[ha][hb][hc]= tab[ha+1][hb][hc]
    tab[ha+1][hb][hc] = " "
    return tab 

def random_move(tab):
    res = get_dires(tab)
    el = random.choice(res)
    mov = [k for k,v in dires.items()  if dires[k]==el][0]
    if mov == "r": return move_right(tab)
    elif mov == "l": return move_left(tab)
    elif mov == "u": return move_upp(tab) 
    elif mov == "d": return move_down(tab)
    elif mov == "t": return move_top(tab)
    elif mov == "b": return move_bot(tab)

def scramble(tab):
    for _ in range(10**3):
        tab = random_move(tab)
    return tab

def check(tab):
    if tab == grid:
        if done== False:
            return True
    else:
        return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if timer == True:
                time_started = True
                start_time = pygame.time.get_ticks()
                timer = False
            if event.key == pygame.K_j and movel == True:
                game_g =  move_left(game_g)
                movecount +=1
            if event.key == pygame.K_l and mover == True:
                game_g =  move_right(game_g)
                movecount +=1
            if event.key == pygame.K_k and  moved == True:
                game_g = move_down(game_g)
                movecount +=1
            if event.key == pygame.K_i and moveu == True:
                game_g =  move_upp(game_g)
                movecount +=1
            if event.key == pygame.K_w and movet == True:
                game_g =  move_top(game_g)
                movecount +=1
            if event.key == pygame.K_s and moveb == True:
                game_g =  move_bot(game_g)
                movecount +=1
            if event.key == pygame.K_SPACE:
                game_g =  scramble(game_g)
                done = False
                timer =  not timer

    status = check(game_g)        
    if status:
        print(movecount)
        done = True
        end_time = pygame.time.get_ticks() 
    draw_grid(game_g)
    game_g, mover, movel, moveu, moved, movet, moveb = get_moves(game_g, mover, movel, moveu, moved, movet, moveb)

    if time_started:
        if done == True:
            counting_time = end_time- start_time
        else:
            counting_time = pygame.time.get_ticks() - start_time

        counting_minutes = str(counting_time//60000).zfill(2)
        counting_seconds = str( (counting_time%60000)//1000 ).zfill(2)
        counting_millisecond = str(counting_time%1000).zfill(3)
        counting_string =counting_minutes +":"+ counting_seconds+"." +counting_millisecond
        counting_text = font.render(str(counting_string), 1, (255,255,255))
        counting_rect = pygame.Rect(650, 500, 100 ,100)
        screen.blit(counting_text, counting_rect)
       
    pygame.display.flip()
    screen.fill(BLACK)
    clock.tick(60)