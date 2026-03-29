import json
import time
import os
import keyboard
import math
import random
import hashlib
from cryptography.fernet import Fernet
import sys
import importlib.util
import requests
from datetime import datetime, timedelta

File = int(0)

try:
    pyc_path_bj = r'__pycache__\blackjack.pyc'  # 使用完整路径
except FileNotFoundError:
    No_File = int(1)
    File = int(1)
try:
    pyc_path_gold = r'__pycache__\gold_money.cpython-313.pyc'
except FileNotFoundError:
    No_File = int(2)
    File = int(1)
try:
    pyc_path_international_currency = r'__pycache__\international_currency.cpython-313.pyc'
except FileNotFoundError:
    No_File = int(3)
    File = int(1)

# 加载模块
try:
    spec_1 = importlib.util.spec_from_file_location('blackjack', pyc_path_bj)
    blackjack = importlib.util.module_from_spec(spec_1)
    spec_1.loader.exec_module(blackjack)

    spec_2 = importlib.util.spec_from_file_location('blackjack', pyc_path_gold)
    gold = importlib.util.module_from_spec(spec_2)
    spec_2.loader.exec_module(gold)

    spec_3 = importlib.util.spec_from_file_location('blackjack', pyc_path_international_currency)
    international_currency = importlib.util.module_from_spec(spec_3)
    spec_3.loader.exec_module(international_currency)
except FileNotFoundError:
    File = int(1)
    No_File = int(114514)

if File == 1:
    if No_File == 1:
        print(f"找不到{pyc_path_bj}文件，请重新解压文件，或者获取游戏文件")
        time.sleep(3)
        exit()
    elif No_File == 2:
        print(f"找不到{pyc_path_gold}文件，请重新解压文件，或者获取游戏文件")
        time.sleep(3)
        exit()
    elif No_File == 3:
        print(f"找不到{pyc_path_international_currency}文件，请重新解压文件，或者获取游戏文件")
        time.sleep(3)
        exit()
    else:
        print('缺失pyc文件，请检查')

levels_num_book={'1': 500,#字典数字等级对应{'x+1'级}方便写代码
                 '2': 2000,
                 '3': 8000,
                 '4': 15000,
                 '7': 25000,
                 '8': 45000,
                 '9': 80000,
                 '10': 150000,
                 '11': 200000,
                 '12': 300000,
                 '13': 500000,
                 '14': 1000000,}

levels_price_book={'1': 500,#字典数字等级对应{'x+1'级}方便写代码
                 '2': 1000,
                 '3': 2000,
                 '4': 2500,
                 '7': 3000,
                 '8': 5000,
                 '9': 6000,
                 '10': 10000,
                 '11': 12000,
                 '12': 12500,
                 '13': 143000,
                 '14': 150000,}

level_return_money_book={'1': 0.5,#字典数字等级对应{'x+1'级}方便写代码
                 '2': 0.45,
                 '3': 0.4,
                 '4': 0.35,
                 '7': 0.3,
                 '8': 0.25,
                 '9': 0.2,
                 '10': 0.15,
                 '11': 0.1,
                 '12': 0.05,
                 '13': 0.05,
                 '14': 0.05,
                 '15': 0,
                 }

game_mode_3_num = ['1','2','3','4','5','6']#俄罗斯*轮盘的中击空位列表
game_mode_3_price_1 = {
    '1': 500000,
    '2': 800000,
    '3': 1200000,
    '4': 2000000,
    '5': 3000000,
}
game_mode_3_price_2 = {
    '1': 800000,
    '2': 1500000,
    '3': 3000000,
    '4': 3500000,
}
game_mode_3_price_3 = {
    '1': 1500000,
    '2': 3000000,
    '3': 4000000,
}
game_mode_3_price_4 = {
    '1': 3000000,
    '2': 4500000,
}
game_mode_3_price_5 = {
    '1': 5500000,
}

ai_card = []
user_card = []

class Game:
    def __init__(self, js_file='data.json', key_file='secret.key'):
        self.js_file = js_file
        self.key_file = key_file
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)
        self.data = self.load_data()  # 保持 data 属性不变
    
    def load_or_create_key(self):#加载或创建加密密钥
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def hash_password(self, password):#密码哈希
        salt = "game_salt_2024"
        combined = password + salt
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def verify_password(self, input_password):#验证密码
        hashed_input = self.hash_password(input_password)
        return hashed_input == self.data['password']
    
    def encrypt_money(self, money):#加密金钱
        money_str = str(money)
        encrypted = self.cipher.encrypt(money_str.encode())
        return encrypted.decode()
    
    def encrypt_gold(self, gold):#加密黄金
        gold_str = str(gold)
        encrypted = self.cipher.encrypt(gold_str.encode())
        # 将 bytes 转换为 base64 字符串
        import base64
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_money(self, encrypted_money):#解密金钱
        try:
            decrypted = self.cipher.decrypt(encrypted_money.encode())
            return int(decrypted.decode())
        except:
            return 0

    def decrypt_gold(self, encrypted_gold):#解密黄金
        try:
            decrypted = self.cipher.decrypt(encrypted_gold.encode())
            return int(decrypted.decode())
        except:
            return 0
    
    def set_money(self, new_money):#设置加密后的金钱
        if isinstance(new_money, int):
            self.data['money'] = self.encrypt_money(new_money)
        else:
            # 如果已经是加密字符串，直接保存
            self.data['money'] = new_money
        self.save_data()
    
    def get_money(self):#获取解密后的金钱
        money_value = self.data['money']
        
        # 如果是整数，说明是未加密的，直接返回
        if isinstance(money_value, int):
            return money_value
        
        # 如果是字符串，解密返回
        if isinstance(money_value, str):
            try:
                return self.decrypt_money(money_value)
            except:
                # 解密失败返回默认值
                return 1000
        
        # 其他情况返回默认值
        return 1000
    
    def set_gold(self, new_gold):#设置加密后的黄金
        if isinstance(new_gold, int):
            self.data['gold'] = self.encrypt_money(new_gold)
        else:
            # 如果已经是加密字符串，直接保存
            self.data['gold'] = new_gold
        self.save_data()
    
    def get_gold(self):#获取解密后的金钱
        gold_value = self.data['gold']
        
        # 如果是整数，说明是未加密的，直接返回
        if isinstance(gold_value, int):
            return gold_value
        
        # 如果是字符串，解密返回
        if isinstance(gold_value, str):
            try:
                return self.decrypt_money(gold_value)
            except:
                # 解密失败返回默认值
                return 0

    def _encrypt_value(self, value: int) -> str:#货币
        """将整数加密为字符串（统一使用 Fernet）"""
        return self.cipher.encrypt(str(value).encode()).decode()

    def _decrypt_value(self, encrypted: str) -> int:#货币
        """将加密字符串解密为整数"""
        try:
            return int(self.cipher.decrypt(encrypted.encode()).decode())
        except:
            return 0

    def get_currency(self, name: str) -> int:#货币
        """获取指定货币的余额（解密后）"""
        value = self.data.get(name, 0)
        if isinstance(value, int):
            # 旧数据迁移：自动加密并保存
            encrypted = self._encrypt_value(value)
            self.data[name] = encrypted
            self.save_data()
            return value
        return self._decrypt_value(value)

    def set_currency(self, name: str, amount: int):#货币
        """设置指定货币的余额（加密保存）"""
        self.data[name] = self._encrypt_value(amount)
        self.save_data()

    def add_currency(self, name: str, amount: int) -> int:#货币
        """增加指定货币的余额，返回新余额"""
        current = self.get_currency(name)
        new_value = current + amount
        self.set_currency(name, new_value)
        return new_value

    def subtract_currency(self, name: str, amount: int) -> bool:#货币
        """减少指定货币的余额，成功返回 True，余额不足返回 False"""
        current = self.get_currency(name)
        if current >= amount:
            new_value = current - amount
            self.set_currency(name, new_value)
            return True
        return False

    def _encrypt_value(self, value: int) -> str:#货币
        """将整数加密为字符串（返回 Base64 字符串）"""
        encrypted = self.cipher.encrypt(str(value).encode())
        return encrypted.decode()  # 直接返回字符串，与 encrypt_money 保持一致

    def _decrypt_value(self, encrypted: str) -> int:#货币
        """将加密字符串解密为整数，失败返回 0"""
        try:
            decrypted = self.cipher.decrypt(encrypted.encode())
            return int(decrypted.decode())
        except Exception:
            return 0

    def load_data(self):#加载数据
        initial_data = {
            'money': self.encrypt_money(1000),  # 加密存储
            'GBP':self._encrypt_value(0),
            'EGP':self._encrypt_value(0),
            'HKP':self._encrypt_value(0),
            'JPY':self._encrypt_value(0),
            'gold': self.encrypt_gold(0),
            'levels': 1,
            'levels_num': 0,
            'month': 0,
            'month_turn': 0,
            'password': self.hash_password('admin123'),
            'invincible_mode': 0,
            'bank_have_borronw': 0,
            'individual_have_borronw': 0,
            'xx_have_borronw': 0,
        }
        try:
            if not os.path.exists(self.js_file):
                # 文件不存在，创建新文件
                with open(self.js_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=4, ensure_ascii=False)
                return initial_data.copy()  # 返回字典
            else:
                # 文件存在，读取文件
                with open(self.js_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 确保 data 是字典
                if not isinstance(data, dict):
                    print("警告：数据格式错误，使用初始数据")
                    return initial_data.copy()
                
                # 数据迁移逻辑
                if 'money' in data and isinstance(data['money'], int):
                    print("检测到旧数据格式，正在转换金钱加密格式...")
                    data['money'] = self.encrypt_money(data['money'])
                
                # 确保 gold 字段存在
                if 'gold' not in data:
                    print("添加缺失的 gold 字段...")
                    data['gold'] = self.encrypt_gold(0)
                
                return data  # 返回字典
        except Exception as e:
            print(f"加载数据时出错: {e}")
            print("使用初始数据继续运行")
            return initial_data.copy()  # 出错时返回初始数据
    
    def save_data(self):#保存数据
        with open(self.js_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_value(self, key):#获取值（特殊处理money）
        if key == 'money':
            return self.get_money()
        return self.data.get(key)
    
    def add_money(self, amount):
        #增加金钱
        current = self.get_money()  # 这会返回整数
        new_money = current + amount
        self.data['money'] = self.encrypt_money(new_money)  # 直接加密保存
        self.save_data()
        return new_money
    
    def subtract_money(self, amount):#减少金钱
        current = self.get_money()
        if current >= amount:
            new_money = current - amount
            self.set_money(new_money)
            self.save_data()
            return True
        else:
            return False
    
    def level_up(self):#升级
        levels_now = str(self.data['levels'])
        if self.data['levels'] <= 15 and self.data['levels_num'] >= levels_num_book.get(levels_now, 0):
            # 增加等级奖励
            reward = levels_price_book.get(str(self.data['levels']), 0)
            current = self.get_money()
            self.set_money(current + reward)
            
            # 其他属性更新
            self.data['levels'] += 1
            self.data['levels_num'] = math.floor(self.data['levels_num'] // 2)
            self.save_data()
            return True
        else:
            return False
    
    def change_password(self, old_password, new_password):
        if self.verify_password(old_password):
            self.data['password'] = self.hash_password(new_password)
            self.save_data()
            return True
        return False
    
    def month_turn_up(self):
        if self.data['month_turn'] == 2:
            self.data['month'] += 1
            self.data['month_turn'] = 0
            self.save_data()
    
    def wait_for_any_key(self):
        keyboard.read_key()
        time.sleep(0.2)

#class Encryption:######################################################
    #def encrypt_money(self, currency)

class PokerGame:
    def __init__(self):
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.suits = ['♠', '♥', '♣', '♦']
        self.deck = self.create_deck()
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
        return drawn_card
    
    def get_rank_count(self, rank):
        #获取某个点数（如K）已经被抽走的数量
        count = 0
        for card in self.drawn_cards:
            if card.startswith(rank):
                count += 1
        return count
    
    def get_remaining_cards(self):
        #获取剩余牌的数量
        return len(self.deck) - len(self.drawn_cards)
    
    def reset(self):
        #重置游戏
        self.drawn_cards = []
        self.card_counts = self.init_card_counts()

class Transaction:
    def sell_print():
        print('1.出售')
        print('2.购买')

    def buy():
        print('请输入购入目标货币数量')
        game = Game('data.json', 'secret.key')


poker = PokerGame()
transaction = Transaction()
game = Game('data.json', 'secret.key')

print(
    '广州市第二中学2023届230516开发')
print(
     '尊重版权，禁止盗版，本游戏仅供学习交流使用，禁止用于商业用途，违者必究！')
print(
      'Money Games是一款虚拟游戏，游戏中的货币和等级仅供娱乐使用，不具有任何实际价值。')
print(
      '请勿将游戏中的货币用于现实生活中的交易或赌博活动。玩家应当理性对待游戏，避免沉迷，并遵守相关法律法规。')

def main_print():
    print()
    print('=======游戏大厅=======')
    print('账号余额:',game.get_money(),'$')
    print('游戏等级:',game.data['levels'])
    print('经验:',game.data['levels_num'])
    print('当前月份:',game.data['month'])
    print('距离下一级还差:',levels_num_book[str(game.data['levels'])]-game.data['levels_num'],'经验')
    print('下一级奖励:',levels_price_book[str(game.data['levels'])],'$')
    print('=====================')
    print('游戏仅为虚拟，请勿赌博，远离毒品，人人有责')
    print('请勿沉迷游戏，合理安排时间，拒绝盗版游戏')
    print('注意自我保护，谨防受骗上当，适度游戏益脑')
    print('沉迷游戏伤身，合理安排时间，享受健康生活')
    print('======游戏选择======')
    print('1.交易所')
    print('2.德*扑克(还未完成千万别碰，碰了电脑卡死)')
    print('3.俄罗斯*轮盘')
    print('4.二十一点')
    print('======玩家选项======')
    print('9.仓库')
    print('\help.指令说明')
    print('======其他功能======')
    print('5.借money')
    print('6.管理员模式')
    print('7.退出游戏')
    print('8.关于游戏')
    print('#####################')
    game_mode = 'main'

def admin_print():
    print()
    print('=======管理员模式=======')
    print('作者：杨凯鹏')
    print('1.修改管理员密码')
    print('2.修改玩家数据')
    print('3.重置玩家数据')
    print('4.无敌模式(不死不扣钱)')
    print('5.退出管理员模式')
    print('=====================')

def invincible():
    invincible_mode = game.data['invincible_mode']
    if invincible_mode == 0:
        invincible_mode = 1
        print('无敌模式已开启')
    else:
        invincible_mode = 0
        print('无敌模式已关闭')

def game_mode_3():
    print()
    print('=======俄罗斯*轮盘=======')
    print('1.开始游戏(100w$入场费)')
    print('2.退出游戏')
    print('3.游戏说明')
    print('=====================')

def get_price_dict(choice):#根据玩家选择的子弹数量返回对应的奖励字典(game_mode_3_)
    if choice == '1':
        return game_mode_3_price_1
    elif choice == '2':
        return game_mode_3_price_2
    elif choice == '3':
        return game_mode_3_price_3
    elif choice == '4':
        return game_mode_3_price_4
    elif choice == '5':
        return game_mode_3_price_5
    else:
        return None

def game_mode_3_start():
    game.add_money(-1000000)
    how_many_continue = int(input('请选择子弹数量(1-5): '))
    user_price_dict = get_price_dict(str(how_many_continue))
    boom_num = random.sample(game_mode_3_num, how_many_continue)
    available_numbers = game_mode_3_num.copy()
    turns = 0
    while available_numbers:
    # 随机选择一个数字
        chosen = random.choice(available_numbers)
        available_numbers.remove(chosen)
        turns += 1
    
    # 检查是否在雷中
        if chosen in boom_num:
            if game.data['invincible_mode'] == 1:
                print('你中枪了，但无敌模式已开启，你没有失去游戏账号数据！')
                for i in range(20):
                    print('不要赌博，赌博害人也害己')
                continue
            else:
                print(f"你中枪了，你失去游戏账号数据！")
                print("3秒后程序退出")
                game.data['money'] = 0
                game.data['levels'] = 1
                game.data['levels_num'] = 0
                game.data['month'] = 0
                game.data['month_turn'] = 0
                game.save_data()
                time.sleep(3)
                exit()
        else:
            turn_key = str(turns)
            print('你很幸运！')
            print(f"你可以继续或者离开，你当前的奖励是{user_price_dict[turn_key]}$")
            print("1.继续 2.离开")
            choice = input("请输入: ")
            if choice == '2':
                #game.add_money(user_price_dict[turn_key])
                game.data['levels_num'] += math.floor(user_price_dict[turn_key] // 20)
                game.add_money(math.floor(user_price_dict[turn_key]) - (math.floor(user_price_dict[turn_key] * level_return_money_book[str(game.data['levels'])])))
                game.level_up()
                print(f"***************************************************************")
                print(f"*你获得了{math.floor(user_price_dict[turn_key])}$,缴纳手续费后实际获得{math.floor(user_price_dict[turn_key]) - (math.floor(user_price_dict[turn_key] * level_return_money_book[str(game.data['levels'])]))}$")
                print(f"*你获得了{math.floor(user_price_dict[turn_key] // 20)}经验")
                print(f"***************************************************************")
                game.save_data()
                if game.level_up():
                    print('恭喜你升级了！')
                game.save_data()
                main_print()
                break
            elif choice == '1':
                continue

def game_mode_4_start():
    print('')
def AI_bj():
    ai_get_card  = poker.draw_card()
    ranks = ai_get_card[:-1]
    ai_card.append(f'{ranks}')

def bj_1():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 10:
        print('您有资格参与小场')
        return True
    else:
        print('不好意思您无法进场')
        return False

def bj_2():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 50000:
        print('您有资格参与中场')
    else:
        print('您无法进场')
        return False

def bj_3():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 1000000:
        print('您有资格参与大场')
    else:
        print('您无法进场')
        return False

def bj_4():
    game = Game('data.json', 'secret.key')
    if game.get_money() >= 10000000:
        print('您有资格参与至尊场')
    else:
        print('您无法进场')
        return False

def get_money():
    print('银行最多可以借你的资产*(0.6*等级)，但是利率低。个人最多可以借你的资产*(0.9*等级)，利率中。xx科技公司可以借无上限，但是利率很高。')
    print('默认在第八个月时还款，你也可以选择提前还款')
    print('利率表：银行每月1%，个人每月4%，xx科技公司每月10%')
    print('1.bank')
    print('2.individual')
    print('3.xx科技公司')
    print('4.还款')
    print('0.返回')
    while True:
        if keyboard.is_pressed('1'):
            print('你选择了bank')
            print('你可以借的金额上限为:',math.floor(game.data['money'] * (0.6 * game.data['levels'])),'$')
            bank_borrow_money = int(input('请输入你要借的金额:(输入0块钱可以返回) '))
            if bank_borrow_money <= math.floor(game.data['money'] * (0.6 * game.data['levels'])):
                game.add_money(bank_borrow_money)
                game.data['bank_have_borronw'] = 1
                bank_borrow_month = game.data['month']
                print('借款成功！')
                print('请在',bank_borrow_month + 8,'月之前还款！')
                print('摁任意键返回游戏大厅')
                if game.wait_for_any_key():
                    return False
            elif bank_borrow_money >= math.floor(game.data['money'] * (0.6 * game.data['levels'])):
                print('借款失败，超过上限！')
            elif game.data['bank_have_borronw'] == 1:
                print('请先还款！')
            elif bank_borrow_money == 0:
                main_print()
                return False
            time.sleep(1)
        elif keyboard.is_pressed('2'):
            print('你选择了individual')
            print('你可以借的金额上限为:',math.floor(game.data['money'] * (0.9 * game.data['levels'])),'$')
            individual_borrow_money = int(input('请输入你要借的金额:(输入0块钱可以返回) '))
            if individual_borrow_money <= math.floor(game.data['money'] * (0.9 * game.data['levels'])):
                game.add_money(individual_borrow_money)
                game.data['individual_have_borronw'] = 1
                individual_borrow_month = game.data['month']
                print('借款成功！')
                print('请在',individual_borrow_month + 8,'月之前还款！')
                print('摁任意键返回游戏大厅')
                if game.wait_for_any_key():
                    return False
            elif individual_borrow_money >= math.floor(game.data['money'] * (0.9 * game.data['levels'])):
                print('借款失败，超过上限！')
            elif game.data['individual_have_borronw'] == 1:
                print('请先还款！')
            elif individual_borrow_money == 0:
                main_print()
                return False
            time.sleep(1)
        elif keyboard.is_pressed('3'):
            print('你选择了xx科技公司')
            xx_borrow_money = int(input('请输入你要借的金额:(输入0块钱可以返回) '))
            if xx_borrow_money > 0:
                game.add_money(xx_borrow_money)
                game.data['xx_have_borronw'] = 1
                xx_borrow_month = game.data['month']
                print('借款成功！')
                print('请在',xx_borrow_month + 8,'月之前还款！')
                print('摁任意键返回游戏大厅')
                if game.wait_for_any_key():
                    return False
            elif game.data['xx_have_borronw'] == 1:
                print('请先还款！')
            elif xx_borrow_money == 0:
                main_print()
                return False
            time.sleep(1)
        elif keyboard.is_pressed('4'):
            print('请选择你要还款的对象：'
                  '1.bank 2.individual 3.xx科技公司')
            repay_choice = input('请输入: ')
            if repay_choice == '1':
                if bank_have_borronw == 1:
                    bank_one_month = game.data['month'] - bank_borrow_month
                    if bank_one_month <= 1 :
                        bank_one_month = 1
                    else:
                        bank_one_month = game.data['month'] - bank_borrow_month
                        bank_repay_money = math.ceil(bank_borrow_money * (1 + 0.01 * bank_one_month))
                        print('你需要还款的金额为:',bank_repay_money,'$')
                        repay_money = int(input('请输入你要还款的金额: '))
                        if repay_money > 0 and repay_money <= game.data['money']:
                            game.subtract_money(repay_money)
                            print('还款成功！')
                            if repay_money >= bank_borrow_money * (1 + 0.01 * bank_one_month):
                                bank_have_borronw=0
                                print('你已经完全还清了bank的借款！')
                            else:
                                print('你还欠bank',math.ceil(bank_borrow_money * (1 + 0.01 * bank_one_month) - repay_money),'$')
                        elif repay_money > game.data['money']:
                            print('你没有足够的余额还款！')
                        elif repay_money <= 0:
                            print('请输入一个正数！')
                else:
                    print('你没有bank的借款需要还！')
            elif repay_choice == '2':
                if individual_have_borronw == 1:
                    indivdual_one_month = game.data['month'] - individual_borrow_month
                    if indivdual_one_month <= 1 :
                        indivdual_one_month = 1
                    else:
                        indivdual_one_month = game.data['month'] - individual_borrow_month
                        individual_repay_money = math.ceil(individual_borrow_money * (1 + 0.04 * indivdual_one_month))
                        print('你需要还款的金额为:',individual_repay_money,'$')
                        repay_money = int(input('请输入你要还款的金额: '))
                        if repay_money > 0 and repay_money <= game.data['money']:
                            game.subtract_money(repay_money)
                            print('还款成功！')
                            if repay_money >= individual_borrow_money * (1 + 0.04 * indivdual_one_month):
                                individual_have_borronw=0
                                print('你已经完全还清了individual的借款！')
                            else:
                                print('你还欠individual',math.ceil(individual_borrow_money * (1 + 0.04 * indivdual_one_month) - repay_money),'$')
                        elif repay_money > game.data['money']:
                            print('你没有足够的余额还款！')
                        elif repay_money <= 0:
                            print('请输入一个正数！')
                else:
                    print('你没有individual的借款需要还！')
            elif repay_choice == '3':
                if xx_have_borronw == 1:
                    xx_one_month = game.data['month'] - xx_borrow_month
                    if xx_one_month <= 1 :
                        xx_one_month = 1
                    else:
                        xx_one_month = game.data['month'] - xx_borrow_month
                    xx_repay_money = math.ceil(xx_borrow_money * (1 + 0.1 * xx_one_month))
                    print('你需要还款的金额为:',xx_repay_money,'$')
                    repay_money = int(input('请输入你要还款的金额: '))
                    if repay_money > 0 and repay_money <= game.data['money']:
                        game.subtract_money(repay_money)
                        print('还款成功！')
                        if repay_money >= xx_borrow_money * (1 + 0.1 * xx_one_month):
                            xx_have_borronw=0
                            print('你已经完全还清了xx科技公司的借款！')
                        else:
                            print('你还欠xx科技公司',math.ceil(xx_borrow_money * (1 + 0.1 * xx_one_month) - repay_money),'$')
                    elif repay_money > game.data['money']:
                        print('你没有足够的余额还款！')
                    elif repay_money <= 0:
                        print('请输入一个正数！')
                else:
                    print('你没有xx科技公司的借款需要还！')
        


        elif keyboard.is_pressed('2'):
            print('你选择了individual')
            # 在这里添加individual的逻辑
            time.sleep(1)
        elif keyboard.is_pressed('3'):
            print('你选择了xx科技公司')
            # 在这里添加xx科技公司的逻辑
            time.sleep(1)
        elif keyboard.is_pressed('4'):
            print('你选择了还款')
            # 在这里添加还款的逻辑
            time.sleep(1)
        elif keyboard.is_pressed('0'):
            break

def pp():
    print('内哥不是内哥，只有第三个是能玩的，别的有时间再搞，工作量大，还没搞好'
          '三秒后游戏退出')
    time.sleep(3)
    exit()

def set_console_size(width, height):#设置控制台窗口大小（Windows）
    try:
        # 使用mode命令设置控制台大小
        os.system(f'mode con: cols={width} lines={height}')
    except Exception as e:
        return False

def start_texas_holdem():
    #启动德州扑克游戏
    import subprocess
    import os
    import time
    
    # 德州扑克游戏路径
    poker_dir = r"neuron_poker-master"
    python39_path = r"C:\Python39\python.exe"
    
    # 检查目录是否存在
    if not os.path.exists(poker_dir):
        print(f"错误：找不到德州扑克游戏目录 {poker_dir}")
        print("请检查路径是否正确")
        input("按回车键返回主菜单...")
        return
    
    print("正在启动德州扑克游戏...")
    print("游戏将在新窗口中运行")
    print("=" * 50)
    
    try:
        # 在新窗口中启动游戏
        process = subprocess.Popen(
            [python39_path, "main.py", "selfplay", "keypress"],
            cwd=poker_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print(f"德州扑克游戏已启动！(进程ID: {process.pid})")
        print("请切换到新窗口进行游戏")
        print("\n" + "=" * 50)
        print("【重要】游戏结束后，请关闭那个黑色窗口")
        print("然后在这个窗口中按回车键返回主菜单")
        print("=" * 50)
        
        # 等待用户按回车
        input()
        
        # 检查进程是否还在运行，如果在就结束它
        if process.poll() is None:
            print("正在关闭德州扑克游戏...")
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
        
    except Exception as e:
        print(f"启动失败：{e}")
        print("可能的原因：")
        print("1. Python 3.9 未正确安装")
        print("2. 游戏文件路径不正确")
        print("3. 缺少必要的依赖包")
        input("按回车键返回主菜单...")

main_print()

game_mode = 'main'

while True:
    if game_mode == 'main':
        try:
            main_input = str(input("在游戏大厅按对应数字键选择游戏，进入后按照提示操作即可："))
            main_menu_input = None
        except ValueError:
            print('请输入整数')
            game_mode == 'nothing'
            game_mode == 'main'
            main_print()
        if main_input == '1' or main_menu_input == '1':
            print('你选择了交易所')
            game_mode = 'transaction'
            time.sleep(1)  # 防止重复触发
        elif main_input == '2' or main_menu_input == '2':
            print('你选择了德*扑克')
            start_texas_holdem()
                # 在这里添加德*扑克游戏的逻辑
            time.sleep(1)
        elif main_input == '3' or main_menu_input == '3':
            print('你选择了俄罗斯*轮盘')
            game_mode_3()
            game_mode = 'game_3'
            time.sleep(1)
        elif main_input == '4' or main_menu_input == '4':
            print('你选择了二十一点')
            game_mode = 'blackjack'
            while keyboard.is_pressed('4'):
                time.sleep(0.1)
            time.sleep(0.2)  # 额外等待
            game_mode = 'blackjack'
            blackjack.bj_print()
            time.sleep(0.2)
                # 在这里添加二十一点游戏的逻辑
            time.sleep(1)
        elif main_input == '5' or main_menu_input == '5':#借钱
            game_mode = 'get_money'
            print('你选择了借money')
            get_money()
            time.sleep(1)
        elif main_input == '6' or main_menu_input == '6':#管理员
            print('进入管理员模式')
            password_input = input(str('请输入管理员密码: '))
            if game.verify_password(password_input):
                game_mode = 'admin'
            else:
                print('密码错误')
                main_print()
            time.sleep(1)
        elif main_input == '7' or main_menu_input == '7':
            exit()
        elif main_input == '8' or main_menu_input == '8':
            game_mode = 'game_explain'
            print('***************************************************************************************************')
            print('游戏版本：v1.0.92小版本  发布时间：2026/3/21')
            print('广州市第二中学2023届230516开发')
            print('作者的话：')
            print('写这个游戏其实有小学的因素，我在小学机房里面留下的CS1.6，给很多我下几届的学生带来一点娱乐')
            print('二中局域网我也调用不了，寻思做一个单机游戏，娱乐一下大家')
            print('虽然这个游戏说不上正能量，但是我觉得只是一个游戏，大家可以当成一个娱乐的东西，毕竟现在的游戏也不都是正能量的')
            print('现实中千万不要赌博，远离毒品！')
            print('开发过程不算非常难，但是写起来还是比较麻烦的')
            print('这个项目我是当一个小的python练习，游戏大厅你输入数字之后没反应的就是懒得写了')
            print('如果你想完成这个游戏，可以在github上找到这个项目，或者添加微信号：vicetone9y9，备注：main.py')
            print('***************************************************************************************************')
            print('更新日志:\nv1.0.1 2026/2/21 游戏大体结构创建\nv1.0.2 2026/2/22 游戏3搭建完成，大厅优化,增加管理者模式\nv1.0.3 2026/2/23 增加无敌模式，借money，月份系统。优化储存，数据加密')
            print('v1.0.4beta 2026/2/26 修复巨大的储存调用bug，优化扑克牌系统，完成21点项目菜单\nv1.0.4 2026/2/26 修复21点菜单界面逻辑问题')
            print('v1.0.5beta 2026/2/28 修复了一些连接问题，增加德州扑克游戏插件（github开源项目）')
            print('v1.0.16 2026/3/3 选项1名称改为“交易所”，添加真实的黄金售价数据进入游戏，每天第一次打开交易所将会获取真实数据，游戏内当天每过一个月将会随机算法输出数据\n，此功能仅会在online版本上线。单机版采用随机算法')
            print('v1.0.7online 2026/3/4 丰富交易所界面。主菜单增加9——仓库功能，游戏正式进入online版本')
            print('v1.0.8online 2026/3/6 交易所添加真实外汇交易，但是有高税，目前支持港元、英镑、埃及镑、日元交易')
            print('v1.0.9online 2026/3/19 增加货币交易加密，和储存加密，管理员模式已添加修改功能')
            print('0.返回')
        elif main_input == '9' or main_menu_input == '9':#仓库
            set_console_size(30,60)
            game_mode = 'warehouse'
            print('拥有可交易黄金9999：',game.get_gold(),'g','\n目前不可交易黄金：0','g')
            print('可交易日元：',game.get_currency('JPY'),'元')
            print('可交易埃及镑：',game.get_currency('EGP'),'元')
            print('可交易英镑：',game.get_currency('GBP'),'元')
            print('可交易港元：',game.get_currency('HKP'),'元')
            print('0.退出')
        elif main_input.count('\\') > 0:#判断指令符号
            if "help" in main_input:#帮助
                game_mode = 'nothing'
                os.system('cls')
                print('\next 下一个月')
                print('0.返回')
                if keyboard.is_pressed('0'):
                    game_mode = 'main'
                    main_print()
                    time.sleep(1)
            elif "next" in main_input:#下一个月
                game.data['month'] += 1
                game.data['month_turn'] = 0
                game.save_data()
                print('执行中...')
                time.sleep(1)
                os.system('cls')
                main_print()
            else:#无命令处理
                print(main_input,'无法查找到指令对象')
                game_mode = 'main'
                time.sleep(0.5)
        else:#判断是否有菜单中的序列号
            print('无法查找到菜单序列号对象')
            game_mode = 'nothing'
            game_mode = 'main'
            time.sleep(0.5)
    elif game_mode == 'game_explain' or game_mode == 'warehouse':
        if keyboard.is_pressed('0'):
            set_console_size(120,40)
            game_mode = 'main'
            main_print()
            time.sleep(1)
    elif game_mode == 'game_3':#俄罗斯*轮盘
        if keyboard.is_pressed('1'):
                print('开始游戏')
                game_mode_3_start()
                game.data['month_turn'] += 1
                time.sleep(1)
        elif keyboard.is_pressed('2'):
                print('退出游戏')
                main_print()
                game_mode = 'main'
                time.sleep(1)
        elif keyboard.is_pressed('3'):
                game_mode = 'game_3_explain'
                print('游戏说明')
                print('6个空位，然后每一次你可以选择离开或者继续')
                print('如果你选择继续，系统会随机生成一个空位，如果你选择的空位被系统选中，你就输了,你的资产和将会清空')
                print('每一次你选择继续，系统都会给你奖励，奖励的金额会随着你选择继续的次数增加而增加')
                print('如果你选择离开，你就可以获得当前的奖励，多少颗子弹影响奖励档位')
                print('0.返回')
    elif main_input == '0' and game_mode == 'game_3_explain':
                game_mode = 'game_3'
                game_mode_3()
                time.sleep(1)
    elif game_mode == 'admin':#管理员
        admin_print()
        if keyboard.is_pressed('1'):
                new_password = input('请输入新的管理员密码: ')
                # 直接加密并保存新密码
                game.data['password'] = game.hash_password(new_password)
                game.save_data()
                print('管理员密码已修改成功！')
                admin_print()
                time.sleep(1)
        elif keyboard.is_pressed('2'):
            print('1.修改基础数据')
            print('2.修改仓库数据')
            try:
                admin_input = int(input('请输入菜单选项：'))
            except ValueError:
                print('输入格式错误')
                continue
            if admin_input == 1:
                current_money = game.data['money']
                current_levels = game.data['levels']
                current_levels_num = game.data['levels_num']
                current_month = game.data['month']
                current_month_turn = game.data['month_turn']
                # 输入新值，如果直接回车则使用原值
                money_input = input(f'请输入新的玩家余额 (当前: {current_money}): ')#bug###########################################################
                if money_input.strip():  # 如果输入不为空
                    new_money = int(money_input)
                else:
                    new_money = current_money
                levels_input = input(f'请输入新的玩家等级 (当前: {current_levels}): ')
                if levels_input.strip():
                    new_levels = int(levels_input)
                else:
                    new_levels = current_levels
                levels_num_input = input(f'请输入新的玩家经验 (当前: {current_levels_num}): ')
                if levels_num_input.strip():
                    new_levels_num = int(levels_num_input)
                else:
                    new_levels_num = current_levels_num
                month_input = input(f'请输入新的月份 (当前: {current_month}): ')
                if month_input.strip():
                    new_month = int(month_input)
                else:
                    new_month = current_month
                month_turn_input = input(f'请输入新的月份回合数 (当前: {current_month_turn}): ')
                if month_turn_input.strip():
                    new_month_turn = int(month_turn_input)
                else:
                    new_month_turn = current_month_turn
                # 更新数据
                game.data['money'] = new_money
                game.set_money(new_money)
                game.data['levels'] = new_levels
                game.data['levels_num'] = new_levels_num
                game.data['month'] = new_month
                game.data['month_turn'] = new_month_turn
                game.save_data()
                admin_print()
                time.sleep(1)
            elif admin_input == 2:#修改仓库
                print("===== 修改货币数量 =====")
                print("1. 修改英镑 (GBP)")
                print("2. 修改埃及镑 (EGP)")
                print("3. 修改港元 (HKP)")
                print("4. 修改日元 (JPY)")
                print('5. 修改黄金 (99.99%)')
                print("0. 返回")
                
                try:
                    currency_choice = int(input("请选择要修改的货币: "))
                except Exception:
                    print('输入错误')
                    continue

                if currency_choice == 0:
                    game_mode = 'nothing'
                    for i in range(10):
                        print('')
                    game_mode = 'admin'
                    admin_print()
                    
                elif currency_choice == 1:
                    current = game.get_currency('GBP')
                    new_value = input(f"当前英镑: {current}, 请输入新数量: ")
                    if new_value.strip():
                        game.set_currency('GBP', int(new_value))
                        print(f"英镑已设置为 {new_value}")
                elif currency_choice == 2:
                    current = game.get_currency('EGP')
                    new_value = input(f"当前埃及镑: {current}, 请输入新数量: ")
                    if new_value.strip():
                        game.set_currency('EGP', int(new_value))
                elif currency_choice == 3:
                    current = game.get_currency('HKP')
                    new_value = input(f"当前港元: {current}, 请输入新数量: ")
                    if new_value.strip():
                        game.set_currency('HKP', int(new_value))
                elif currency_choice == 4:
                    current = game.get_currency('JPY')
                    new_value = input(f"当前日元: {current}, 请输入新数量: ")
                    if new_value.strip():
                        game.set_currency('JPY', int(new_value))
                elif currency_choice == 5:
                    current = game.get_gold()
                    new_value = input(f"当前黄金99.99%：{current}，请输入新数量:")
                    if new_value.strip():
                        game.set_gold(int(current))
                else:
                    print('未找到有效对象')
                    continue
                game_mode = 'nothing'
                game_mode = 'admin'
        elif keyboard.is_pressed('3'):#重置    增加金钱重置
                game.data['money'] = 1000000
                game.data['levels'] = 1
                game.data['levels_num'] = 0
                game.data['month'] = 0
                game.data['month_turn'] = 0
                game.data['bank_have_borronw'] = 0
                game.data['individual_have_borronw'] = 0
                game.data['xx_have_borronw'] = 0
                
                game.save_data()
                print('玩家数据已重置')
                admin_print()
                time.sleep(1)
        elif keyboard.is_pressed('4'):
                invincible()
                print('无敌模式切换成功,再次点击4可切换无敌状态')
                game_mode = 'admin'
                admin_print()
                time.sleep(1)
        elif keyboard.is_pressed('5'):
                main_print()
                game_mode = 'main'
                time.sleep(1)
    elif game_mode == 'get_money':#借钱返回逻辑

        if keyboard.is_pressed('0'):
            game_mode = 'main'
            main_print()
            time.sleep(1)
        elif get_money() == False:
                
                game_mode = 'main'
                main_print()
                time.sleep(1)
    elif game_mode == 'blackjack':
        ai_card_num = 0#初始化AI手牌数量
        choice = str(input('请输入数字'))
        if choice == '0':
            main_print()
            game_mode = 'main'
            time.sleep(1)
        elif choice == '1':
            game_mode = 'bj_rule'
            blackjack.bj_rule()
            time.sleep(1)
        elif choice == '2':
            bj_level = 1
            bj_1()
            if not bj_1():
                game_mode = 'blackjack'
                blackjack.bj_print()
            input_money_bj = int(input("输入******:"))
            if input_money_bj <= 10:
                print('You need call more money!')
            elif input_money_bj > 10000:
                print('You call money too more,you can turn up a level. ')
            time.sleep(1)
        elif choice == '3':
            bj_level = 2
            bj_2()
            if not bj_2():
                game_mode = 'blackjack'
                blackjack.bj_print()
            input_money_bj = int(input("输入******:"))
            if input_money_bj <= 50000:
                print('You need call more money!')
            elif input_money_bj > 400000:
                print('You call money too more,you can turn up a level. ')
            time.sleep(1)
        elif choice == '4':
            bj_level = 3
            bj_3()
            if not bj_3():
                game_mode = 'blackjack'
                blackjack.bj_print()
            input_money_bj = int(input("输入******:"))
            if input_money_bj <= 1000000:
                print('You need call more money!')
            elif input_money_bj > 3000000:
                print('You call money too more,you can turn up a level. ')
            time.sleep(1)
        elif choice == '5':
            bj_level = 4
            bj_4()
            if not bj_4():
                game_mode = 'blackjack'
                blackjack.bj_print()
            input_money_bj = int(input("输入******:"))
            if input_money_bj <= 10000000:
                print('You need call more money!')
            time.sleep(1)
    elif game_mode == 'bj_rule':
            if keyboard.is_pressed('0'):
                game_mode = 'blackjack'
                blackjack.bj_print()
                time.sleep(1)
    elif game_mode == 'transaction':#交易所逻辑
            print('你选择了交易所')
            print('')
            print('')
            print("每日第一次打开将会获取昨日的真实数据来填充交易所")
            print('1.黄金/外币汇率（真实数据每日只会更新一次）')
            print('2.虚拟股票')
            print('0.退出')
            time.sleep(0.2)
            try:                
                input_1 = int(input('请输入数字:'))
            except ValueError:
                print('请输入整数')
                continue
            if input_1 == 1:#黄金、外汇交易逻辑
                set_console_size(40,60)
                gold.take_gold_money()
                international_currency.exchange_currency_GBP()
                international_currency.exchange_currency_EGP()
                international_currency.exchange_currency_HKD()
                international_currency.exchange_currency_JPY()
                gold_transaction = str(input('请输入交易序列号\n（序列号为顺序个数，第一个为0）\n输如"e"返回：'))
                if gold_transaction == 'e':
                    set_console_size(120,40)
                    game_mode == 'main'
                    game_mode == 'transaction'
                elif gold_transaction == '0':
                    print('='*10,"GBP交易",'='*10)
                    transaction.sell_print()

            elif input_1 == 2:#虚拟股票交易逻辑
                pp()
            elif input_1 == 0:
                set_console_size(120,40)
                main_print()
                game_mode = 'main'



#判断交易逻辑


#检验21点的AI_bj()输出情况