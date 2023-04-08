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
            
        print('Sending response...')
            
        return resp
        