import web_scraping
import data_analysis
import openai
import sys

openai.api_key = ''
studyplan_document = 'document.pdf'


def help(keywords, df):
    print('Available commands are:\n',
          'profile : Plots profiles of study based on most similar courses to keywords.\n',
          'courses : Plots all courses based on similarity to keywords.\n',
          'advice : Gives most similar courses for profile based on keywords.')
    
def advice(keywords, df):
    profile = input('Type your profile: ')
    data_analysis.course_advice(keywords, profile, df = df)    
    
def courses(keywords, df):
    data_analysis.plot_courses_to_likeness(keywords, df = df)

def profile(keywords, df):
    data_analysis.plot_for_profile(keywords, df = df)




print('Please wait...')
web_scraping.write_to_csv(studyplan_document)
keywords = input('Write all your keywords with "," as a separator: ').split(',')
print('Please wait...')
df = data_analysis.likeness_df(keywords)


commands = {'help': help, 'advice' : advice, 'courses': courses, 'profile' : profile,}

while True:
    user_input = input('Type your command: ')
    if user_input == 'quit':
        break
    elif user_input.lower() in commands.keys():
        commands[user_input.lower()](keywords, df.copy())
    else:
        print("Unknown command. Type 'help' for a list of commands.")
    