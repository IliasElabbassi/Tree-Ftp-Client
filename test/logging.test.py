from logging import log


import logging

def error_test():
    logging.error("This is an error !")

def logging_test():
    logger = logging.getLogger('Logging test')
    logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
    logger.debug('Information Debug')
    logger.info('Information Info')
    logger.warning('Avertissement')
    logger.error('Message d’erreur')
    logger.critical('Erreur grave')

if __name__ == "__main__":
    error_test()