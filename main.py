'''
MIT License
Copyright (c) 2023 GeunHyeok LEE
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import time
import configparser
from sys import exit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore

from src.modules.logger import logger
from src.utils.time import string_to_second
from src.models.lecture import Lecture
from src.models.video import Video
from src.constants import LOGIN_PAGE_URL, \
    STUDY_PAGE_URL, \
    VIDEO_ELAPSE_PERCENT, \
    SELECTORS, \
    LOADING_SYMBOLS

class KNOUAutoPlayer:
    __VERSION__ = '1.0.0'

    def __init__(self, **kwargs):
        logger.info('initializing knou-auto-player')
        try:
            options = webdriver.ChromeOptions()
            enabled_headless = kwargs['enable_headless']
            mute_audio = kwargs['mute_audio']
            enabled_string = f'{Fore.GREEN}enabled{Fore.RESET}'
            disabled_string = f'{Fore.RED}disabled{Fore.RESET}'

            if kwargs['enable_headless']:
                options.add_argument('headless')
                options.add_argument('window-size=800x600')
                options.add_argument('disable-gpu')
                options.add_argument('log-level=3')
            logger.info(f'○ headless mode {enabled_string if enabled_headless else disabled_string}')
            
            if kwargs['mute_audio']:
                options.add_argument("--mute-audio")
            logger.info(f'○ mute audio {enabled_string if mute_audio else disabled_string}')

            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')

            logger.info('loading chrome driver..')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), \
                                      options=options)
            driver.implicitly_wait(5)
        except Exception as e:
            logger.error('failed to load chrome driver', str(e))
            exit()

        self._wait = WebDriverWait(driver, 5)
        self._driver = driver
        self._main_window = None

    def _inspect(self, selector, element=None):
        try:
            self._driver.implicitly_wait(0)
            target = element if element != None else self._driver
            return target.find_element(By.CSS_SELECTOR, selector)
        except:
            return None
        finally:
            self._driver.implicitly_wait(5)

    def login(self, user_id, user_password):
        logger.info('connect to U-KNOU page..')
        self._driver.get(LOGIN_PAGE_URL)

        logger.info('trying to login..')
        prev_url = self._driver.current_url
        try:
            self._driver.find_element(By.NAME, 'username').send_keys(user_id)
            password_field = self._driver.find_element(By.NAME, 'password')
            self._driver.execute_script(
                'arguments[0].value = "{}"'.format(user_password),
                password_field
            )
            password_field.send_keys(Keys.RETURN)
        except Exception as e:
            logger.error('uncaught error occurs', str(e))
            exit()

        time.sleep(3)

        try:
            self._wait.until(EC.url_changes(prev_url))
        except Exception as e:
            logger.error('login timeout')
            exit()

        if 'login' not in self._driver.current_url:
            self._driver.get(STUDY_PAGE_URL)
            self._main_window = self._driver.current_window_handle
            return self
        else:
            logger.error('check account information')
            exit()

    def _open_all_lectures(self):
        lectures = self._driver.find_elements(By.CSS_SELECTOR, \
                                              SELECTORS['LECTURE']['ROOT'])

        for lecture in lectures:
            _, code = lecture.get_attribute('id').split('-')
            more_selector = SELECTORS['LECTURE']['MORE'].replace('@', code)
            lecture.find_element(By.CSS_SELECTOR, more_selector).click()
            time.sleep(0.5)

        for body in self._driver.find_elements(By.CSS_SELECTOR, \
                                               SELECTORS['LECTURE']['BODY']):
            self._driver.execute_script('arguments[0].style.display = "block";', body)

        return lectures

    def _load_lectures(self):
        logger.info('loading lectures and videos..')
        total_videos = 0
        watched_video_count = 0
        waiting_video_count = 0
        not_watched_video_count = 0

        parsed_lectures = []
        for lecture in self._open_all_lectures():
            lecture_data = Lecture()
            parsed_lectures.append(lecture_data)

            # lecture id
            lecture_data.id = lecture.get_attribute('id')

            # lecture title
            lecture_data.title = lecture.find_element(
                By.CSS_SELECTOR,
                SELECTORS['LECTURE']['TITLE']
            ).get_attribute('textContent')
            logger.empty()
            logger.info(str(lecture_data))

            # videos
            videos = lecture.find_elements(By.CSS_SELECTOR, SELECTORS['LECTURE']['VIDEO']['ROOT'])
            total_videos += len(videos)

            for video in videos:
                video_data = Video()
                lecture_data.videos.append(video_data)

                # video id
                video_data.id = video.get_attribute('id')

                # video title
                video_data.title = video.find_element(
                    By.CSS_SELECTOR,
                    SELECTORS['LECTURE']['VIDEO']['TITLE']
                ).get_attribute('textContent').replace('\n', '')

                # check this video is not ready
                waiting_element = self._inspect(SELECTORS['LECTURE']['VIDEO']['WAITING'], \
                                                element=video)
                video_data.waiting = bool(waiting_element)

                if video_data.waiting:
                    waiting_video_count += 1
                else:
                    # if already watch this video, this element has `on` class
                    watched_element = self._inspect(SELECTORS['LECTURE']['VIDEO']['WATCHED'], \
                                                    element=video)
                    if watched_element:
                        video_data.watched = 'on' in watched_element.get_attribute('class')

                    if video_data.watched:
                        watched_video_count += 1
                    else:
                        not_watched_video_count += 1

                logger.info(str(video_data))

        logger.empty()
        logger.success(
            f'{len(parsed_lectures)} lectures, {total_videos} videos loaded'
        )
        logger.info(f'   ├ {Fore.GREEN}✔ watched{Fore.RESET}: {watched_video_count}')
        logger.info(f'   ├ {Fore.YELLOW}◻ waiting{Fore.RESET}: {waiting_video_count}')
        logger.info(f'   └ {Fore.RED}✖ not watched{Fore.RESET}: {not_watched_video_count}')
        logger.empty()

        return parsed_lectures
    
    def _focus_to_main(self):
        self._driver.switch_to.window(self._main_window)
        self._driver.switch_to.default_content()

    def _focus_to_popup(self):
        for window in self._driver.window_handles:
            if window != self._main_window:
                self._driver.switch_to.window(window)
                self._driver.switch_to.default_content()
                return

    def _focus_to_video(self):
        for window in self._driver.window_handles:
            if window != self._main_window:
                self._driver.switch_to.window(window)
                self._driver.switch_to.frame(SELECTORS['PLAYER']['ROOT'])
                return
            
    def _waiting_for_video(self, title):
        symbol_count = len(LOADING_SYMBOLS)
        elapsed_seconds = 0
        total_seconds = 0
        tick = 0
        keep_playing = True

        total_duration = self._driver.find_element(
            By.CSS_SELECTOR, SELECTORS['PLAYER']['TOTAL_DURATION']
        ).get_attribute('textContent')
        total_seconds = string_to_second(total_duration)

        logger.info(f' └ Total duration: {Fore.CYAN}{total_duration}{Fore.RESET}')
        logger.empty()

        while keep_playing:
            elapsed_time = '00:00'
            elapsed_time_element = self._inspect(SELECTORS['PLAYER']['ELAPSED'])
            if elapsed_time_element:
                elapsed_time = elapsed_time_element.get_attribute('textContent')
                elapsed_seconds = string_to_second(elapsed_time)

            elapsed_percent = round((elapsed_seconds / total_seconds) * 100, 2)
            if elapsed_percent >= VIDEO_ELAPSE_PERCENT:
                keep_playing = False

            tick += 1
            symbol = LOADING_SYMBOLS[tick % symbol_count]
            print(f'\r{symbol} Now playing {title}... {elapsed_time} ({elapsed_percent}%)  ', end='')
            time.sleep(0.5)
        else:
            logger.empty()
            logger.info(f'video elapsed over {Fore.CYAN}{VIDEO_ELAPSE_PERCENT}%{Fore.RESET}')
            logger.info('stop watching and close video')
            logger.empty()

        try:
            self._focus_to_popup()
            self._driver.execute_script('fnStudyEnd();')
            alert = self._wait.until(EC.alert_is_present())
            alert.accept()
        except:
            logger.warning('cannot found end study alert')

    def run(self):
        lectures = self._load_lectures()

        for lecture in lectures:
            logger.info(f'{lecture.title}')

            for video in lecture.videos:
                if video.watched:
                    logger.info(f'{Fore.GREEN}(watched){Fore.RESET} {video.title}')
                    continue
                if video.waiting:
                    logger.info(f'{Fore.YELLOW}(waiting){Fore.RESET} {video.title}')
                    continue

                title = f'{lecture.title} :: {video.title}'
                logger.info(f'{Fore.GREEN}preparing{Fore.RESET} {title}')
                self._focus_to_main()
                show_button_selector = SELECTORS['LECTURE']['VIDEO']['SHOW_VIDEO']

                self._open_all_lectures()
                self._driver.find_element(
                    By.CSS_SELECTOR,
                    f'#{video.id} > {show_button_selector}'
                ).click()
                self._focus_to_video()
                
                time.sleep(5)

                try:
                    # press play video button
                    play_button = self._driver.find_element(
                        By.CSS_SELECTOR, SELECTORS['PLAYER']['PLAY']
                    )
                    self._wait.until(EC.visibility_of(play_button))
                    play_button.click()
                    logger.info(f'{Fore.GREEN}playing{Fore.RESET} {title}')
                except:
                    logger.error('cannot found play button')
                    continue

                try:
                    # if play history exist, continue watching from previous playback history
                    continue_button = self._driver.find_element(
                        By.CSS_SELECTOR, SELECTORS['PLAYER']['WATCH_CONTINUE']
                    )
                    self._wait.until(EC.visibility_of(continue_button))
                    continue_button.click()
                    logger.info('continue watching')
                except:
                    pass

                self._waiting_for_video(f'{Fore.CYAN}{title}{Fore.RESET}')
                time.sleep(1)
            else:
                logger.empty()
        else:
            logger.empty()
            logger.success('all videos watched')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    # player
    enable_headless = config.get('player', 'headless') == '1'
    mute_audio = config.get('player', 'mute_audio') == '1'

    # account
    user_id = config.get('account', 'id')
    user_password = config.get('account', 'password')

    if not (user_id and user_password):
        raise ValueError('account information is required')

    KNOUAutoPlayer(enable_headless=enable_headless, mute_audio=mute_audio) \
        .login(user_id, user_password) \
        .run()
