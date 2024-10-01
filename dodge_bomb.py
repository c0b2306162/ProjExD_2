import os
import random
import sys
import pygame as pg
import time

accs = [a for a in range(1, 11)]

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bpund(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん、または爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate= True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    elif obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False 
    return yoko, tate

def create_bomb():
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return accs, bb_imgs   



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kkc_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20)) # 空のSurface
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10)
    vx, vy = +5, -5
    
    bb_rct = bb_img.get_rect() # 爆弾rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    accs, bb_imgs = create_bomb()

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        

        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾が重なった場合
            backg = pg.Surface((1100, 650)) # 半透明の黒背景を描画
            backg.set_alpha(128)
            backg.fill((0, 0, 0))
            screen.blit(backg, (0, 0))
            fonto = pg.font.Font(None, 80) #GameOverの文字を描画
            txt = fonto.render("Game Over!", True, (255, 255, 255))
            screen.blit(txt, [400, 200])
            screen.blit(kkc_img,[345, 200]) #泣いているこうかとんを描画
            screen.blit(kkc_img, [745,200])
            pg.display.update() # 画面の更新
            time.sleep(5) #　時間の一時停止
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 横座標, 縦座標
        
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] # 横方向
                sum_mv[1] += tpl[1] # 縦方向

        kk_rct.move_ip(sum_mv)
        
        avx = vx*accs[min(tmr//500, 9)] # 位置の加速度
        avy = vy*accs[min(tmr//500, 9)]

        if check_bpund(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip((avx, avy))
        yoko, tate = check_bpund(bb_rct)
        if not yoko:
            vx *= -1
        elif not tate :
            vy *= -1
        bb_img = bb_imgs[min(tmr//500, 9)] # こうかとんの大きさ拡大
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
