import json
import time
import os
import keyboard
import math
import random
import hashlib
from cryptography.fernet import Fernet

import blackjack

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
    
    def decrypt_money(self, encrypted_money):#解密金钱
        try:
            decrypted = self.cipher.decrypt(encrypted_money.encode())
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
    
    def load_data(self):#加载数据
        initial_data = {
            'money': self.encrypt_money(1000),  # 加密存储
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
        
        if not os.path.exists(self.js_file):
            with open(self.js_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=4, ensure_ascii=False)
            return initial_data.copy()
        else:
            with open(self.js_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'money' in data:
            # 如果 money 是整数，说明是旧数据，需要重新加密
                if isinstance(data['money'], int):
                    print("检测到旧数据格式，正在转换金钱加密格式...")
                    data['money'] = self.encrypt_money(data['money'])
        
        return data
    
    def save_data(self):
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

game = Game('data.json', 'secret.key')

print('广州市第二中学2023届230516开发')
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
    print('1.*票')
    print('2.德*扑克')
    print('3.俄罗斯*轮盘')
    print('4.二十一点')
    print('======其他功能======')
    print('5.借money')
    print('6.管理员模式')
    print('7.退出游戏')
    print('8.关于游戏')
    print('#####################')
    print('在游戏大厅按对应数字键选择游戏，进入后按照提示操作即可')
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
                if game.level_up():
                    print('恭喜你升级了！')
                game.save_data()
                main_print()
                break
            elif choice == '1':
                continue

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

main_print()

game_mode = 'main'

while True:
    if game_mode == 'main':
        if keyboard.is_pressed('1'):
            print('你选择了*票')
            pp()
                # 在这里添加*票游戏的逻辑
            time.sleep(1)  # 防止重复触发
        elif keyboard.is_pressed('2'):
            print('你选择了德*扑克')
            pp()
                # 在这里添加德*扑克游戏的逻辑
            time.sleep(1)
        elif keyboard.is_pressed('3'):
            print('你选择了俄罗斯*轮盘')
            game_mode_3()
            game_mode = 'game_3'
            time.sleep(1)
        elif keyboard.is_pressed('4'):
            print('你选择了二十一点')
            game_mode = 'blackjack'
            pp()
                # 在这里添加二十一点游戏的逻辑
            time.sleep(1)
        elif keyboard.is_pressed('5'):#借钱
            game_mode = 'get_money'
            print('你选择了借money')
            get_money()
            time.sleep(1)
        elif keyboard.is_pressed('6'):
            print('进入管理员模式')
            password_input = input(str('请输入管理员密码: '))
            if game.verify_password(password_input):
                game_mode = 'admin'
                admin_print()
            else:
                print('密码错误')
                main_print()
            time.sleep(1)
        elif keyboard.is_pressed('7'):
            exit()
        elif keyboard.is_pressed('8'):
            game_mode = 'game_explain'
            print('游戏版本：v1.0.3  发布时间：2026/2/23')
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
            print('0.返回')
    elif game_mode == 'game_explain':
        if keyboard.is_pressed('0'):
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
    elif keyboard.is_pressed('0') and game_mode == 'game_3_explain':
                game_mode = 'game_3'
                game_mode_3()
                time.sleep(1)
    elif game_mode == 'admin':
        if keyboard.is_pressed('1'):
                new_password = input('请输入新的管理员密码: ')
                # 直接加密并保存新密码
                game.data['password'] = game.hash_password(new_password)
                game.save_data()
                print('管理员密码已修改成功！')
                admin_print()
                time.sleep(1)
        elif keyboard.is_pressed('2'):
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
                game.data['levels'] = new_levels
                game.data['levels_num'] = new_levels_num
                game.data['month'] = new_month
                game.data['month_turn'] = new_month_turn
                game.save_data()
                admin_print()
                time.sleep(1)
        elif keyboard.is_pressed('3'):
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
        if keyboard.is_pressed('1'):
            