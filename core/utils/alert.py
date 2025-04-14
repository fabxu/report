import requests
from core.errors.error import Error
import yaml
from datetime import datetime

class AlertClient:
    def __init__(self, config_path: str):
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)
            alert_config = data.get("alert", {})
            url = alert_config.get("path", "")
            key = alert_config.get("key", "")
            template = alert_config.get("templates", "")
            
            self.url = url.format(key)
            self.template = template
    
    def send_alert_msg(self, report_name: str, job_name: str, job_creator: str, job_id: int, msg: str) -> Error:
        wrapped_content = self.template.format(report_name, job_name, job_creator, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), job_id, msg)
        content_body = {
            "msgtype": "markdown",
            "markdown": {
                "content": wrapped_content
            }
        }
        response = requests.post(self.url, json=content_body)
        return response
