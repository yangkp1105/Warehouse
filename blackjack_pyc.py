import keyboard
import random

def import_main():
    from main import Game

    game = Game('data.json', 'secret.key')
    return game

class PokerGame:
    def __init__(self):
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.suits = ['♠', '♥', '♣', '♦']
        self.deck = self.create_deck()
        self.card_counts = {}
        self.drawn_cards = []  # 存储已抽出的牌，每张牌是 (rank, suit) 的元组
    
    def create_deck(self):
        #创建完整的牌组
        deck = []
        for rank in self.ranks:
            for suit in self.suits:
                deck.append((rank, suit))  # 使用元组存储(数字,花色)
        return deck
    
    def init_card_counts(self):
        #初始化每张牌的数量统计
        counts = {}
        for card in self.deck:
            counts[card] = 1
        return counts
    
    def draw_card(self):
        #随机抽取一张牌（不重复）
        available_cards = [card for card in self.deck if card not in self.drawn_cards]
        
        if not available_cards:
            print("牌已经抽完了！")
            return None
        
        drawn_card = random.choice(available_cards)
        self.drawn_cards.append(drawn_card)
        self.card_counts[drawn_card] = 0
        return drawn_card
    
    def get_rank_count(self, rank):
        #获取某个点数（如K）已经被抽走的数量
        count = 0
        for card in self.drawn_cards:
            if card[0] == rank:
                count += 1
        return count
    
    def get_remaining_cards(self):
        #获取剩余牌的数量
        return len(self.deck) - len(self.drawn_cards)
    
    def reset(self):
        #重置游戏
        self.drawn_cards = []
        self.card_counts = self.init_card_counts()

poker = PokerGame()

def bj_print():#bj是blackjack缩写
    print('=========Welecome to Blackjack==========')
    print('1.游戏规则\n2.小场(底分10-1w)\n3.中场(底分5w-40w)\n4.大场(100w-300w)\n5.至尊场(底分1000w)\n0.退出')
    print('='*30)

def bj_rule():
    print('底分就是你每次游玩投入的最少底注，单场收益上线是底分最高值。')
    print('你讲面对人机庄家，你只能看到他的第一张牌的点数，后面的点数你不知道，但是你知道他有多少张牌')
    print('J,Q,K算10点，A算11点')
    print('你可以叫牌或者停牌（拿一张或者，不再要拍）')
    print('当双方都停牌以后谁最接近21点谁就赢并获得double筹码')
    print('当你叫牌之后点数总和超过21点，你就爆牌输掉了')
    print('双击0.返回')
    if keyboard.is_modifier('0'):
        return True

def bj_1():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 10:
        print('您有资格参与小场')
    else:
        print('不好意思您无法进场')

def bj_2():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 50000:
        print('您有资格参与中场')
    else:
        print('您无法进场')

def bj_3():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 1000000:
        print('您有资格参与大场')
    else:
        print('您无法进场')

def bj_4():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 10000000:
        print('您有资格参与至尊场')
    else:
        print('您无法进场')