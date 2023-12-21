import csv
import itertools
import PyPDF2
import requests
from bs4 import BeautifulSoup
import re
import os


def web_retriever(CourseCode):
    try:
        page = requests.get("https://www.ntnu.no/studier/emner/" + CourseCode)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find(id = 'course-content-toggler').text, soup.find(id = 'learning-goal-toggler').text
    except:
        print(CourseCode, ' does not exist.')
        return Exception
        
        
        
def extract_course_data(text):
    pattern = r"(\b[A-ZØ]+\d*\b)\s+([A-Z0-9]+)\s+(.*?)(?=\s\(\d+\.?\d*\))"
    match = re.search(pattern, text)
    if match:
        course_code, status, course_name = match.groups()
        return course_code, status, course_name
    else:
        return None, None, None
    
    

def is_course(text):
    course_code, status, course_name = extract_course_data(text)
    if course_code != None:
        return True
    else: return False



def create_directory(directory_path):
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f'Folder {directory_path} was created.')
        else:
            print(f'Folder {directory_path} exists already.')
    except Exception as e:
        print('Error occured when trying to make a folder.', '\n', e)
        
        

def write_to_folder(study_plan = 'document.pdf', folder = 'Courses'):
    #Turn pdf into list of lines
    try:
        reader = PyPDF2.PdfReader(study_plan)
        doc = list(itertools.chain.from_iterable([page.extract_text().split('\n') for page in reader.pages]))
        profile = ''
    except Exception as e:
        print('Error occured when opening document.', '\n', e)
        return
        
    for line in doc:
        #Check for new profile
        if line[:13] == 'Hovedprofil :':
            profile = line[14:]
            create_directory(folder + '/' + profile)
        elif line[:15] == 'Studieretning :':
            profile = line[16:]
            create_directory(folder + '/' + profile)
            
        #File writing
        if is_course(line):
            course_code , status, course_name = extract_course_data(line)
            try:
                f = open(folder + '/' + profile + '/' + course_code + '.txt', 'w', encoding='utf-8')
                info, goals = web_retriever(course_code)
                f.write(line + info + goals)
                f.close()
            except Exception as e:
                print('Something went wrong when writing to file.', '\n', e)     
    print('Done with writing courses to folder.')
    
    


def write_to_csv(study_plan = 'document.pdf', csv_file = 'Courses.csv'):
    #Initialization
    header = ['CourseCode', 'CourseName', 'Status', 'Semester', 'CourseContent', 'CourseGoals', 'Profile']
    try:
        reader = PyPDF2.PdfReader(study_plan)
        doc = list(itertools.chain.from_iterable([page.extract_text().split('\n') for page in reader.pages]))
        file_handler = open(csv_file, 'w', encoding='utf-8')
        writer = csv.writer(file_handler)
        writer.writerow(header)
    except Exception as e:
        print('Error occured when initializing.')
        raise e
    

    profile = ""
    year = 1
    half = 1
    c_course = False
    
    for line in doc:
        #Check for type of line
        if line[:13] == 'Hovedprofil :':
            profile = line[14:]
        elif line[:15] == 'Studieretning :':
            profile = line[16:]
        
        if bool(re.search(r'^(HØST|VÅR) (\d+)\. år$', line)):
            if line[0] == "V":
                half = 0
            else: half = 1
            year = int(re.search(r'^(HØST|VÅR) (\d+)\. år$', line).group(2))
            c_course = False
        elif bool(re.search(r'^Komplement', line)) | c_course:
            c_course = True
            continue
        if 'eksperter i team' in line.lower():
            continue
        
        #Writing to csv
        if is_course(line) :
            try:
                course_code, status, course_name = extract_course_data(line)
                Content, Goals = web_retriever(course_code)
            except Exception as e:
                print('Error occured when reading line:')
                print(line,'\n', e)
                continue
            try:
                data = [course_code, course_name.replace(',', ' '), status, (year*2)-half, Content.replace(',', ' ').replace('\n', ' ') , Goals.replace(',',' ').replace('\n', ' '), profile]
                writer.writerow(data)
            except Exception as e:
                print('Error occured when writing data for line:', line, '\n', e)
                print(Content, Goals)
    print('CSV file successfully written.')
