import pandas as pd
import matplotlib.pyplot as plt
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

def likeness(row, keywords_embedding):
    try:
        response = openai.embeddings.create(
            input = row['CourseContent'] + " " + row['CourseGoals'],
            model = "text-embedding-ada-002"
        )
        #Embedding to numpy array
        row_embedding = response.data[0].embedding

        row_emb_array = np.array(row_embedding).reshape(1, -1)
        keywords_emb_array = np.array(keywords_embedding).reshape(1, -1)

        #Cosine similarity
        likeness_score = cosine_similarity(row_emb_array, keywords_emb_array)[0][0]
        return likeness_score
    except Exception as e:
        print(f"An error occurred: {e} on row {row}")
        return None
    
def likeness_df(keywords : list, csv_file = 'Courses.csv'):
    keywords_embedding_response = openai.embeddings.create(
    input = keywords,
    model = "text-embedding-ada-002"
    )

    keywords_embedding = np.mean([embedding.embedding for embedding in keywords_embedding_response.data], axis=0)
    
    #To save tokens, only embed courses once
    df = pd.read_csv(csv_file, encoding='utf-8')
    df = df.groupby(list(df.columns[:-1]))['Profile'].agg(list).reset_index()
    df['Likeness'] = df.apply(likeness, keywords_embedding = keywords_embedding,axis = 1)
    df = df.explode('Profile').reset_index(drop=True)
    return df

def plot_courses_to_likeness(keywords : list, df : pd.DataFrame, csv_file = 'Courses.csv'):
    if bool(df.empty):
        df = likeness_df(keywords, csv_file)
        
    df.groupby('Profile').apply(lambda x: x.plot(kind='scatter', x='CourseCode', y='Likeness', title=x.name))
    plt.show()
    


def profile_most_alike_courses(keywords : list, df : pd.DataFrame, csv_file = 'Courses.csv'):
    if bool(df.empty):
        df = likeness_df(keywords, csv_file)
    
    df = df.drop(['CourseContent', 'CourseGoals'], axis = 1)
    unique = df.groupby(['Profile', 'Semester'])
    
    myDic = {}
    
    for case in unique:
        caseDF = case[1]
        if case[0][1] == 7 | case[0][1] == 8:
            remaining_slots = 3
        else: remaining_slots = 4
        
        o_courses = caseDF[caseDF['Status'] == 'O']

        #Fill M-Courses
        m_courses = caseDF[caseDF['Status'].str.startswith('M')]
        unique_m_statuses = m_courses['Status'].unique()
        for status in unique_m_statuses:
            max_course = m_courses[m_courses['Status'] == status].nlargest(1, 'Likeness')
            o_courses = pd.concat([o_courses, max_course])
            
        #Fill remaining course slots
        remaining_slots = remaining_slots - len(o_courses)
        if remaining_slots > 0:
            other_courses = caseDF[~caseDF['Status'].isin(['O'] + list(unique_m_statuses))]
            o_courses = pd.concat([o_courses, other_courses.nlargest(remaining_slots, 'Likeness')])

        myDic[case[0]] = o_courses
    return myDic
    
def plot_for_profile(keywords : list, df : pd.DataFrame, csv_file = 'Courses.csv'):
    if bool(df.empty):
        df = likeness_df(keywords, csv_file)

    myDic = profile_most_alike_courses(keywords, df, csv_file)
    
    #Merge dataframes
    grouped_dfs = defaultdict(list)
    for key, df in myDic.items():
        grouped_dfs[key[0]].append(df)
        
    merged_dfs = {group: pd.concat(dfs) for group, dfs in grouped_dfs.items()}
    
    #Plot desired data
    profiles = merged_dfs.keys()
    mean_values = [subdf['Likeness'].mean() for subdf in merged_dfs.values()]
        
    plt.bar(profiles, mean_values)
    plt.show() 
    

def course_advice(keywords : list, profile : str, df : pd.DataFrame, csv_file = 'Courses.csv'):
    if bool(df.empty):
        df = likeness_df(keywords, csv_file)
    
    myDic = profile_most_alike_courses(keywords, df, csv_file)
    
    if profile not in [values[0] for values in myDic.keys()]:
        print('Profile does not exist.')
        return
        
    for key in myDic:
        if key[0] == profile:
            print(key)
            print(myDic.get(key))
