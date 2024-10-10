import logging
from playwright.sync_api import Browser
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
from page_objects.demo_pages import DemoPages
from page_objects.test_cases import TestCases

class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self. page)

        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'page: {self.page.url}, console error: {message.text}')

        def dialog_handler(dialog: Dialog):
             logging.warning(f'page: {self.page.url}, dialog text: {dialog.message}')
             dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)
    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu:  str):
        self.page.click(f'text="{menu}"')
        self.page.wait_for_timeout(100)

    def login(self, login: str, password: str):
        self.page.fill('#id_username', login)
        self.page.fill('#id_password', password)
        self.page.click('input[type="submit"][value="Login"]')
        self.page.wait_for_timeout(100)

    def create_test(self, test_name: str, test_description: str):
        self.navigate_to('Create new test')
        self.page.fill('#id_name', test_name)
        self.page.fill('#id_description', test_description)
        self.page.click('input[type="submit"][value="Create"]')
        self.page.wait_for_timeout(100)

    def click_menu_button(self):
        self.page.click('.menuBtn')

    def is_menu_button_visible(self):
        return self.page.is_visible('.menuBtn')

    def get_location(self):
        return self.page.text_content('.position')

    def intercept_requests(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)

    def stop_intercept(self, url: str):
        self.page.unroute(url)

    def refresh_dashboard(self):
        self.page.click('input')

    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')

    def close(self):
        self.page.close()
        self.context.close()