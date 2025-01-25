# RoundZer0

### Revolutionizing the Hiring Process with AI-Powered Interviews
RoundZer0 is a platform designed to transform the hiring process by using AI for initial candidate interviews. The goal is to create a fair and unbiased recruitment system that evaluates candidates based on their skills and potential, rather than prior commercial experience.

### Why RoundZer0?
Traditional hiring processes often overlook talented individuals due to biases or a lack of formal experience. RoundZer0 tackles this issue by conducting AI-driven "Round Zero" interviews tailored to specific job roles. These interviews ensure every candidate has an equal opportunity to demonstrate their abilities, leveling the playing field for all applicants.

### Benefits for Employers
RoundZer0 simplifies recruitment by providing pre-screened candidates evaluated through AI-powered interviews. This saves time and resources, allowing recruiters to focus on meaningful face-to-face interactions in later interview stages.

### Vision
The vision behind RoundZer0 is to build a hiring process that prioritizes talent, inclusivity, and efficiency. By fostering a process driven by potential rather than resumes, this project aims to make job opportunities accessible to everyone and help employers identify the best talent for their teams.


#### [Visit RoundZer0](https://roundzero-2ed378b75104.herokuapp.com/)


![Image](https://github.com/user-attachments/assets/dc813460-34de-484a-83ec-7ddc58a83478)



## Table of Contents

- [User Experience](#user-experience)
- [Features](#features)
- [Credits](#credits)


## User Experience

### Ideal User Demographic

**RoundZer0 is ideal for:**

- **Employers:**
  - Recruiters and hiring managers seeking an efficient, unbiased way to screen candidates.
  - Companies looking to save time and resources during the initial stages of recruitment.
  - Organizations striving to foster inclusivity and diversity in their hiring process.


- **Candidates:**
  - Job seekers eager to prove their skills, regardless of commercial experience.
  - Individuals looking for a fair and objective assessment of their abilities.
  - Professionals transitioning into new industries or roles.


- **Goals for Employers:**
  - **As an employer using RoundZer0, I want to:**
    - Quickly set up and customize AI-driven interviews for specific roles.
    - Save time by automating the initial candidate screening process.
    - Access detailed, unbiased reports on candidate performance.
    - Focus on interviewing top candidates identified through the AI assessments.


- **Goals for Candidates:**
  - **As a candidate participating in RoundZer0, I want to:**
    - Easily understand how to complete the AI interview process.
    - Showcase my skills and potential without being judged by my resume alone.
    - Receive clear instructions and feedback throughout the interview experience.
    - Feel confident that the assessment process is fair and unbiased.


### User Stories:
To understand the needs and goals of both Employers and Candidates, I have outlined detailed User Stories that guided the development of RoundZer0.

[View User Stories Here](https://github.com/users/tibssy/projects/3/views/1?groupedBy%5BcolumnId%5D=Milestone)


## Features

### Site Navigation

The site features a fixed-position navigation bar at the top of the page, ensuring users can easily access key areas of the platform without needing to scroll back to the top. The navigation bar adapts based on the type of user logged in, ensuring a tailored experience.

- **For Employers:**
  - **Dropdown Menu:**
    - **Profile:** Access and manage your personal and company information.
    - **My Jobs:** View and manage job postings, track candidates, and monitor ongoing interviews.
  - **For Candidates:**
    - **Profile:** Edit personal details and preferences.
    - **History:** Review your interview history, including completed AI interviews and their outcomes.
  - **Unregistered user / Signed-Out user:**
    - **Register:** Register as a candidate or employer to access the platform.
    - **Login:** Existing users can log in to their accounts.

![Image](https://github.com/user-attachments/assets/64aab1da-57a0-495d-bd54-5e6dfaf58ea7)
![Image](https://github.com/user-attachments/assets/1aeebf3b-0cd4-48ad-b9b7-35923cf19fce)
The navigation bar ensures a user-friendly experience, allowing users to focus on their specific needs without clutter or confusion. It provides quick access to the platform's core functionalities, enhancing usability and efficiency.


### Search and Sort Feature

**Search Bar:**
The platform includes a prominently placed search bar that allows users to filter job posts quickly and efficiently. This feature is designed for both registered and unregistered users, ensuring easy access to job opportunities.
  - Users can input keywords such as job title, required skills, or industry to narrow down the list of available positions.
  - The search is case-insensitive and provides real-time suggestions as users type.

**Dropdown for Sorting:**
To further enhance usability, a dropdown menu is included next to the search bar, enabling users to sort job postings based on specific criteria.
  - **Posted Date:** Displays the most recently/oldest posted jobs first.
  - **Company Name:** Alphabetically sorts job postings by company name for easier navigation.
  - **Location:** Groups job postings by location for users targeting specific regions.

![Image](https://github.com/user-attachments/assets/977ed31a-7ee4-4991-be92-2b33d71e299b)
This combined Search and Sort Feature makes it simple for users to find the most relevant job opportunities quickly. By providing customizable filters and sorting options, the platform ensures an efficient and intuitive job-seeking experience.


### Interview History Feature
The Interview History feature provides candidates with a comprehensive and organized view of their past interviews. This functionality ensures transparency and allows candidates to track their performance over time.

- **List of Interviewed Positions:**
  - Displays a list of all job positions the candidate has interviewed for.
  - Each entry includes the job title and collapsible details for a more streamlined view.
- **Brief Feedback:**
  - For each interview, brief feedback is provided, offering constructive insights on the candidate's performance.
  - Feedback is sent immediately after the AI-driven interview, ensuring prompt guidance.
- **Timestamp and Company Details:**
  - Includes the date and time of the interview, as well as the company's name, helping candidates keep track of their application timeline.
- **Delete Option:**
  - Candidates have the option to delete any interview history entry. This gives users control over managing their records and maintaining a clean history view if desired.

![Image](https://github.com/user-attachments/assets/feb109d6-5486-45cc-b5fa-fa2fcf8beac8)
This feature promotes self-improvement by offering valuable feedback and ensures candidates stay informed about their past interactions.


### Profile Feature
The Profile feature allows candidates to create and manage their professional profiles, ensuring they present their skills and qualifications effectively during the hiring process.
- **Candidates can set up their profile with the following details:**
  - **Name:** Displayed during interviews and visible to employers after the interview.
  - **Executive Summary:** A brief personal overview or statement summarizing the candidate's professional background.
  - **Key Skills:** A list of the candidate's core competencies and strengths to highlight their expertise.
- **Interviewer Access:**
  - During AI-driven interviews, the profile is visible to the AI interviewer, allowing tailored questions based on the candidate’s information.
- **Employer Access Post-Interview:**
  - After the interview, the employer who posted the job can view the candidate’s profile, including contact details (email address and phone number), to facilitate further communication.
- **Profile Management:**
  - **Edit Profile:** Candidates can update their profile details at any time to reflect changes in their skills or professional summary.
  - **Account Deletion:** Candidates can permanently delete their accounts, ensuring full control over their data.

![Image](https://github.com/user-attachments/assets/9058714c-8928-4461-bc0a-c7a73226be3d)
This feature empowers candidates to present their best selves while ensuring employers have access to key details to make informed hiring decisions.


### Employer's My Jobs Section
The My Jobs section is a dedicated feature for employers, offering robust tools to manage job postings and oversee applications efficiently.
- **Job Management:**
  - Create: Employers can easily post new job openings by providing necessary details such as job title, description, location, and required skills.
  - Read: View a comprehensive list of all active job postings, complete with their details.
  - Update: Modify existing job postings to reflect changes in requirements or additional information.
  - Delete: Remove job postings that are no longer relevant or filled.

![Image](https://github.com/user-attachments/assets/2efc3f1c-9364-4551-ab3f-1268b2941f73)

- **Interview Customization:**
  - Set Interview Duration: Employers can define the length of interviews for each job posting.
  - Add Custom Questions: Tailor the interview process by adding specific questions relevant to the job role. These questions will be used by the AI during the candidate interview.

![Image](https://github.com/user-attachments/assets/cc326e34-e85d-4049-a643-168a2dbbb4a4)

- **Application Overview:**
  - View all candidate applications submitted for each job posting.
  - Access detailed candidate profiles, including interview results, performance feedback, and contact information.
  - Manage applications efficiently to identify and shortlist top talent.

![Image](https://github.com/user-attachments/assets/833e0733-32aa-4cc6-a440-97205a1c64be)


## Credits

- **Django Channels Documentation**
  - [Django Channels](https://channels.readthedocs.io) Used for WebSockets.
- **Openai Documentation**
  - [OpenAI](https://platform.openai.com/docs/overview) Used for Speech To Text