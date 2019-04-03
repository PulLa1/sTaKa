#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/30.
import logging
import yaml
import logging.config
import os


class Log():
    def __init__(self):
        self.logger = logging
        self.main()

    def setup_logging(self,default_path='config.yaml', default_level=logging.INFO):
        path = default_path
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.logger.config.dictConfig(config)
        else:
            self.logger.basicConfig(level=default_level)


    def main(self):
        yaml_path = 'conf.yaml'
        self.setup_logging(yaml_path)

    def get_log(self):
        return self.logger


if __name__ == '__main__':
    log = Log().get_log()
    log.info("cccccsas")

