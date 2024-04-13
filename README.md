# SHAMELESS.LY - a psuedo-social media platform
#### Video Demo:  <https://youtu.be/UqvUhGuLwJs>
#### Description:

__Hello, CS50x!__

Welcome to my final project submission. This took inspiration from a popular website during the pandemic called *"unsent project"*, though I never had the opportunity to access it but my girlfriend shared to me what it was all about - it's a social networking platform where you don't need an account to post and can __post things or thoughts that you couldn't say out loud in person__. It was basically a lot like twitter or facebook according to her that people used to cope with the emotional distress brought the lockdowns and quarantines, so I took that as an inspiration.

I named the project or website as __Shameless.ly__ (domain already taken by someone else btw but I'm just using that name for as a placeholder for this exercise) because it draws inspiration of __not being ashamed to post your thoughts__ on the platform, whatever they may be and without judgement.

That being said, if you examine all the HTML, CSS, and JS files I will be honest that I initially drew inspiration from a Youtube tutorial I found (https://www.youtube.com/watch?v=p1GmFCGuVjw&pp=ygUSbG9nIGluIHBhZ2UgZGVzaWdu) in the overall design of the website since I honestly don't have any design skills but after getting the gist of it, I was able to make my own css design customizations in the `styles_landing.css`, `styles.css` drew inspiration from the Youtube tutorial which I made some minor personal tweaks.

I had to acquire some understanding of HTML and how important meta tags are and DOM structuring is from search engine optimization. I tried to structure the DOM in a way that it made sense, same goes for the meta tags to be sufficient enough for search engines to get data from i.e. the desciptions, alt texts, etc.

The real meat of the project went into the backend design which for some reason I find more fun than designing the front end. The entire app.py file was done by me with a lot of trial and error and searching online for references. I might have developed a bad habit of doing print() to debug my code but hey it worked! I also copied some snippets of codes from pset9 finance to help with the web apps security such as the app.configs, @login_required, and password hashing.

Getting immediately into the meat and bones of the flask backend, I believe I've written sufficient documentation in the app.py file itself so I won't go through that anymore but the major highlights of the program would be the following:

In `def login()` I added an error checker defaultly set to None, this will handle any login or account registration errors that the user may make such as:

    1. Non-existent or not registered account/email
    2. Wrong passwords
    3. Registering an already taken username
    4. Registering an email address that was already registered by someone else
    5. Not all fields in the registration form are filled. Although HTML handles that with the required tag but we still need to implement a check or protect in the backend to prevent someone from just altering their own copy of the HTML file in their browser and submitting it as David showed in the Flask lesson video (demonstrated also in my video usage of the project)

The value of error will be modified if any of the abovementioned conditions are found.

I implemented a simple posting system using sqlite. It will store the posted text and timestamp into the database and the page will refresh to show the 10 most recent posts made including the one you posted.

I also implemented 4 SQL tables that stores: login credentials, profile info that links with the id in login credentials, posts with their own post_ids that links with user_ids, a separate table that contains the urls of all selectable profile photos.

I didn't bother using try except because from what I've read online it takes more resources vs if-else conditionals, and also the fact that I got very used to programming in C in the first few weeks of lectures.

The whole process of creating the social media site was like SQL hell where i had to make sure that the right bio, posts, profile image, etc are routed to the right user_id, I also got stuck with some simple mistakes (i.e. typos, forgot to add the correct name attribute in request.form.get method) because of how complex the thing became because of the 4 tables where I separated the: login credentials, user posts, user profile data including bio and selected profile imgs, and a separate table containing the links to the images. I thought of doing it this way to keep it organized and to keep the number of columns to a minimum by grouping together into separate tables only the related items.

So that was pretty much it from me for now. It's not yet perfect but I did learn a lot of new stuff in programming with the python, Flask, SQLite tech stack. I will focus on refining the website in the future to further hone my skills but for now I think this is good enough given the time and lectures I took. I hope you find my project good enough! I hope I pass so that I can proceed to CS50web for a deep dive!