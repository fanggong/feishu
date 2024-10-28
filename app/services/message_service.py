from app.feishu.FeishuAppRobot import FeishuAppRobot
from datetime import datetime


class MessageService:
    def __init__(self, robot: FeishuAppRobot):
        self.robot = robot
        self.name = robot.get_robot_name()

    def send_text_message(self, receive_id, content, receive_id_type='user_id'):
        content = {
            'text': f"[{datetime.now()}] {content}"
        }
        self.robot.send_msg(receive_id, 'text', content, receive_id_type)

    def send_interactive_card(self, receive_id, template_id, template_version_name, template_variable, receive_id_type='user_id'):
        self.robot.send_interactive_card(receive_id, template_id, template_version_name, template_variable, receive_id_type)

    def update_interactive_card(self, token, template_id, template_version_name, template_variable):
        self.robot.update_interactive_card(token, template_id, template_version_name, template_variable)
