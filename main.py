# This is the main file for job hunting.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import openai  # Import the OpenAI Python package, assuming you've installed it
import os

def check_database(name):
    with open('save/resume_database.json', 'r') as f:
        database = json.load(f)
    return name in database

def save_to_database(name, resume):
    with open('save/resume_database.json', 'r') as f:
        database = json.load(f)
    database[name] = resume
    with open('save/resume_database.json', 'w') as f:
        json.dump(database, f)

def fetch_resume(name):
    with open('save/resume_database.json', 'r') as f:
        database = json.load(f)
    return database.get(name, None)


def generate_cover_letter(prompt):
    openai.api_key = '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';
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2000,  # Example limit; adjust based on needs
        messages=[
            {"role": "system",
             "content": "You are a professional and helpful assistant that generates cover letters and answers "
                        "questions from the applicant's profile to help the applicant get the job."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def main():
    # Initliase the directory

    if not os.path.exists('save'):
        os.makedirs('save')

    # Initialize the database file if it doesn't exist
    try:
        with open('save/resume_database.json', 'x') as f:
            json.dump({}, f)
    except FileExistsError:
        pass

    is_in_db = input("Is your resume already in our database? (yes/no): ")
    name = ""

    if is_in_db.lower() == 'yes':
        name = input("Enter your name: ")
        if not check_database(name):
            print("Name not found in the database.")
            return
        resume = fetch_resume(name)
    else:
        name = input("Enter your name: ")
        resume = input("Input your resume: ")
        save_to_database(name, resume)

    print("\n")
    job_desc = input("Provide your job description: ")
    print("\n")
    job_title = input("What's the job title?")
    print("\n")
    word_limit = input("Is there a word limit? (Optional): ")
    print("\n")
    special_pref = input("Any special preferences? (Optional): ")
    print("\n")
    prompt1 = f"You are going to generate a cover letter for applicant {name} to apply for {job_title}. Job Description:{job_desc}. Please articulate why the applicant's profile is highly compatible with the company's needs and culture in a compelling and professional tone. Aim to secure the applicant's acceptance. Make your response around {word_limit} words. {special_pref}."
    prompt2 = f"Generate a cover letter that helps applicant {name} in applying for {job_title}. Job Description:{job_desc}. Provide a professional and engaging narrative that underscores the applicant's qualifications and fit for the role. Your primary objective is to help the applicant get accepted for the position. Adhere to a word limit of {word_limit}. {special_pref}."

    cover_letter1 = generate_cover_letter(prompt1)
    cover_letter2 = generate_cover_letter(prompt2)

    print("Version 1:---------------------------------------------------------------", cover_letter1)
    print("=========================================================================")
    print("\nVersion 2:--------------------------------------------------------------", cover_letter2)

    chosen_version = input("Which version do you prefer? (1/2): ")
    # Implement a mechanism to update the ranking algorithm based on the chosen version

    folder_path = f'save/{name}/{job_title}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(f"{folder_path}/cover_letter1.txt",'w') as f1:
        f1.write(cover_letter1)
    with open(f"{folder_path}/cover_letter2.txt",'w') as f2:
        f2.write(cover_letter2)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Xisen!')
    print('Welcome on board this great project for you to hunt down your job!')
    main()
