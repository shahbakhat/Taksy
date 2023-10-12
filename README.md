![](/core/static/images/welcome.png)


# Taksy - Taxi bookig App apsseneger only

-  Taksy is a web app only for passnegers where the idea is passenger can make a booking for a specific time and admin of the app can check the bookings through the admin apanel of the app.

- Passenger can signup and login to the app and have a profile where they can store their phone number and password.

[View the deployed version here!](https://taksy-083499a57331.herokuapp.com/)

## Design

- ### Structure of the Application
  - Idea was taken from my previous proffession and the app i used to use as a driver and the was imprinted in my head.
  ---

   ### Welcome Page
   ---

   When a user go to the the link of the application, user is welcomed by following page. where user can either choose to go login page or signup page.
   ![](/core/static/images/welcome.png)

   ---
   ### Login Page
   ---
   When a user choose to login, if he doesnt have an account he can click on signup link to go to the signup form.
   ![](/core/static/images/login.png)

   ---
   ### Signup Page
   ---
   If user goes to the signup form, he is redirected to the following page. if he has an account already then he can login using the link provided just at the very bottom of the form.
   ![](/core/static/images/signup.png)

   ---
   ### Book a Taxi Page
   ---
   Either or both of these cases where user logs in or signs up he/she will be redirected to the the book a taxi page. where he can input the pickup and dropoff address and the time he desires be picked up, after that he can see the route and the distance of the route.

   ![](/core/static/images/booktaxi.png)

   ![](/core/static/images/booktaxi2.png)
   
   ---
   ### My Trips
   ---
   When a user finishes making a booking he will be redirected to My Trips page where he can see the details if the trip and is able to cancel the booking.

   ![](/core/static/images/mytrips.png)

   ---
   ### Cancel Booking
   ---
   If user cancels his trip and click on cancel button , a reconirmation modal will be shown to the user that do they really want to cancel the booking.
   and after canceling the trip will be shown in my trips with Red color and canceeled status at the top right corner of the booking card.

    ![](/core/static/images/canceltripmodal.png)

   ---
   ### Profile Page
   ---
   The profile page has First and Last name fields and profile picture field, and phone number. and also password field and change password field. user is able to update the profile as he/she likes.

   ![](/core/static/images/profile.png)
   
   ---
   ###  Adding the Credit Card
   ---
   User can add a credit card to the profile and keep it and remove it from the profile, stripe API has been used to create the credit card form and frontend element too. This festure is left for future implementations.

    ![](/core/static/images/addingcard.png)



## User Stories

  -   #### First Time Visitor Goals

      1. As a first time user I want to understand the bookig system easily.
      2. As a first time visitor I want to save my time and booking procedure must be quick. 
      3. As a first time user I want my details should be saved for the nect time i make booking.

  -   #### Returning Visitor Goals

      1. As a returning visitor i want to the history of my bookings and cancelled booking. 
      2. As a returning visitor my details must be saved , the credit card and my profile info. 
      3. As a returning visitor I should be able to change my profile picture if i want to.

  -   #### Frequent User Goals
      1. As a frequent user I want to be as quick as posssible to make my booking.
      2. As a frequent user I want all my data is saved on my account.
---
---
## Agile Planning
---
### Github Projects
- Github Projects were used to plan a todo list for thif project.
   ![](/core/static/images/agile1.png)
 ![](/core/static/images/agile2.png)


---

# Testing 


### Validator Testing - HTML

[W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the website. I have checked the HTML via address input and also by inspecting the page source and running this through the validator.

### Pylint
Pylint was used all the way through the development and errors were fixed during the development and at the end all the Python code was tested and found no issues.

### View Functions
All the view functions working perfectly without any error and all the associated Urls are in order.


* Welcome Page.
---
Encountered many errors in a deployed version where server requests were not going through, then i resolved by adding CORSHEADERS app, and CSRF allowed origins.
* Book a Taxi page.
---
In deployed version the Api keys were recognised and accessed and my environment variable were not being set, so i manually added them in Heroku settings. because this page has Google maps in it.
* My Trips Page.
---
My trips were being added to the page but when try to cancel the trip the channel froze due to the Bootstrap Jquery CDN duplication in base.html so i resolved that issue too.
* Signup Page.
---
Signup Form was being filled and submiitted but data was not being saved at all this was very complex issue at a time but error was very small in the Input Elemet the url was not mentioned which associated to the view function of the signup.
* Login.
---
The AUTHENTICATION was a real pain for days to me because it was my first time dealing with authentication model and Django User model and My own custom models but got through the pain of it and learned a lot from it.
* Stripe API
---
Stripe API caused me so many errors and had to go through so many Videos on youtube and other sources like artiles. first time using APIs was challenging but after all got it done and made it working perfectly.

* Models
----
All data specific to any model in the app is being being stored in the database.

* Taxi Booking
---
User is successfully booking the Taxi and successful booking is being saved in my trips and can been seen by admin in admin panel.



### Validator Testing - CSS
No errors were found when passing through the official [(Jigsaw) validator](https://jigsaw.w3.org/css-validator/): even though CSS was used very minimal.


### Lighthouse

Google Developer Tools lighthouse was used to check perfomance and accessibility issues. and here are the results.

![](/core/static/images/lighthouse.png)


## MANUAL TESTING

### Testing User Stories

### Manual Testing

The site was tested manually by going through all CRUD screens and forms, and ensuring error validation and functionality. The HTML, Python code was all manually.
adding and removing profile data and credit card, trips booking and cancellation.

* Forms
---
All the forms were tested including Login,Signup,Taxibooking form.
All data is passed through and submitted to the database successfully.

* Login
---
User logs in without any issue and redirected to the booking page.
* Signup
---
Sigup daata is beig saved successfully and user is redirected to the the booking page.
* Profile Update
---
User can update his profile easily with not issues and all redirects urls work fine.


The site was tested on the following devices: MacBook Air, MacBook Pro, iPhone, iPad, Google Pixel and ASUS laptop. The site was tested in Chrome and Safari.

## Deployment

### Local Deployment
​
*VSCODE* IDE was used to write the code for this project.


To clone a repository directly from Visual Studio Code (VSCode) without using the terminal, you can use the following steps:

- Open Visual Studio Code:

If you haven't already installed Visual Studio Code, download and install it from the official website: https://code.visualstudio.com/.

- Open VSCode:

Launch Visual Studio Code.
Make sure you have the necessary extensions installed for the programming languages or frameworks you'll be working with. VSCode often prompts you to install relevant extensions when you open a new project.

- Clone a Repository:

  1. Click on the "Source Control" icon in the left-hand sidebar (or use the Ctrl+Shift+G keyboard shortcut) to open the Source Control tab.

  2. Click on the "Clone Repository" button in the Source Control tab.

  3. In the dialog that appears, enter the URL of the repository you want to clone, e.g.,

  4. Choose the local directory where you want to clone the repository. You can click the "Browse..." button to navigate to your desired local directory.

  5. Click "Clone."

VSCode will clone the repository from the remote source and open it for you. You can start working on the project directly within VSCode without using the terminal. The Source Control tab in VSCode will allow you to manage your changes, commits, and synchronize with the remote repository.

---

### Heroku Deployment
---
​
This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.
​
Deployment steps are as follows, after account setup:
​
- Select *New* in the top-right corner of your Heroku Dashboard, and select *Create new app* from the dropdown menu.
- Enter a name for your app. The app name must be unique, so you need to adjust the name until you find a name that hasn't been used.
- From the dropdown, choose the region closest to you (EU or USA), and finally, select *Create App*.
- From the new app *Settings*, click *Reveal Config Vars*, and set the value of KEY to `PORT`, and the value to `8000` then select *add*.
- Now, add a seecond Config Var for the `creds.json`file, which contains the API Key from Google Sheets. Set the value of KEY to `CREDS` and paste the entire contents of `creds.json` in the VALUE box. Select *add*.
- Further down, to support dependencies, select *Add buildpack*.
- The order of the buildpacks is important. Select `Python` first, then *Save changes*. Click *Add buildpack* again, and select `Node.js`, then *Save changes*. If they are not in this order, you can drag them to rearrange them

Heroku needs two additional files in order to deploy properly.
- requirements.txt
- Procfile

You can install this project's requirements (where applicable) using: `pip3 install -r requirements.txt`. If you have your own packages that have been installed, then the requirements file needs to be updated using: `pip3 freeze --local > requirements.txt`

The Procfile can be created with the following command: `echo web: node index.js > Procfile`

For Heroku deployment, follow these steps to connect your GitHub repository to the newly created app:
​
- At the top of the screen on Heroku, select *Deploy*.
- Next to *Deployment method* select *GitHub*, then scroll down and click *Connect to GitHub* to confirm you want to connect.
- In the *repo-name* field, search for the name of the GitHub repository to deploy, and click *Search*.
- Click *Connect* to link the GitHub repository with Heroku. 
- Scroll down to the *Manual deploy* section, and click *Deploy Branch*.
- If you like, click *Enable Automatic Deploys* in the *Automatic deploys* section to have Heroku rebuild your app every time you push a new change to GitHub.

The frontend terminal should now be connected and deployed to Heroku.

## Credits and Bugs


### Content

### Code

- [MDN Web Docs](https://developer.mozilla.org/en-US/) for general debugging. 

- [StackoverFlow](https://stackoverflow.com/questions/70656467/stripe-card-element-isnt-visible-python-django) used to resolve stripe Catd element issues.

- [StackoverFlow](https://stackoverflow.com/questions/27729487/how-to-catch-a-unique-constraint-failed-404-in-django) solved unique constraint error.

- [Bootstrap Docs ](https://getbootstrap.com/docs/5.3/getting-started/introduction/) was used for every element.

- [Stackoverflow] (https://stackoverflow.com/questions/34033108/django-authentication-with-custom-user-model-not-working) was used to get an idea of clean Password and clean email addresses.

- Advice, help, debugging and guidance for my whole project from my online resources.

- Some deployment instructions were taken from Code Institute previous project.

- Slack used to ask questions from fellow students and alumnis. This was particular helpful when trying to get my Heroku Deployment working properly.


## Acknowledgements 

- I thank to code Institute for providing the great material or this course and really learned how to actully build something not just a typical online course. Slack community as always, and my friends and family who supported me specially while raging over the code not working.