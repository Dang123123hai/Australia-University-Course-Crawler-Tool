import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options

# I use both beautifuSlSoup and Selenium for data crawling because the main data from the website UAC
# is written by java Script which is unable to crawling using BeautifulSoup. The reason i use Selenium
# is to interpret so Beautiful Soup can parse.
def course_tracking(mode, course):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    DRIVER_PATH = '/path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
    # create list of course info:
    institution, course_tt, campus, lowest_atar, median_atar, highest_atar, lowest_srank, median_srank, highest_srank, min_srank, g_rank, assumed_knowledge, rcm_studies = [
        [] for i in range(13)]
    # Change the course, mode input for easier on google searching
    course = course.replace(' ', '+')
    url = 'https://www.google.com/search?q="uac"+course+search+' + mode + '+of' + '+' + course
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Parse the link to find the link have info about the uac website course and mode
    soup_link_course = soup.find_all("div", {'class': 'egMi0 kCrYT'})
    link_course = []
    for i in soup_link_course:
        link = i.find('a').get('href')
        link_course.append(link)
    c = []
    for i in link_course:
        try:
            j = i.replace('/url?q=', '')
            index = j.index('html')
            result = j[:index + len('html')]
            c.append(result)
        except ValueError:
            pass
    c1 = [i for i in c if i.startswith('https://www.uac.edu.au/')]
    for school_link in c1:
        try:
            # Run driver using selenium:
            driver.get(school_link)
            # Read the page with BeautifulSoup through Selenium
            soup1 = BeautifulSoup(driver.page_source, "lxml")
            # Institution name
            institution_name = soup1.find('p', {'class': 'institution-name'}).get_text()
            # Course title
            course_title = soup1.find('h1', {'class': "course-title"}).get_text()

            # School and course campus
            campuses_find = soup1.find_all('span', {'class': 'course-location-campus mt-0 mob-table-cell ng-binding'})
            campu = ' ,'.join((i.get_text()) for i in campuses_find)

            # Filter for the admission criteria data
            soup_admission = soup1.find('div', {'id': 'admission'})
            # Assumed Knowledge
            assumed_knowledge_1 = soup_admission.find(lambda tag: tag.name == 'p' and (
                        tag.find('strong', text='Assumed knowledge:') or tag.find('strong',
                                                                                  text='Assumed knowledge: ') is not None))

            try:
                assume_knowledge_2 = assumed_knowledge_1.get_text(strip=True).replace('Assumed knowledge:', '')
            except AttributeError:
                assume_knowledge_2 = None
            # Reccomend Study
            rcm_studies_1 = soup_admission.find(lambda tag: tag.name == 'p' and (
                        tag.find('strong', text='Recommended studies:') or tag.find('strong',
                                                                                    text='Recommended studies: ') is not None))

            try:
                rcm_studies_2 = rcm_studies_1.get_text(strip=True).replace('Recommended studies:', '')
            except AttributeError:
                rcm_studies_2 = None
            # Gurantee Rank
            g_srank_1 = soup_admission.find(
                lambda tag: tag.name == 'p' and tag.find('strong', text='Guaranteed selection rank:') is not None)

            try:
                g_srank_2 = g_srank_1.get_text(strip=True).replace('Guaranteed selection rank:', '')
            except AttributeError:
                g_srank_2 = None
            # Minimum selection rank
            min_srank_1 = soup_admission.find(
                lambda tag: tag.name == 'p' and tag.find('strong', text='Minimum selection rank:') is not None)

            try:
                min_srank_2 = min_srank_1.get_text(strip=True).replace('Minimum selection rank:', '')
            except AttributeError:
                min_srank_2 = None

            # ATAR:
            try:
                atar_data_table = soup1.find('table', {'id': 'atarDataTable'}).find_all('td')
                low_atar, med_atar, high_atar = [atar_data_table[i].get_text() for i in range(3)]
            except AttributeError:
                low_atar, med_atar, high_atar = [None for i in range(3)]

            # Selection rank:
            try:
                atar_data_table = soup1.find('table', {'id': 'atarDataTable'}).find_all('td')
                low_srank, med_srank, high_srank = [atar_data_table[i].get_text() for i in range(3, 6)]
            except AttributeError:
                low_srank, med_srank, high_srank = [None for i in range(3)]

            # Append the list
            lowest_atar.append(low_atar)
            median_atar.append(med_atar)
            highest_atar.append(high_atar)
            lowest_srank.append(low_srank)
            median_srank.append(med_srank)
            highest_srank.append(high_srank)
            min_srank.append(min_srank_2[:5] if min_srank_2 != None else min_srank_2)
            g_rank.append(g_srank_2)
            assumed_knowledge.append(assume_knowledge_2)
            rcm_studies.append(rcm_studies_2)
            institution.append(institution_name)
            course_tt.append(course_title)
            campus.append(campu)
        except AttributeError:
            pass

    for i in range(100):
        e = []

        # Access to the next page of Google
        link = soup.find('a', attrs={'aria-label': 'Next page'})
        href = link['href']
        url = 'https://www.google.com' + href
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup_link_course = soup.find_all("div", {'class': 'egMi0 kCrYT'})
        link_course = []
        for i in soup_link_course:
            link = i.find('a').get('href')
            link_course.append(link)
        c = []
        for i in link_course:
            try:
                j = i.replace('/url?q=', '')
                index = j.index('html')
                result = j[:index + len('html')]
                c.append(result)
            except ValueError:
                pass
        c1 = [i for i in c if i.startswith('https://www.uac.edu.au/')]
        for school_link in c1:
            try:
                # Run driver using selenium:
                driver.get(school_link)
                # Read the page with BeautifulSoup through Selenium
                soup1 = BeautifulSoup(driver.page_source, "lxml")
                # Institution name
                institution_name = soup1.find('p', {'class': 'institution-name'}).get_text()
                # Course title
                course_title = soup1.find('h1', {'class': "course-title"}).get_text()

                # School and course campus
                campuses_find = soup1.find_all('span',
                                               {'class': 'course-location-campus mt-0 mob-table-cell ng-binding'})
                campu = ' ,'.join((i.get_text()) for i in campuses_find)

                # Filter for the admission criteria data
                soup_admission = soup1.find('div', {'id': 'admission'})
                # Assumed Knowledge
                assumed_knowledge_1 = soup_admission.find(lambda tag: tag.name == 'p' and (
                            tag.find('strong', text='Assumed knowledge:') or tag.find('strong',
                                                                                      text='Assumed knowledge: ') is not None))

                try:
                    assume_knowledge_2 = assumed_knowledge_1.get_text(strip=True).replace('Assumed knowledge:', '')
                except AttributeError:
                    assume_knowledge_2 = None
                # Reccomend Study
                rcm_studies_1 = soup_admission.find(lambda tag: tag.name == 'p' and (
                            tag.find('strong', text='Recommended studies:') or tag.find('strong',
                                                                                        text='Recommended studies: ') is not None))

                try:
                    rcm_studies_2 = rcm_studies_1.get_text(strip=True).replace('Recommended studies:', '')
                except AttributeError:
                    rcm_studies_2 = None
                # Gurantee Rank
                g_srank_1 = soup_admission.find(
                    lambda tag: tag.name == 'p' and tag.find('strong', text='Guaranteed selection rank:') is not None)

                try:
                    g_srank_2 = g_srank_1.get_text(strip=True).replace('Guaranteed selection rank:', '')
                except AttributeError:
                    g_srank_2 = None
                # Minimum selection rank
                min_srank_1 = soup_admission.find(
                    lambda tag: tag.name == 'p' and tag.find('strong', text='Minimum selection rank:') is not None)

                try:
                    min_srank_2 = min_srank_1.get_text(strip=True).replace('Minimum selection rank:', '')
                except AttributeError:
                    min_srank_2 = None

                # Get Atar table:
                atar_data_table = soup1.find('table', {'id': 'atarDataTable'}).find_all('td')

                # ATAR:
                try:
                    low_atar, med_atar, high_atar = [atar_data_table[i].get_text() for i in range(3)]
                except AttributeError:
                    low_atar, med_atar, high_atar = [None for i in range(3)]

                # Selection rank:
                try:
                    low_srank, med_srank, high_srank = [atar_data_table[i].get_text() for i in range(3, 6)]
                except AttributeError:
                    low_srank, med_srank, high_srank = [None for i in range(3)]

                # Append the list
                lowest_atar.append(low_atar)
                median_atar.append(med_atar)
                highest_atar.append(high_atar)
                lowest_srank.append(low_srank)
                median_srank.append(med_srank)
                highest_srank.append(high_srank)
                min_srank.append(min_srank_2[:5] if min_srank_2 != None else min_srank_2)
                g_rank.append(g_srank_2)
                assumed_knowledge.append(assume_knowledge_2)
                rcm_studies.append(rcm_studies_2)
                institution.append(institution_name)
                course_tt.append(course_title)
                campus.append(campu)
            except AttributeError:
                pass

        if e == []:
            break

    df = pd.DataFrame(list(
        zip(institution, course_tt, campus, lowest_atar, median_atar, highest_atar, lowest_srank, median_srank,
            highest_srank, min_srank, g_rank, assumed_knowledge, rcm_studies)),
                      columns=['Institution', 'Course name', 'Campus', 'Lowest ATAR', 'Median ATAR', 'Highest ATAR',
                               'Lowest selection rank', 'Median selection rank', 'Highest selection rank',
                               'Minimum selection rank', 'Guranteed selection rank', 'Assumed knowledge',
                               'Recommend studies'])
    driver.quit()
    return df.sort_values(by=['Institution','Course name']).drop_duplicates(subset=['Institution','Course name']).reset_index(drop=True)