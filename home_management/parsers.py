from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class AddressParser:

    def __init__(self, data):
        self.driver = self._config_driver()
        self._url = 'https://dom.gosuslugi.ru/#!/houses'
        self._data = data
        self._timeout = 5
        self._form_selector = '.form-base form'
        self._form_group_selector = f'{self._form_selector} .form-group'
        self._select_container_selector = f'{self._form_group_selector} .select2-container'
        self._select2_selector = '#select2-drop'
        self._select2_input_selector = f'{self._select2_selector} input'
        self._select2_results_selector = f'{self._select2_selector} ul.select2-results'
        self._select2_no_results_selector = f'{self._select2_results_selector} li.select2-no-results'
        self._select2_result_selector = f'{self._select2_results_selector} li.select2-result'
        self._submit_btn_selector = 'button[type="submit"]'
        self._search_result_selector = '.hcs-public-house-search-block .register-card'
        self._search_no_result_selector = '.hcs-public-house-search-block .app-cabinet-header:not(.ng-hide)'

    def get_passport_url(self):
        self.driver.get(self._url)
        self._wait_for_form()
        self._fill_form()

        self._submit()

        result = self._search_results()

        if result:
            passport_link = self.driver.find_element_by_css_selector('a.cnt-link[ng-click="showPassport(house)"]')
            passport_link.click()
            modal_ok_btn = self.driver.find_element_by_css_selector('.modal button.btn-action')
            modal_ok_btn.click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.quit()
            return url

    def _fill_form(self):
        self._select_region()

        if self._data['city'] and self._data['settlement']:
            self._select_city()
            self._select_settlement2()
        elif self._data['city']:
            self._select_city()
        elif self._data['settlement']:
            self._select_area()
            self._select_settlement()

        if self._data['street']:
            self._select_street()

        if self._data['house']:
            self._select_house()

    def _select_region(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).region-2'))
        )
        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['region'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )

                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_area(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).area-2'))
        )
        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['area'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )

                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_settlement(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).settlement-2'))
        )
        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['settlement'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )

                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_settlement2(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).planningStructureElement-2'))
        )

        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['settlement'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )

                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
                    self._select_settlement()
                    return self._select_city()
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_city(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).city-2'))
        )

        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['city'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )

                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
                    self._select_area()
                    return self._select_city()
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_street(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).street-2'))
        )
        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['street'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )
                if len(select2_results) > 1:
                    for result in select2_results:
                        if self._reduce_string(result.text) == self._reduce_string(f'{self._data["street_type"]} {self._data["street"]}'):
                            result.click()
                            break
                else:
                    if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                        select2_results[0].click()
                    else:
                        print('Результаты не найдены')
                        select2_input.send_keys(Keys.ESCAPE)
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _select_house(self):
        select_field = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'{self._select_container_selector}:not(.select2-container-disabled).house-2'))
        )
        if 'select2-container-disabled' not in select_field.get_attribute('class'):
            chosen = select_field.find_element_by_css_selector('a span.select2-chosen')
            if chosen.text.lower().startswith('выберите'):
                toggle = select_field.find_element_by_css_selector(f'{self._select_container_selector} a')
                toggle.click()
                select2_input = self.driver.find_element_by_css_selector(self._select2_input_selector)
                select2_input.send_keys(self._data['house'])
                select2_results = WebDriverWait(self.driver, self._timeout).until(
                    lambda d: d.find_elements_by_css_selector(
                        f'{self._select2_no_results_selector},{self._select2_result_selector}')
                )
                if 'select2-no-results' not in select2_results[0].get_attribute('class'):
                    select2_results[0].click()
                else:
                    print('Результаты не найдены')
                    select2_input.send_keys(Keys.ESCAPE)
            else:
                return
        else:
            print('Элемент не доступен')
            return

    def _submit(self):
        btn = WebDriverWait(self.driver, self._timeout).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, self._submit_btn_selector))
        )
        btn.click()

    def _search_results(self):
        results = WebDriverWait(self.driver, self._timeout).until(
            ec.presence_of_all_elements_located(
                (By.CSS_SELECTOR, f'{self._search_result_selector},{self._search_no_result_selector}')
            )
        )
        if len(results) == 1:
            if 'register-card' in results[0].get_attribute('class'):
                print('Есть результат')
                return results[0]
            else:
                print('Отсутствуют результаты поиска')
        else:
            print('Много результатов. Нужно уточнить запрос')


    @staticmethod
    def _reduce_string(text):
        return ''.join(c for c in text if c not in [' ', '.', '-'])

    def _wait_for_form(self):
        try:
            WebDriverWait(self.driver, self._timeout).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, self._form_group_selector))
            )
        except TimeoutException:
            self.driver.refresh()

    @staticmethod
    def _config_driver():
        options = Options()
        return webdriver.Chrome(options=options)


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
