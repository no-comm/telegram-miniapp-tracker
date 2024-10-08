# Telegram MiniApp Tracker

The project allows you to track traffic for any telegram mini application.

First, you need to log in to telegram.

The main file to run main.py , to run, you need to specify the arguments

```
python main.py <method> <username_bot> <short_app_name> <start_param>
Example: python main.py tdata username_bot short_app_name start_param
Example: python main.py web
```

## Web

To log in via web telegram, you must specify the web argument, after which authorization will be performed, followed by saving the session.json, for the following launches.

After authorization, you just need to open a window with the game (the mini application launch button)

## Tdata

Authorization via tdata assumes that you have logged into your account in telegram version 4.x.x and below, then you need to place the tdata folder in the startup folder main.py

In the startup arguments, you must specify username_not, short_app_name, start_param (optional)

Example for hamster combat:

```
python main.py tdata hamster_kombat_bot start
```

## Traffic tracking

A window with the game opens, you need to do all the necessary actions in it to generate requests (just click on different buttons), after which the folders packets_log, packets, py_module will be created in the folder with the domain name of the site.

## packets_log

### order_packet.txt

Shows the order in which packages are sent

```
2024-10-08 16:31:57.361070 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/user | GET | 200
2024-10-08 16:31:57.541499 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/promotions | GET | 200
2024-10-08 16:31:57.797396 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/links | GET | 200
2024-10-08 16:31:58.190652 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/user | GET | 200
2024-10-08 16:31:58.437761 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/cards | GET | 200
2024-10-08 16:32:00.466426 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/cards | GET | 200
```

### order_packet_unique.txt

Shows the order in which packages are sent, but only unique URLs

```
2024-10-08 16:31:57.361070 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/user | GET | 200
2024-10-08 16:31:57.541499 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/promotions | GET | 200
2024-10-08 16:31:57.797396 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/links | GET | 200
2024-10-08 16:31:58.437761 | https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/cards | GET | 200
```

## packets

Creates subfolders from package sending domains and saves all packages in json format

Example: miniapp_user.json in scam_me_backend_fs4mn_ondigitalocean_app

```json
{
    "request": {
        "method": "GET",
        "url": "https://scam-me-backend-fs4mn.ondigitalocean.app/miniapp/user",
        "headers": {
            "referer": "https://scam-me.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.31 Safari/537.36",
            "auth-token": ""
        },
        "body": null
    },
    "response": {
        "status": 200,
        "headers": {
            "date": "Tue, 08 Oct 2024 11:31:57 GMT",
            "content-encoding": "br",
            "cf-cache-status": "MISS",
            "last-modified": "Tue, 08 Oct 2024 11:31:57 GMT",
            "server": "cloudflare",
            "x-do-app-origin": "",
            "x-do-orig-status": "200",
            "vary": "Origin, Accept-Encoding",
            "content-type": "application/json",
            "access-control-allow-origin": "https://scam-me.com",
            "cache-control": "private",
            "access-control-allow-credentials": "true",
            "cf-ray": ""
        },
        "body": null
    }
}
```

## py_module

The main PacketsLog.py with the implementation of all queries in the same order, the utils folder with query classes
