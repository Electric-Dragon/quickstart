from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googlesearch import search

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly','https://www.googleapis.com/auth/classroom.coursework.me','https://www.googleapis.com/auth/classroom.coursework.students']

def confirmation(title):
    response = 'something'
    while response == 'something':
        response = str(input('Are you okay with the search term to be -  ' + title + '? (y/n)'))
    if response == 'y' or response == 'Y':
        return True
    elif response == 'n' or response == 'N':
        return False
    else:
        response = 'something'
        pass

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    coursesNamesList = []
    coursesIdsList = []
    assignmentsTitlesList = []
    assignmentsIdsList = []
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print()
        print('Courses:')
        for course in courses:
            print(course['name'] + ' - ' + course['descriptionHeading'])
            coursesNamesList.append(course['name'])
            coursesIdsList.append(course['id'])

        courseChoice = int(input('Choose a course (1-' + str(len(coursesIdsList)) + ')')) -1
        if courseChoice >= 0 and courseChoice < len(coursesIdsList):

            results = service.courses().courseWork().list(courseId=coursesIdsList[courseChoice]).execute()
            assignments = results.get('courseWork')

            if not assignments:
                print('No assignments found.')
            else:
                print()
                print('Assignments:')
                for assignment in assignments:
                    print(assignment['title'])
                    assignmentsTitlesList.append(assignment['title'])
                    assignmentsIdsList.append(assignment['id'])

                assignmentChoice = int(input('Choose an assignment (1-' + str(len(assignmentsIdsList)) + ')')) -1
                if assignmentChoice >=0 and assignmentChoice < len(assignmentsIdsList):

                    result = confirmation(assignmentsTitlesList[assignmentChoice])

                    if result:
                        for i in search(assignmentsTitlesList[assignmentChoice], tld="co.in", num=10, stop=10, pause=2):
                            print(i)
                    else:
                        searchTerm = input('Enter your preferred search term -   ')
                        for i in search(assignmentsTitlesList[assignmentChoice], tld="co.in", num=10, stop=10, pause=2):
                            print(i)


if __name__ == '__main__':
    main()


# MYP 4 - 99635970062
# MYP 4 - 90520511569
# Design_MYP 4_2020-2021 - 68164076693
