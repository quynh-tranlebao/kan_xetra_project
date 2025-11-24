"""running the Xetra ETL application"""
import logging
import logging.config

import yaml

def main():
    # Parsing YAML file
    config_path = 'C:/xetra_project/kan_xetra_project/configs/xetra_report_config.yml'
    config  = yaml.safe_load(open(config_path))
    #print(config)
    # configure logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info("This is a test.")


if __name__ =='__main__':
    main()