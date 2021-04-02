# MS3 
# Online Cookbook Recipe & Tool Sharing!
This site is intended for people to not only **FIND** recipes, but also **SHARE** their own, 
whilst simultaneously **INSPECTING** various cooking tools that can help with these fantastic cooking moments!
Thus, this site will aim to provide users with all they need to achieve their ideal meal.

---
# UX

In terms of User Stories, this site behaves differently depending if the user is registered with the site, or is an anonymus visiter.
And so, as such, the user stories differ.

### **Anonymus User**

* *I want to find/search for recipes*
* *Perhaps there are tools that will help me with my cooking?*
* *What do I gain from creating an account?*

### **Registered User** 
(shares many of the user stories with anonymys users, in addition to these...)

* *I want to share my own recipies with others*
* *I want to be able to manage my profile*
* *I want to edit my own recipies*

However, there are also other cases that need to be noted.

* *The admin user will need to be able alter anything regarding the site, including user's profiles and recipies*

### **Wireframes**
* Included below are links to the wireframes for three major devices; **desktop**, **mobile**, and **tablets**)
(Alternatively, they may be found inside the "wireframes" folder directory).

---

# Features

In addition to other features, the **CRUD** guidelines are also intended to be major features for this site's functionality and purpose.

* *Log In/Log Out*

* *Register*

* *Manage Profile*

* *Browse*

* *Search*

* *Social Media*

* *Navigation Menu*

* *Given two registered users, user 1 should not be able to update or delete user 2's recipes, nor can the anonymus user alter any other's recipes. Users cannot change anything about
any other users profiles as well*

* *If a recipe is deleted but you clicked on edit or accessed it through the URL, it should redirect you to a 404 page*
* *The search bar will show/auto complete only recipe titles*

* Expected -Feature is expected to do X why the user does Y
Testing - Tested the feature by doing Y
Result - The feature did not respond due to A,B,C
or
Result - The feature acted as normally and it did Y
Fix - I did Z to the code because something was missing
and the inclusion of screenshots.

---

# Technologies/Programs Used
* HTML 
* CSS 
* Materlize Library
* Python
* Flask
* MongoDB, AWS (Free Tier)
* Chrome Dev Tools 
* Lighthouse Audits
* Github
* Gitpod
* Heroku
* dnspython
* Flask-pymongo
* Fontawesome
* Jquery
* Werkzeug

Additional technologies/installs may be observed in the requirements.txt file located in the directory, or accessed through here; https://github.com/Windmost8/MS3-Cookbook-MostaphaE/blob/39c2cf5fe35dca38f12ab4fad3b0c562eef14493/requirements.txt

---

# Typography/Color Sceheme
As mentioned in the technologies seciton, materlize was used as a css library for this project.
The color scheme decided upon was light orange, with an aliceblue background. The light orange in question is
called "orange lighten-2" from Materlize. The reason for orange was because I felt that it closely matched the theme
of the site, which was about cooking, and orange is a color very dominantly present in dishes.

The reason for an aliceblue background was just as a contrast against the orange color.

In addition, a text-shadow css class wa put in place to allow texts to be shown easier for the eyes against colorful backgrounds, which in this case was orange again.
Also, the text itself is white in color for it to also stand out despite the orange background.

# Testing

### **Screenshots**

* All screenshots can be found in the screenshots folder,
or viewed from this link;

* The screenshots include both desktop and mobile pictures, indicating the intended output.
Such as;

### **Validation**

* HTML code was validated through https://validator.w3.org/

* CSS code was validated through https://jigsaw.w3.org/css-validator/

### **Test Cases**


### **Issues** 

* At times, whilst opening browser through gitpod, the project shown may not be updated despite clicking on the refresh button. 
    Therefore one must ctrl-click the refresh button for a forced refresh. 

---

# Deployment

### **Gitpod** 

* To preview site through gitpod, run the command "python3 -m http.server" in the terminal (without the quotes). 
* Executing this should prompt a pop up for port 8080
    alongside the options to "Make Public" or "Open Browser". If it is the first time after opening gitpod, then click on "Make Public", and then "Open Browser" if the pop up
    comes up again. If the pop up does not come, you may alternatively ctrl-click on the link that will be shown in the terminal for port 8080.
* Gitpod has no automatic saving, so saving after each change is optimal.


### **Github**
* In order to commit, whilst still in gitpod, running the command git add . (or a specific file/folder instead of "." (without the quotes)),
    will add all the changes you have done to be prepared for a commit. 
* After this step, you may run the command git commit -m "your comment" (your comment being whatever message you want to convey alongside the commit). Running this will 
    show how much changes were done, through the terminal.
* Finally, running the command git push should put your changes and project into your repository.

### **Heroku**
* ds


---

# Credits 
Two of the cooking images were taken from https://www.dreamstime.com/photos-images/asian-cooking.html.
The two in question being:
https://thumbs.dreamstime.com/b/onion-pepper-tomato-tomato-lime-vegetable-asian-cooking-vintage-image-onion-pepper-tomato-tomato-lime-vegetable-asian-185990624.jpghttps://thumbs.dreamstime.com/b/asian-food-cooking-wok-noodles-chicken-stir-fry-vegetables-ingredients-spices-sauces-chopsticks-dark-rustic-83701227.jpg

---
