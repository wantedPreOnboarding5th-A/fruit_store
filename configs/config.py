import os
import yaml

yaml_settings = dict()
path = os.path.abspath(os.path.dirname(__file__))
filename = "config_real.yml"

with open(os.path.join(path, filename)) as f:
    yaml_settings.update(yaml.load(f, Loader=yaml.FullLoader))


class Config:
    databases: dict = yaml_settings["databases"]
    secrets: dict = yaml_settings["secrets"]
    naver_pay: dict = yaml_settings["naver_pay"]
    card_pay: dict = yaml_settings["card_pay"]
    token: dict = yaml_settings["token"]
    # aws_s3: dict = yaml_settings["aws_s3"]


config = Config()
