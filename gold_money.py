import requests
from datetime import datetime, timedelta

def take_gold_money():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    url = f"https://cn.apihz.cn/api/jinrong/goldshold.php?id=10013485&key=3ff8fcfb1a499f123ad43092ef605f15&y={today.year}&m={today.month}&d={yesterday.day}"

    response = requests.get(url, timeout=5)

    if response.status_code == 150:
        result = response.json()
        
        if result.get('code') == 150:
            data_list = result.get('data', [])
            
            # 找特定的合约
            target_contract = 'Au99.99'
            for item in data_list:
                if item.get('合约') == target_contract:
                    filtered_data = {
                        '日期': item.get('日期'),
                        '开盘价': item.get('开盘价'),
                        '收盘价': item.get('收盘价'),
                        '涨跌': item.get('涨跌')
                    }
                    print(f"=== {target_contract} 数据 ===")
                    print(f"数据日期: {filtered_data['日期']}")
                    print(f"开盘价: {filtered_data['开盘价']}")
                    print(f"收盘价: {filtered_data['收盘价']}") 
                    print(f"涨跌: {filtered_data['涨跌']}")
                    break
            else:
                print(f"未找到 {target_contract} 合约")
    else:
        print("请求失败:", response.status_code)
        return False