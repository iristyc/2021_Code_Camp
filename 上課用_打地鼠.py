"""
引入我們會需要用到的程式庫
"""
import pygame
import time
from random import randint

"""
決定視窗大小及我們會常常用到的顏色
這樣的好處是以後我們如果要改主題顏色或視窗大小，只要對應去改這邊的資料就好
"""
# 螢幕尺寸
SCREEN_WIDTH = 400 # 寬
SCREEN_HEIGHT = 400 # 長

# 顏色
GREEN = (73, 188, 11)#用tuple去存RGB的顏色
YELLOW = (225, 225, 0)
WHITE = (255, 255, 255)

"""
觀察我們會需要知道的資訊
首先是老鼠會出現在某個 (x,y) 座標上（一次一隻）
所以我們透過 x, y 變數來記住目前老鼠在哪裡方便判斷
接著是我們預計設計出來的遊戲裡面會需要什麼資訊？
分數及遊戲時間，那我們額外加個開始時間，方便計算過了幾秒鐘
最後還有一個東西，我們希望知道什麼時候滑鼠有按下
這樣槌子才能對應改變成敲下去的樣子
"""
# 老鼠位置及遊戲資訊
x = None  # 老鼠出現在(x,y)座標
y = None
score = 0 # 目前得分
game_time = 20 # 遊戲時間限制
start_time = 0 # 目前的時間
mallet_down = False # 判斷滑鼠有沒有按下去，true是按下去，false是還沒按下去

"""
我們玩遊戲的時候會有幾個狀態，像是一開始的首頁、遊戲中的畫面和最後結束的畫面
因此我們設計一個變數來儲存目前的狀態，好讓我們對應去顯示畫面及處理動作
像是我們不會希望還沒開始的時候，時間就開始倒數或是老鼠就在亂跑
"""
# game state: 0 - welcome, 1 - playing, 2 - game over
state = 0#畫面的狀態

"""
接著可以設定初始化的遊戲視窗，順便載入會使用到的圖片
由於只會執行一次，不用函式包起來比較好對這些變數操作
"""
# 建立視窗及載入圖片
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 建立長寬為400,400的視窗
clock = pygame.time.Clock() # 創建一個對象來幫助跟蹤時間 
mole = pygame.image.load('mole.png') # 載入 地鼠的圖片 ((等等要拿來打的
mallet = pygame.image.load('mallet.png') # 載入槌子 還沒槌 下去的圖片((mallet_down = False出現
down_mallet = pygame.image.load('down-mallet.png') # 載入槌子 槌下去 的圖片((mallet_down = True出現
background = pygame.image.load('grass.png') # 載入遊戲畫面的背景
pygame.mouse.set_visible(False) # 在遊戲視窗中 滑鼠看不到 
pygame.display.set_caption('click a mole') # 使窗左上角的名稱(應用程式、遊戲的名稱)
pygame.font.init() # 該函數用於「初始化」字體模塊，如果沒有這行 程式就不會初始化 甚麼都不會出現!!

"""
對應不同的畫面，我們分別把他定義成函式
分別為 welcome_screen 歡迎頁面、 play_screen 遊戲頁面 及 end_screen 結束頁面
然後我們對應看裡面需要做什麼事情
"""
def welcome_screen():#歡迎的畫面
    # 背景填滿綠色
    screen.fill(GREEN)
    # 設定字體樣板 pygame.font.SysFont("字體名稱", 字體大小)
    font = pygame.font.Font(None, 30)
    # 設定歡迎畫面會出現的文字 (文字, 是否開啟鋸齒(如果要修邊，就打true，但效能會變慢), 顏色, 背景(可不加=透明))
    text = font.render("press ENTER to start", False, WHITE)
    # 將文字、老鼠及槌子顯示在畫面上
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 185)) # 文字位置
    screen.blit(mallet, (200, 50)) # 槌子位置 #x座標&y座標(最左上角是(0,0)、最右上角是(400,0))
    screen.blit(mole, (120, 250)) # 地鼠位置

def play_screen():#玩遊戲的畫面
    # 將草地顯示在背景上
    screen.blit(background, (0,0))
    """
    接著去思考有哪些東西需要改變或動作，我們先預想會有哪些函式並寫在這裡
    之後我們再去實作他
    """
    # 顯示分數
    show_score()
    # 顯示時間
    show_timer()
    # 顯示老鼠
    show_mole()
    # 顯示槌子
    show_mallet()

def end_screen():#結束的畫面
    # 背景填滿綠色
    screen.fill(GREEN)
    # 設定字體樣板分別顯示遊戲結束、分數及重新開始按鈕
    font = pygame.font.Font(None, 30) # 字體物件先建立出來
    game_over = font.render("GAME OVER", False, WHITE) # (文字, 是否鋸齒, 顏色, 背景)
    font = pygame.font.Font(None, 25) 
    points = font.render("score: " + str(score), False, WHITE)
    font = pygame.font.Font(None, 22)
    restart = font.render("press ENTER to play again", False, WHITE)
    # 將上述資訊字樣 顯示到螢幕上
    screen.blit(game_over, (SCREEN_WIDTH / 2 - game_over.get_width() / 2, 100))
    screen.blit(points, (SCREEN_WIDTH / 2 - points.get_width() / 2, 200))
    screen.blit(restart, (SCREEN_WIDTH / 2 - restart.get_width() / 2, 300))

"""
接著來實作遊玩的函式，這部分有點多我們可以先從簡單的開始
play 及 end 函式用來處理開始玩及玩完的遊戲狀態

Global:
將外部的變數視為全域變數引入函式之中
這樣對他修改後就不會隨著函式消失就恢復原狀
"""
def play():
    # 取用遊戲狀態、分數及開始時間資訊
    global state, score, start_time # 預設為 0, 0, 0 
    # 設定遊戲開始時間 time.time() 會取得目前的時間
    start_time = time.time() # import的套件，裡面的時間方法time()
    # 將分數歸 0 且狀態設定為 1 遊玩中
    score = 0
    state = 1 # 把畫面設定為page=playing
    # 產生新的老鼠（這邊先立一個函式之後完成）
    new_mole()
    # 產生瞬間先檢查是否有被打到（這邊先立一個函式之後完成）
    whack()#打擊

def end():
    # 狀態改為 2 結束遊戲
    global state
    state = 2 # page=game_over

"""
接著處理剛剛提到的產生新老鼠 new_mole 以及槌子 whack 打老鼠的偵測
"""

def new_mole():
    # 隨機 決定下一個老鼠產生的位置
    global x, y
    # 老鼠能出線的範圍: x 從螢幕最左到右邊扣掉老鼠的寬都能取, y 則向下移 30 到底部扣掉老鼠的高都能取
    x = randint(0, SCREEN_WIDTH - mole.get_width())#後面的相減是為了不要讓老鼠的圖片超出視窗，而預留空間
    y = randint(30, SCREEN_HEIGHT - mole.get_height())

def whack():
    global score
    # 取得滑鼠當前的位置
    mx, my = pygame.mouse.get_pos() # pos是position意思
    # 取得老鼠的寬及高
    width, height = mole.get_size()
    # 將座標計算是不是點擊在老鼠的圖片上, 如果有的話要"加分"和"產生新的老鼠"
    # mx-x 是滑鼠與老鼠圓心的距離 要小於等於<= 老鼠1/2寬度width/2
    if abs(mx - x - width / 2) <= width / 2 and abs(my - y - height / 2) <= height / 2:
        score += 1 #分數+1 #mx是滑鼠的x座標 #(滑鼠的座標)-(老鼠的核心位置)-(老鼠圖片的寬度/2)
        new_mole() #產生新老鼠

"""
接著在顯示 (blit) 圖片之前要來檢查滑鼠是不是有按下去
如果有按下去的話要改變 mallet_down 的狀態來判斷顯示成槌子槌下去的圖片
"""

def check_mallet_state():
    global mallet_down
    # 檢查滑鼠左鍵有沒有被按，[左鍵、中鍵、右鍵]，如果被按下則為 True，[0]為抓到左鍵是否為True表示被按下去。
    if pygame.mouse.get_pressed()[0]:
        mallet_down = True # 改變狀態: 鎚子槌下去
    else:
        mallet_down = False # 改變狀態: 槌子恢復原本樣貌

"""
最後一部分是要來顯示老鼠、槌子、分數及時間
"""

def show_mole():
    # 把隨機出來的位置放老鼠上去
    screen.blit(mole, (x, y))


def show_mallet():
    # 檢查槌子狀態
    check_mallet_state()
    # 取得槌子圖片各種位置資料
    mallet_position = mallet.get_rect()
    # 將槌子的中心點設在滑鼠點的位置
    mallet_position.center = pygame.mouse.get_pos()
    # 依照狀態不同將槌子顯示
    if mallet_down:
        # 如果mallet_down滑鼠是點下的狀態True-塞槌子槌下去的圖片
        screen.blit(down_mallet, mallet_position)
    else:
        # 如果mallet_down滑鼠是點下的狀態False-塞槌子原始的圖片
        screen.blit(mallet, mallet_position) 

def show_score():
    # 設定字型模板
    font = pygame.font.Font(None, 28)
    # 用模板來建立分數文字
    text = font.render(str(score), False, WHITE)
    # 將文字顯示上去
    screen.blit(text, (10, 0))

def show_timer():
    # 現在的時間 - 開始時間(start_time) = 經過的秒數(elapsed)
    elapsed = time.time() - start_time
    # 遊戲總時間 - 經過的秒數(elapsed) = 要顯示的剩餘秒數
    timer = game_time - elapsed
    # 如果秒數歸零則遊戲結束
    if timer < 0:
        end() # 顯示end畫面
    # 建立字型模板、建立時間文字及顯示到 end 畫面上
    font = pygame.font.Font(None, 28)
    text = font.render(str(int(timer)), False, WHITE)
    screen.blit(text, (370, 0))

"""
接下來要寫事件處理的部分
每個遊戲狀態都有要處理的事件
像是遊戲一開始按下 Enter 的時候要開始玩 -> Play()
遊戲中的話按下滑鼠要去打地鼠
遊戲結束的話一樣按下 Enter 要重新開始遊戲 -> Play()
"""

# 處理首頁
def handle_welcome(e):
    # 顯示歡迎畫面
    welcome_screen()
    # 偵測鍵盤 Enter 事件: 按下去 && 是Enter按鍵
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        play() # 進入遊戲畫面 Playing Page

def handle_play(e):
    # 偵測滑鼠按下事件
    if e.type == pygame.MOUSEBUTTONDOWN:
        whack() # 判斷是否有打中


def handle_end(e):
    # 偵測鍵盤 Enter 事件
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        play() # 再來玩一場 進入遊戲畫面 playing page



# 遊戲主要運行的流程
def main():
    # 設定運行狀態
    running = True
    while running:
        # 使用了pygame.event.get()來處理所有的事件
        for event in pygame.event.get():
            # 當按下視窗的 X 結束遊戲運行
            if event.type == pygame.QUIT:
                running = False # 跳出while迴圈
            # 首頁
            elif state == 0: # page: Welcome頁面
                handle_welcome(event) # 是否enter觸發=> 進入遊戲
            # 遊玩中
            elif state == 1: # page: Playing頁面
                handle_play(event) # 是否按下去滑鼠 => 判斷是否有打中
            # 遊戲結束
            elif state == 2: # page: end頁面
                handle_end(event) # 是否enter觸發 => 繼續遊戲

        # 遊玩中繪製遊戲畫面
        if state == 1:
            play_screen()
        # 結束時繪製結束畫面
        if state == 2:
            end_screen()

        # 設定每秒至少 update 30 次 (對這個 while loop) 表示每秒最多應通過30幀
        clock.tick(30)

        # 更新畫面
        pygame.display.update()

    # 當視窗關閉時 (running = false), 關閉視窗
    pygame.quit()

# 執行遊戲主要運行流程
main()