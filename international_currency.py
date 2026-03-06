import requests
from datetime import datetime

def exchange_currency_GBP():#英镑
    url = "https://cn.apihz.cn/api/jinrong/huilv.php"
    params = {
        'id': '10013485',
        'key': '3ff8fcfb1a499f123ad43092ef605f15',
        'from': 'USD',  # 从美元
        'to': 'GBP',     # 兑换英镑
        'money': '100'      # 兑换1单位货币
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            
            # 检查返回状态码
            if result.get('code') == 200:
                print("=== 美元兑换英镑汇率 ===")
                print(f"更新时间: {result.get('uptime')}")
                print(f"兑换方向: {result.get('from')} → {result.get('to')}")
                print(f"当前汇率: 100 {result.get('from')} = {result.get('rate')} {result.get('to')}")
                print('')
                return {
                    'from_currency': result.get('from'),
                    'to_currency': result.get('to'),
                    'rate': float(result.get('rate', 0)),  # 转换为浮点数
                    'result': float(result.get('result', 0)),  # 转换为浮点数
                    'update_time': result.get('uptime')
                }
            else:
                print("API返回错误:", result.get('message', '未知错误'))
                return None
        else:
            print("请求失败, HTTP状态码:", response.status_code)
            return None
            
    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        return None
    except ValueError as e:
        print("数值转换异常:", str(e))
        return None

def exchange_currency_EGP():#埃及镑
    url = "https://cn.apihz.cn/api/jinrong/huilv.php"
    params = {
        'id': '10013485',
        'key': '3ff8fcfb1a499f123ad43092ef605f15',
        'from': 'USD',  # 从美元
        'to': 'EGP',     
        'money': '100'      # 兑换1单位货币
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            
            # 检查返回状态码
            if result.get('code') == 200:
                print("=== 美元兑换埃及镑汇率 ===")
                print(f"更新时间: {result.get('uptime')}")
                print(f"兑换方向: {result.get('from')} → {result.get('to')}")
                print(f"当前汇率: 100 {result.get('from')} = {result.get('rate')} {result.get('to')}")
                print('')
                return {
                    'from_currency': result.get('from'),
                    'to_currency': result.get('to'),
                    'rate': float(result.get('rate', 0)),  # 转换为浮点数
                    'result': float(result.get('result', 0)),  # 转换为浮点数
                    'update_time': result.get('uptime')
                }
            else:
                print("API返回错误:", result.get('message', '未知错误'))
                return None
        else:
            print("请求失败, HTTP状态码:", response.status_code)
            return None
            
    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        return None
    except ValueError as e:
        print("数值转换异常:", str(e))
        return None
    
def exchange_currency_HKD():#港元
    url = "https://cn.apihz.cn/api/jinrong/huilv.php"
    params = {
        'id': '10013485',
        'key': '3ff8fcfb1a499f123ad43092ef605f15',
        'from': 'USD',  # 从美元
        'to': 'HKD',     
        'money': '100'      # 兑换1单位货币
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            
            # 检查返回状态码
            if result.get('code') == 200:
                print("=== 美元兑换港元汇率 ===")
                print(f"更新时间: {result.get('uptime')}")
                print(f"兑换方向: {result.get('from')} → {result.get('to')}")
                print(f"当前汇率: 100 {result.get('from')} = {result.get('rate')} {result.get('to')}")
                print('')
                return {
                    'from_currency': result.get('from'),
                    'to_currency': result.get('to'),
                    'rate': float(result.get('rate', 0)),  # 转换为浮点数
                    'result': float(result.get('result', 0)),  # 转换为浮点数
                    'update_time': result.get('uptime')
                }
            else:
                print("API返回错误:", result.get('message', '未知错误'))
                return None
        else:
            print("请求失败, HTTP状态码:", response.status_code)
            return None
            
    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        return None
    except ValueError as e:
        print("数值转换异常:", str(e))
        return None
    
def exchange_currency_JPY():#日元
    url = "https://cn.apihz.cn/api/jinrong/huilv.php"
    params = {
        'id': '10013485',
        'key': '3ff8fcfb1a499f123ad43092ef605f15',
        'from': 'USD',  # 从美元
        'to': 'JPY',     
        'money': '100'      # 兑换1单位货币
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            
            # 检查返回状态码
            if result.get('code') == 200:
                print("=== 美元兑换日元汇率 ===")
                print(f"更新时间: {result.get('uptime')}")
                print(f"兑换方向: {result.get('from')} → {result.get('to')}")
                print(f"当前汇率: 100 {result.get('from')} = {result.get('rate')} {result.get('to')}")
                print('')
                return {
                    'from_currency': result.get('from'),
                    'to_currency': result.get('to'),
                    'rate': float(result.get('rate', 0)),  # 转换为浮点数
                    'result': float(result.get('result', 0)),  # 转换为浮点数
                    'update_time': result.get('uptime')
                }
            else:
                print("API返回错误:", result.get('message', '未知错误'))
                return None
        else:
            print("请求失败, HTTP状态码:", response.status_code)
            return None
            
    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        return None
    except ValueError as e:
        print("数值转换异常:", str(e))
        return None
    
if __name__ == "__main__":
    exchange_currency_EGP()
    exchange_currency_GBP()
    exchange_currency_HKD()
    exchange_currency_EGP()