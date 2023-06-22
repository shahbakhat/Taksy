

## Taksy
Taksy app is a Taxi booking system hwere Passeneger can book a taxi in advance and have peace of mind.

View the deployed version [here](https://taksy-083499a57331.herokuapp.com/)!


## User Stories
### First Time Visitor Goals
- As a first time user i want to signup as quickly as possible.
- As a first time visitor I want to book as quick as possible to save time.
- As a first time user I want it to be easy to sign up and get the trip booked.

### Returning Visitor Goals
- As a returning visitor I want to see have my details saved to save the hassle of doing it again.
- As a returning visitor I want to make sure that i judt login and book and there are no extra steps to take.

### Frequent User Goals
- As a frequent user I want to book the trip on one tap.
- As a frequent user I want to be able to book and cancel the trip at change of plans.

## Agile Planning
### Github Projects
i used github and ChatGPT to make a gameplan to execute this as sufficient as possible.

![Github Projects](https://github.com/shahbakhat)

## Features
### Existing Features
in future improvements im already working on it make it like some already Taxi dispatches in existence. like Uber, FreeNow , Bolt and few others. want to make a brand logo and develop the Driver client server realtion where Passenger aand Driver will be able to communicate with one model , model as in Backend model.

#### Register & Login
At the start of the application i have a Welcome page with conventional Taxi colour scheme #FFC107 and nice hover effect on buttons. You can register register and start booking.

#### Book a Taxi  Tab
On Book a Taxi tab there is inputs for pickup and dropoff addresses with google maps routes display with calculated distance between the pickup and dropoff. Your payment method is shown at the bottom so you can see what you are paying with and your saved phone number is shown too.


#### My Trips Tab
When you have made a succesful booking , you will be redirected to My Trips tab here you can see your bookings and you can cancel the  booking by clicking the cancel button.

#### Profile Tab
It has been made very simpple to just save First Name and Last Name , Phone Number and you can change your password and other info of course.


#### Payment Tab
Here you can save your card information and remove your card information whenever you want to, Stripe has been used a Payment gateway so you know we have no details whatsoever saved except the last 4 digits of the card.

#### Profile picture and Name
Your profile picture will be shown at the top right of the screen with your name and the name is actually the link button to your profile.

### Deleting Account
There are 2 models in the backend one is User model which customised model and has a corresponding Object called with the role of the user. User model is the just a user with your profile and the corresponing Object model is the functioning model for the actions taking place on behalf of the user such as payment methods and and booking trips.
On deleting the user will delete the associated model and the associated details with it.

## Deployment
### Local Deployment
To create a local copy of this project, follow these steps:
1. Clone the project's repository by running the following command in your terminal:
```
git clone [[repository-link](https://github.com/shahbakhat/Taksy)]
```
2. Set up a virtual environment and install the project dependencies by running the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Create a file named `.env` in the project's root directory and add the necessary environment variables, such as database connection details and API keys.

4. Run the development server with the following command:
```
python manage.py runserver
```
5. Access the website locally by visiting `http://localhost:8000` in your web browser.

### Heroku Deployment
This project is deployed on Heroku, a cloud-based platform for hosting web applications. To deploy your own version of JVN on Heroku, follow these steps:
1. Sign up for a Heroku account and create a new app.

2. Set up the necessary environment variables in the Heroku app's settings. These variables should include your database connection details, secret key, and other configuration settings.

3. Connect your Heroku app to the project's GitHub repository by linking them in the Deployment section of the Heroku dashboard.

4. Enable automatic deployments from the selected branch of your repository.

5. Trigger a manual deployment or wait for automatic deployments to take place whenever you push changes to the selected branch.

6. Once the deployment is complete, access your live website using the provided Heroku URL.

## Credits and Acknowledgements
### Media
- The logo was created using Looka.com.
- Background photos used in different sections of the website were sourced from realgear.net, raregallery.net, and wallpaperFlare.

### Content
- Code Institute's Gitpod Full Template provided the initial workspace template for this project.
- The README structure was inspired by Code Institute's README Template.

### Code
- Code Pen was utilized for testing and experimenting with code snippets before implementing them in the project.
- Code Institute's modules, including "I Think Therefore I Blog" and "Hello Django," were referenced for setting up the basic structure and functionality of posting news articles and managing user comments.
- Stack Overflow and MDN Web Docs , WW3 schools, Youtube videos, ChatGPT, articles.
- Geeks for Geeks, Coding Ninja.
- Google Firebase, Google Cloud Platform for Developers.

### Acknowledgements
- Cant thank enough to Code institute help in my exceptional times i really appreciate their understaing of scenarios in peoples life.
- The Code Institute Slack community was an excellent source of advice and inspiration, especially when troubleshooting deployment-related challenges.

## Bugs
- At first all was going well but when starting working with the models abd APIs it got really complicated.
- Migrations and there behavior to the functions of the whole framework was mind bogling and i had to drop certain tables and once even deleted the pycache and the whole .db file.
- Got stuck is AUTH_USER_MODLE and its authentications process and the whole system. the instance of the objects it keot the awake straight for 3 nights, it was very stressful but slowly slowly got out of it by solving the puzzles and it made me happy that i learned a lot with this project.
