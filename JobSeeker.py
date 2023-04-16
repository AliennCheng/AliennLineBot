from selenium import webdriver
from bs4 import BeautifulSoup

class JobSeeker:
    def __init__(self):
        print('Job seeker inited.')

    def seekGoogle(self):
        url = 'https://careers.google.com/jobs/results/?employment_type=FULL_TIME&hl=en&jlo=en-US&location=New%20Taipei%20City,%20Taiwan&location=Taipei,%20Taiwan&q=Software%20Engineer&sort_by=date'

        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        gc_cards = soup.find_all('div', {'class': 'gc-card__container'})

        jobs = []

        for gc_card in gc_cards:
            job = {}
            job['title'] = gc_card.find('h2').text.strip()
            job['qualification'] = gc_card.find_all('div', {'class': 'gc-job-qualifications'})[0].text.strip()
            jobs.append(job)

        print(str(len(jobs)) + ' jobs found.')

        jobs = [x for x in jobs if 'computer science' in x['qualification'].lower() and not 'intern' in x['title'].lower()]

        resp = ''
        for job in jobs[:10]:
            resp += '\nTitle:\n'
            resp += job['title']
            resp += '\nQualification:\n'
            resp += job['qualification']
            resp += '\n\n--------\n'

        return resp

    def seekMicrosoft(self):
        url = 'https://careers.microsoft.com/us/en/search-results?category=Software%20Engineering'

        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(30)

        try:
            # Wait until fieldset clickable
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Employment type')]")))

            # Full-time jobs
            button = driver.find_element_by_xpath("//button[contains(., 'Employment type')]")
            driver.execute_script("arguments[0].click();", button)
            checkbox = driver.find_element_by_xpath("//label[contains(., 'Full-Time')]//input[@type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)

            # Located in Taiwan
            button = driver.find_element_by_xpath("//button[contains(., 'Country')]")
            driver.execute_script("arguments[0].click();", button)
            checkbox = driver.find_element_by_xpath("//label[contains(., 'Taiwan')]//input[@type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)

            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, 'html.parser')
            job_items = soup.find_all('li', {'class': 'jobs-list-item'})

            print(str(len(jobs)) + ' jobs found.')

            resp = ''
            for item in job_items[:10]:
                title = item.find('span', {'class': 'job-title'}).text.strip()
                category = item.find('span', {'class': 'job-category'}).text.strip()
                date = item.find('span', {'class': 'job-date'}).text.strip()

                resp += f'\nTitle:\n{title}'
                resp += f'\nCategory:\n{category}'
                resp += f'\nDate:\n{date}'
                resp += '\n========\n'
                
            return resp

        except:
            driver.quit()
            return 'No result found.\n'