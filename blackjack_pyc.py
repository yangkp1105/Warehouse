def import_main():
    from main import Game
    from main import PokerGame

    game = Game('data.json', 'secret.key')
    bj = PokerGame()

def bj_print():#bj是blackjack缩写
    print('=========Welecome to Blackjack==========')
    print('1.游戏规则\n2.小场(底分10-1w)\n3.中场(底分5w-40w)\n4.大场(100w-300w)\n5.至尊场(底分1000w)\n0.退出')
    print('='*10)

def bj_rule():
    print('底分就是你每次游玩投入的最少底注，单场收益上线是底分最高值。')
    print('你讲面对人机庄家，你只能看到他的第一张牌的点数，后面的点数你不知道，但是你知道他有多少张牌')
    print('J,Q,K算10点，A算11点')
    print('你可以叫牌或者停牌（拿一张或者，不再要拍）')
    print('当双方都停牌以后谁最接近21点谁就赢并获得奖池所有筹码')
    print('当你叫牌之后点数总和超过21点，你就爆牌输掉了比赛')

def bj_1():
    if game.get_money() >= 10:
        print('您有资格参与小场')
    else:
        print('不好意思您无法进场')

def bj_2():
    if game.get_money() >= 50000:
        print('您有资格参与中场')
    else:
        print('您无法进场')

def bj_3():
    if game.get_money() >= 1000000:
        print('您有资格参与大场')
    else:
        print('您无法进场')

def bj_2():
    if game.get_money() >= 10000000:
        print('您有资格参与至尊场')
    else:
        print('您无法进场')