import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TodoAppSeleniumTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        
        cls.app_url = os.environ.get('APP_URL', 'http://localhost:3000')
        
        cls.wait_for_app()
    
    @classmethod
    def wait_for_app(cls):
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                cls.driver.get(f"{cls.app_url}/health")
                time.sleep(2)
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise Exception(f"App not ready after {max_attempts} attempts: {e}")
                time.sleep(2)
    
    def setUp(self):
        self.driver.get(self.app_url)
        time.sleep(1)
    
    def test_add_todo_functionality(self):
        print("Test Case 1 Add Todo Functionality")
        
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        add_button = self.driver.find_element(By.ID, "add-btn")
        
        test_todo = "Test Todo Item from Selenium"
        
        input_field.clear()
        input_field.send_keys(test_todo)
        add_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "todo-item"))
        )
        
        todo_items = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        self.assertGreater(len(todo_items), 0, "No todo items found after adding")
        
        page_source = self.driver.page_source
        self.assertIn(test_todo, page_source, f"Added todo '{test_todo}' not found on page")
        
        print("Test Case 1 Passed and Todo item was successfully added")
    
    def test_complete_todo_functionality(self):
        print("Test Case 2 Complete Todo Functionality")
        
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        add_button = self.driver.find_element(By.ID, "add-btn")
        
        test_todo = "Todo to be completed"
        input_field.clear()
        input_field.send_keys(test_todo)
        add_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "todo-item"))
        )
        
        complete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-success') and contains(text(), 'Complete')]"))
        )
        complete_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-decoration-line-through"))
        )
        
        completed_todos = self.driver.find_elements(By.CLASS_NAME, "text-decoration-line-through")
        self.assertGreater(len(completed_todos), 0, "No completed todos found")
        
        undo_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-warning') and contains(text(), 'Undo')]")
        self.assertTrue(undo_button.is_displayed(), "Undo button not found for completed todo")
        
        print("Test Case 2 Passed Todo item was successfully marked as complete")
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)