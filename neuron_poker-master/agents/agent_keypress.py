"""manual keypress agent"""

from gym_env.enums import Action


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='Keypress'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = (observation, info)  # not using the observation for random decision
        
         # 动作中文映射
        action_map = {
            0: "弃牌",
            1: "让牌", 
            2: "跟注",
            3: "加注(3BB)",
            4: "加注(½底池)",
            5: "加注(底池)",
            6: "加注(2倍底池)",
            7: "全下"
        }
        
        action = None
        while action is None:
            # 转换动作为中文显示
            action_list = []
            for act in action_space:
                act_num = act.value
                act_name = action_map.get(act_num, str(act))
                action_list.append(f"<{act_name}: {act_num}>")
            
            # 显示操作提示
            print(f"请选择操作（输入数字）: {action_list}")
            
            getch = input()
            try:
                action = Action(int(getch))
            except:  # pylint: disable=bare-except
                print("输入无效，请重新输入")
            return action