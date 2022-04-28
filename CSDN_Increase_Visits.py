import json
import time
import os
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By


def click_loop(user_name: str = 'aaaaaaze', loops: int = 86400, duration: float = 0.0):
    """
    :param user_name: CSDN username
    :param loops: times to loop
    :param duration: waiting time between loops, in seconds
    """

    blog_site = f'https://blog.csdn.net/{user_name}?type=blog'

    # creating cookies if not exist
    if not os.path.exists('cookies.json'):
        driver = webdriver.Chrome()
        driver.get(blog_site)
        driver.maximize_window()
        print('Login and press \'ESC\' to acquire cookies.')
        keyboard.wait('esc')
        cookie_list = driver.get_cookies()
        with open('cookies.json', 'w') as f:
            f.write(json.dumps(cookie_list))
        print('Cookies Saved.')
        driver.close()
        driver.quit()
    else:
        print('Cookies checked.')

    # click loop
    for i in range(loops):
        t_start = time.time()

        # init
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=option)
        driver.get(blog_site)

        # Read Cookies
        with open('cookies.json', 'r') as f:
            cookie_list = json.load(f)
        for cookie in cookie_list:
            driver.add_cookie(cookie)
        driver.get(blog_site)
        time.sleep(0.5)

        # Click article
        index = 0
        while index := index + 1:
            time.sleep(0.5)
            xpath = f'//*[@id="userSkin"]/div[2]/div/div[2]/div[1]/div[2]/div/article[{index}]'
            try:
                driver.find_element(by=By.XPATH, value=xpath).click()
            except:
                break
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            time.sleep(0.5)
            driver.close()
            driver.switch_to.window(windows[0])

        driver.quit()
        time.sleep(duration)
        print(f'Round {i + 1} finished, {index} articles clicked, costs {time.time() - t_start:.1f} seconds', )


if __name__ == '__main__':
    click_loop(user_name='aaaaaaze')
