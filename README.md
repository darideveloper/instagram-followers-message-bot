<div><a href='https://github.com/darideveloper/instagram-followers-message-bot/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/darideveloper/instagram-followers-message-bot.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/instagram-followers-message-bot/blob/master/logo.png?raw=true' alt='Instagram Followers Message Bot' height='80px'/>

# Instagram Followers Message Bot

Bot for track your Instagram followers and submit messages to the new ones.

Start date: **2023-06-05**

Last update: **2023-06-05**

Project type: **client's project**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#relatedprojects'>Related Projects</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li>
<li><a href='#roadmap'>Roadmap</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a><a href='https://sqlite.org/index.html' target='_blank'> <img src='https://cdn.svgporn.com/logos/sqlite.svg' alt='SQLite' title='SQLite' height='50px'/> </a></div>

# Related projects

<div align='center'><a href='https://github.com/darideveloper/instagram-post-bot' target='_blank'> <img src='https://github.com/darideveloper/instagram-post-bot/blob/master/logo.png?raw=true' alt='Instagram Post Bot' title='Instagram Post Bot' height='50px'/> </a></div>

# Media

![screenshot](https://github.com/darideveloper/instagram-followers-message-bot/blob/master/screenshot.png?raw=true)

# Details

This project detect your **new followers on Instagram**, and **sent custom a message** to them. 

You can setup the number of messages per day (more details in the **settings** section).

## Database

The information its saved in the local database **database/database_bot.db**, and you can manage it with the python scripts inside the "scripts folder":
* **add_message.py** - add manually a register of a new message
* **delete_messages.py** - delete all messages in database
* **get_messages.py** - show all messages in database

### Send values

The **sent** column of the database, may have one of the following values: 

* **0.** Message ready to send
* **1.** Message sent
* **2.** Initial follower
* **3.** Error sending message

## Workflow

1. The first time you run the script, it will get your current followers from your profile. 
2. After that, each time, the script will get the new followers, and submit a custom messages to them (message requested by terminal)
3. When a new follower its detected, it is saved in the database with "sent" status as "0" (like to False).
4. After sent the message, the status its updated to "1" (like to True).
5. You can setup the max number of messages to send per day in the **.env** file.

# Install

## Third party modules

Install all modules from pip: 

``` bash
$ pip install -r requirements.txt
```

## Programs

To run the project, the following software must be installed:: 

* [Google Chrome](https://www.google.com/intl/es/chrome) last version
* Python >= 3.10

# Settings

## Enviroment variables

In this file (*.env*), are the main options and settings of the project.

1. Create a **.env** file, and place the following content

```bash
MESSAGES_PER_DAY = 10
WAIT_TIME = 2
```

### MESSAGES_PER_DAY

Max number of messages to sent each day

### WAIT_TIME

Wait time (in minutes) between each message.

*Note: you can see as reference the **sample.env** file*

## Cookies

You should login with your instagram account,  get your cookies (in order to avoid login), and save them in this file (*cookies.json*).

1. Install the extension [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=es)
2. Open a Incognito window 
2. Go to your Instagram account (with user and password)
3. Click on the EditThisCookie icon
4. Click on button "Export" (the cookies will be copy to your clipboard)
5. Create a file **cookies.json** in the project folder
6. Paste the cookies
7. Save the file

*Note: you can see as reference the **sample.cookies.json** file*

# Run

Run the project folder with python: 
```sh
python .
```

Or run the main file:
```sh
python __main__.py
```

## Run in loop

If you want to tun the bot in loop (one or multiple times each day), I suggest you to use tools to run the script all days at specific time, like [Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) for windows, [Cron](https://www.google.com/search?q=linux+cronjobs&oq=linux+cronjobs&aqs=chrome..69i57.3719j0j1&sourceid=chrome&ie=UTF-8) for Linux or [Jenkins](https://www.jenkins.io/) for both systems

# Roadmap

* [x] Login with cookies from local json file
* [x] Get folloers first time
* [x] Use local database
* [x] Detect new followers
* [x] Submit custom message to new followers
* [x] Limit max number of messages per day

