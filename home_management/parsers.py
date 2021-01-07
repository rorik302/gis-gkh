from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class PassportParser:
    def __init__(self, url):
        self.driver = self._config_driver()
        self.timeout = 10
        self._passport_info = []
        self._url = url
        self._max_requests = 4
        self._table_selector = 'table.attr-body-table'
        self._row_selector = f'{self._table_selector} tbody tr'
        self._collapsed_element_selector = f'{self._row_selector} a._collapsed'
        self._modal_selector = '#loading-dialog'
        self._label_selector = f'{self._row_selector} label'
        self._value_selector = f'{self._row_selector} td.attr-body-td-param-value'
        self._units_selector = self._value_selector

    def get_passport_info(self):
        self.driver.get(self._url)
        self._wait_for_table()
        self._open_collapsed_elements()
        self._extract_passport_info()
        return self._passport_info

    def _extract_passport_info(self):
        rows = self.driver.find_elements_by_css_selector(self._row_selector)
        for row in rows:
            self._passport_info.append(self._generate_record(row))

    def _generate_record(self, row):
        return {
            'index': row.find_element_by_css_selector(self._label_selector).text.split('. ')[0],
            'title': row.find_element_by_css_selector(self._label_selector).text.split('. ')[1],
            'units': self._filter_empty_text(row.find_elements_by_css_selector(self._units_selector)[0].text),
            'value': self._filter_empty_text(row.find_elements_by_css_selector(self._value_selector)[1].text)
        }

    @staticmethod
    def _filter_empty_text(text):
        return None if text in ['', '-'] else text

    def _open_collapsed_elements(self, collapsed_elements=None):
        if collapsed_elements:
            collapsed_elements = self._open_collapsed_and_return_remains(collapsed_elements)
        elif not collapsed_elements:
            collapsed_elements = self._find_collapsed_elements()
            if not collapsed_elements:
                print('Все поля раскрыты')
                return
        return self._open_collapsed_elements(collapsed_elements)

    def _find_collapsed_elements(self):
        try:
            collapsed_elements = self.driver.find_elements_by_css_selector(self._collapsed_element_selector)
            return collapsed_elements if collapsed_elements else None
        except NoSuchElementException:
            return None

    def _open_collapsed_and_return_remains(self, elements):
        if len(elements) >= self._max_requests:
            for _ in elements[:self._max_requests]:
                self._click_element(elements.pop(0))
        else:
            for _ in elements:
                self._click_element(elements.pop(0))
        self._wait_for_modal()
        return elements

    def _click_element(self, element):
        try:
            element.click()
        except ElementClickInterceptedException:
            sleep(1)
            return self._click_element(element)

    def _wait_for_modal(self):
        try:
            WebDriverWait(self.driver, self.timeout * 3).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, self._modal_selector))
            )
            WebDriverWait(self.driver, self.timeout * 60).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, self._modal_selector))
            )
        except TimeoutException:
            pass

    def _wait_for_table(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, self._row_selector)))
        except TimeoutException:
            self.driver.refresh()

    @staticmethod
    def _config_driver():
        options = Options()
        return webdriver.Chrome(options=options)
