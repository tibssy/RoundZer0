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
- [Design](#design)
- [Technical Details / Solutions](#technical-details--solutions)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
- [Acknowledgments](#acknowledgments)

---

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

---

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

![Image](https://github.com/user-attachments/assets/e3a0f31b-4514-4e39-be18-b0f28ae25c6c)
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

This feature empowers employers with flexibility and control, ensuring a smooth and customized hiring process tailored to their organization’s needs.


### Interview
The Interview Page is designed to provide candidates with a familiar and comfortable environment during the AI-driven interview process. The layout is simple yet efficient, ensuring a seamless experience for both candidates and employers.

- **User-Friendly Layout:**
  - Familiar and intuitive design to keep candidates focused on the interview.
  - Includes a Camera On/Off Toggle for user privacy and comfort.
  - A prominent End Interview Button for candidates to finish the interview if necessary.
- **AI Interviewers:**
  - A diverse pool of 20 AI interviewers: 10 male and 10 female.
  - Each interviewer is equipped with a unique voice, adding a personal touch to the interview experience.
  - The interviewer is chosen randomly or based on predefined criteria to simulate real-world interviews.
- **Conversation Logging and Timestamping:**
  - The entire interview conversation is saved in text format for processing and review.
  - Each candidate’s response is timestamped to monitor the interview duration and ensure it stays within the employer-defined time limit.
  - The AI interviewer can greet the candidate based on the time of day.
- **Feedback Generation:**
  - A brief feedback summary is immediately sent to the candidate at the end of the interview.
  - A detailed feedback report is sent to the employer for review.
  - Employers testing their own job posts can simulate an interview without receiving feedback from the AI.
- **Strict Topic Adherence:**
  - The interviewer strictly adheres to the job interview topics and does not allow the candidate to stray into unrelated subjects, ensuring the conversation remains professional and focused.
- **Interview Restrictions:**
  - Candidates can have only one interview per job post, ensuring no additional opportunities to repeat the process.

![Image](https://github.com/user-attachments/assets/5fda61d0-a9f8-41c9-b2e7-63c59d86cc3f)

This feature adds a layer of human-like interaction and thoughtfulness while maintaining structure and efficiency. It reflects the importance of personalization and professionalism in the candidate experience.


### Notifications

- **Modal Notifications:**
  - When an action requires user confirmation (e.g., deleting a profile, interview history, or job post), a modal popup notification appears.
  - These modals ensure the user is fully aware of the consequences before proceeding with the action.
  - Modal notifications are designed with clear prompts, such as "Are you sure you want to delete this item?" followed by confirmation and cancel options.
- **Alert Notifications:**
  - Alerts are displayed for each step when a modification is successfully saved to the database.
  - Alerts are visually distinct, with styles that indicate success, error, or warning, ensuring clarity for users.
  - Auto-Close Feature: Alert notifications automatically close after 3 seconds, providing seamless feedback without disrupting the user experience.

![Image](https://github.com/user-attachments/assets/b146314a-6f4a-465e-8f57-ddbc79f1701c)

This notification system enhances usability by keeping users informed and guiding them through critical interactions.

---

## Design

### Imagery
The visual design of the web application leverages a modern and professional aesthetic to enhance usability and appeal. Key elements of the imagery include:

### Color Palette
- **Color Palette**
  - Dark Blue (#15354b): Used for navigation bars, headers, and key UI elements to create a professional tone and provide contrast.
  - Orange (#ff8800): Applied to active icons and call-to-action elements, drawing attention to interactive features.
- **Background**
  - Light gray blue gradient image create a neutral and clean backdrop that emphasizes content and reduces visual clutter.
### Icons and Visual Cues
- **Bootstrap Icons:**
  - Icons from the Bootstrap library are seamlessly integrated throughout the application for clarity and consistency.
  - Home, Jobs, About, Profile, and Logout are represented with intuitive icons for quick identification.
  - Icons are consistently colored in orange to create a cohesive design and highlight functionality.
### Typography
- **Font:**
  - The application uses Roboto Condensed, a modern sans-serif typeface.
  - The font’s narrow letterforms and clean design ensure readability and enhance the app's professional appearance.
  - Job titles, candidate names, and section headers are bolded and slightly larger to ensure focus.
  - Subheadings and body text remain lightweight and consistent for clarity.
### Card-Based Layout
- **Design Features:**
  - Rounded edges create a visually appealing and approachable look.
  - Subtle shadows are applied to separate cards from the background and add depth.
  - Consistent margins and padding provide a balanced and structured layout.

The combination of Roboto Condensed, Bootstrap Icons, and a cohesive card-based layout ensures a minimalist and user-focused design. This approach avoids unnecessary clutter, keeping attention on job postings and candidate evaluations.

---

## Technical Details / Solutions

### AI Voice-Based Interviewer
To ensure an enjoyable and low-latency experience for the AI interviewer, I focused on developing this feature first, as it was both the most challenging and critical component of the project.

**Frontend Implementation**
  - **WebSocket for Low Latency:**
    - WebSocket was chosen to connect the frontend and backend, significantly reducing latency by eliminating the need for repeated handshakes.
    - The WebSocket connection is established at the start of the interview, ensuring efficient data transfer throughout the session.

  
  - **Microphone Activation via WebRTC:**
    - The microphone is activated and managed by WebRTC to capture the audio seamlessly.
    - RMS (Root Mean Square) levels are calculated on the frontend to determine when the user is speaking.
      - Threshold Logic: When the RMS level reaches 0.01, recording begins.
      - If the RMS level drops below the threshold, the system waits for a 2-second silence delay before stopping the recording.
    - Audio is sent to the backend immediately after this 2-second delay.


  - **Audio Size Testing:**
    - Through testing, I found that 1 minute of audio equals approximately 1 MB in size on my setup, ensuring efficient transmission over WebSocket.

**Backend Implementation**
  - **Speech-to-Text Processing:**
    - Upon receiving the audio, the backend sends it to the OpenAI Whisper API (via OpenAI Python library) for transcription.
    - Users are differentiated by type:
      - **Regular users:** Access transcription through Groq.
      - **Staff members:** Access transcription through OpenAI.


  - **AI Response Generation:**
    - Transcribed text is processed using either Groq (LLaMA 3.3 model) or OpenAI (GPT-4o-mini model) via the OpenAI library.
    - Job description and user profile data are embedded into the system message to ensure responses are tailored to the interview context.
    - **Streaming Responses:**
      - The stream=True parameter in the chat completion request enables the backend to send responses as a stream of text chunks.
      - A Python generator is used to process the stream and construct sentences as soon as the first sentence is received.


  - **Text-to-Speech Conversion:**
    - Sentences are sent one by one to the Edge-TTS API for text-to-speech conversion.
    - The generated audio is transmitted back to the frontend sentence by sentence.

**Frontend Playback**
  - **Audio Queue Management:**
    - Received audio chunks are stored in an ***audioQueue*** array.
    - Playback starts as soon as the first audio chunk is received, continuing sequentially until the queue is empty.
    - Once playback finishes and no audio remains in the queue, the system resumes listening for microphone RMS levels, restarting the cycle.

**Full Cycle Workflow**
1. **Audio Capture:** Microphone listens for RMS level changes and records user input.
2. **Audio Transmission:** After a 2-second silence delay, audio is sent to the backend via WebSocket.
3. **Transcription:** The backend transcribes the audio to text using Whisper.
4. **Response Generation:** AI processes the transcription and generates a response.
5. **Audio Playback:** The response is converted to speech and sent to the frontend for playback.
6. **Repeat:** The cycle continues until the interview is manually closed by the user.

![Image](https://github.com/user-attachments/assets/b5bb0453-dbb4-4396-a778-d9a0a6681599)


### Model Relationships

**Candidate Profile Relationships**
  - **Relationship with User:**
    - OneToOneField: Each candidate is linked to exactly one User instance. This ensures that every candidate has a unique user account.
    - Cascade Delete: When the linked User instance is deleted, the corresponding Candidate profile is also removed.
  - **Relationship with InterviewHistory:**
    - ForeignKey: Each candidate can have multiple interview records.
    - Cascade Delete: Deleting a Candidate will delete all related interview histories.

**Interview History Relationships**
  - **Relationship with Candidate:**
    - Each interview record belongs to one candidate (ForeignKey relationship).

**Employer Profile Relationships**
  - **Relationship with User:**
    - OneToOneField: Each employer is linked to exactly one User instance.
    - Cascade Delete: Deleting a User instance will delete the associated employer profile.
  - **Relationship with InterviewFeedback:**
    - Employers can provide feedback on candidates through the InterviewFeedback model.

**JobPost Relationships**
  - **Relationship with User (Author/Employer):**
    - ForeignKey: Each job post is associated with one User (employer) instance.
    - Cascade Delete: Deleting a User will remove all job posts created by that user.
  - **Relationship with EvaluationRubric:**
    - ForeignKey: A job post can have multiple associated rubrics for candidate evaluation.
  - **Relationship with InterviewFeedback:**
    - ForeignKey: Each feedback is tied to a specific job post.

**Interview Feedback Relationships**
  - **Relationship with JobPost:**
    - ForeignKey: Feedback is linked to one job post.
    - Cascade Delete: If a job post is deleted, all associated feedback is removed.
  - **Relationship with Candidate:**
    - ForeignKey: Feedback is linked to one candidate.
    - Cascade Delete: Deleting a candidate removes all feedback related to them.

**Evaluation Rubric Relationships**
  - **Relationship with JobPost:**
    - ForeignKey: A rubric can be optionally tied to a job post.
    - Nullability: Rubrics can exist without being tied to a specific job post (null=True, blank=True).

![Image](https://github.com/user-attachments/assets/e4e92879-039f-4730-9ebe-6f5ad479a379)

---

## Testing
For the testing phase, each app will be thoroughly evaluated to ensure quality and performance. I will use Lighthouse to assess mobile and desktop performance, accessibility, and SEO metrics. Each app will also be checked using pylint-django to identify and resolve any coding standard issues. Additionally, I will validate the HTML of the apps using the W3C HTML Validator (validator.w3.org) to ensure compliance with web standards. Finally, I will run the unit tests I have written for each app to validate their functionality and ensure that all components work as intended. This comprehensive testing process will ensure robust and reliable applications.

### Home App:

![Image](https://github.com/user-attachments/assets/232f4795-85e8-43fe-a8e6-4265cde910ca)
![Image](https://github.com/user-attachments/assets/b6429771-7143-472a-af63-cb2643cf585b)
![Image](https://github.com/user-attachments/assets/997ea51d-d847-4fdf-97d3-4bee651cf726)

### JobPosts App:

![Image](https://github.com/user-attachments/assets/4671e353-290b-4d10-a7dc-6e9268bb44e8)
![Image](https://github.com/user-attachments/assets/5e72e88c-5c0d-4ddf-a622-146cb923158e)
![Image](https://github.com/user-attachments/assets/6637f725-603e-4d91-985c-a033c0a6a7f8)

### About App:

![Image](https://github.com/user-attachments/assets/5a636046-84e8-4e57-b846-62241fa7a93d)
![Image](https://github.com/user-attachments/assets/72abfdc6-fc6a-4730-8dab-4ea854e9344b)
![Image](https://github.com/user-attachments/assets/39c3a9b0-15c6-46ac-b666-9aa1ea27aac0)

### Profile Page:

![Image](https://github.com/user-attachments/assets/928b8d86-4425-408c-88a9-556feeb48b0a)

### Edit Profile Page:

![Image](https://github.com/user-attachments/assets/e8d4b09d-35c0-4400-a6be-ca06314fd754)

### Interview History Page:

![Image](https://github.com/user-attachments/assets/70a2caed-4cc6-4467-8835-cbfe63393813)

### SignUp Page:

![Image](https://github.com/user-attachments/assets/1402e43b-2dfe-434a-a6b4-ac848e44f560)

### SignIn Page:

![Image](https://github.com/user-attachments/assets/a50c3181-7953-4a8f-af6b-296fcb59c264)

### SignOut Page:

![Image](https://github.com/user-attachments/assets/81ac2455-ff92-4851-aaf3-41be6e6527ed)

### My Jobs Page:

![Image](https://github.com/user-attachments/assets/587dc308-6e5f-48be-a3e7-0df71581703d)

### Job Applications Page:

![Image](https://github.com/user-attachments/assets/1e3f8dfd-d768-43b0-bc29-852ddc669fe9)

During the testing phase, I used the W3C HTML Validator (https://validator.w3.org) to check the HTML of my applications for compliance with web standards. However, testing certain pages was not possible as they require user login to access. For CSS validation, I used the W3C CSS Validator (https://jigsaw.w3.org). While testing, I encountered some errors due to the use of CSS nesting, which is not yet fully supported in the validator. Additionally, I received an error for the font-optical-sizing: auto; property, even though it was implemented following examples provided in the official Google Fonts documentation. Despite these validation issues, the property functions correctly across modern browsers, as intended.

All JavaScript files were tested using JSHint (https://jshint.com/) with the configurations /* jshint esversion: 6 */ and /* jshint esversion: 8 */. This ensured compatibility and adherence to ES6 and ES8 standards, with no significant issues detected during testing.

---

## Deployment

For deployment, this project leverages Heroku's platform, which makes it simple to host and run terminal-based Python applications in the cloud. Here’s a guide for manually deploying your project to Heroku using a GitHub repository:

### Deployment Steps:

- **1. Create a Heroku Account**
    - Visit [Heroku](https://dashboard.heroku.com/) and sign up for an account.

- **2. Create a New App**
    - Go to the Heroku dashboard and click **new**.
    - On the dropdown click **Create new app**.
    - Provide a unique app name and select your region then click **Create app**.

- **3. Connect to GitHub**
    - In the **Deploy** tab, choose **GitHub** as the deployment method.
    - Search for your repository and connect it to Heroku.

- **4. Manual or Automatic Deploy**
    - Enable **Automatic Deploys** for Heroku to update the app with every push to GitHub, or use the **Manual Deploy** option to deploy the main branch manually.

This deployment process ensures your application runs smoothly in a web-based environment hosted on Heroku.

---

## Credits

- **Django Channels Documentation**
  - [Django Channels](https://channels.readthedocs.io) Used for WebSockets.
- **Openai Documentation**
  - [OpenAI](https://platform.openai.com/docs/overview) Used for Speech To Text and chat response generation.
- **Groq Documentation**
  - [Groq Cloud](https://console.groq.com/docs/overview) Used for Speech To Text and chat response generation.
- **Image Generation**
  - [Leonardo AI](https://app.leonardo.ai) Used for interviewer generation in Disney Pixar style.
- **Video Generation**
  - [Pixverse AI](https://app.pixverse.ai) Used for image-to-video generation to animate interviewers.
- **Image Upscaling**
  - [Upscayl Desktop](https://www.upscayl.org/) Utilized for upscaling images to higher resolutions.
- **Image Editing and Conversion**
  - [GIMP - GNU Image Manipulation Program](https://www.gimp.org/) Open-source tool for editing images and converting them to WebP and many other formats.
- **Version Control**
  - [GitHub](https://github.com) Used for version control and repository management.
- **Integrated Development Environment (IDE)**
  - [Pycharm Community Edition](https://www.jetbrains.com/pycharm/), IDE used for coding and development.
- **Bootstrap**
  - [Bootstrap](https://getbootstrap.com/), Used bootstrap classes to simplify development.
- **Icons**
  - [Bootstrap Icons](https://icons.getbootstrap.com/) Free, high quality, open source icon library with over 2,000 icons.
- **Fonts**
  - [Google Fonts](https://fonts.google.com) Used Roboto Condensed font family for this project.
- **StackOverflow**
  - [StackOverflow](https://stackoverflow.com) Used to find solutions for specific coding issues, like rotating a 2D array in JavaScript.
- **W3Schools**
  - [W3Schools](https://www.w3schools.com/css/) Used to find some design solutions, like a toggle switch.
- **ChatGPT**
  - [ChatGPT](https://chatgpt.com/) Used to generate the text content of my project, also used for generating fixtures to create mock data for job posts.

---

## Acknowledgments

Thank you to my mentor, Brian Macharia, for his continuous support and valuable feedback. His tips and resources have been instrumental in enhancing my coding and testing skills.
