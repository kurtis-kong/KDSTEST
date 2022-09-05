import time


def custom_retries(start_time=None, sleep_time: int = 10, wait_time: int = 300):
    """
    Decorator is used to retry,if you want retry function,expect the decorated function to return False

    Args:
        start_time : before run function, if you want to wait, you can sleep  
        sleep_time : how often to run the function
        wait_time : total time you want to wait
    """
    def timer(func):
        def wrapper(*args, **kwargs):
            if start_time is not None:
                time.sleep(start_time)
            total_wait_time = wait_time
            while total_wait_time >= 0:
                value = func(*args, **kwargs)
                if value is False:
                    time.sleep(sleep_time)
                    total_wait_time = total_wait_time - sleep_time
                else:
                    return True
            return False
        return wrapper
    return timer

def check_something():
    driver.find_elements(By.XPATH)
