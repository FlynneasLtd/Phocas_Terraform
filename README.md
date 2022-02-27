# Phocas Terraform
Download the latest version of Terraform for Windows/Linux using Python

This repo contains scripts to download the lastest stable release of Terraform, schedule the script and backup the existing file retaining its version name. The testing machine was Windows 11 Pro.
Please see below a description of the task.

## Problem
We want to automatically update Terraform "https://www.terraform.io" on our deployment server every week.

## Guide
The deployment server is Windows Server 2019, Windows 10 or modern linux distro. The choice is a personal preference for the sake of the challenge.

## Challenges
Each challenge is set to build on the previous challenge.

### 1
Script an automatic download of the latest stable release of Terraform, the file must be placed in
  C:/Program Files/Terraform (C:\Program Files\Terraform\)
  /usr/bin/terraform
Some notices regarding the challenge, elevation will be required and the location of the releases can be found here ("https://releases.hashicorp.com/terraform")
  
### 2
Schedule the script or explain a system to perform the script from challenge 1. It must run weekly on Mondays at 9am New Zealand Standard Time (NZST).
A notice on this challenge is the deployment server's timezone is UTC.

### 3
Modify the script to rename the existing file for backup purposes.
A notice here is regarding a naming convention to keep the version number.

## Description
I have chosen Python for this task. This was chosen primarily because this was the language used at Phocas moreso than other languages. A secondary reason is Python can be installed on different OS making it more versatile. Lastly, whilst my most experienced language is in Node, I definitely wanted to make the process in Python as a true challenge.

## Pre Requisites
The script runs assuming a few things; including that python 3 is installed. First, that it will be elevated during the schedule task. This can be achieved as written inside the script:
- Windows
  - Elevate within Task Scheduler by choosing the user to an administrator.
  - Run whether the user is logged on or not.
- Linux
  - Edit the sudoers file to allow the account running the cron job to use sudo without a password prompt but for security specifically to run the py script.
  - Schedule the script in cron but add to the root cron using sudo crontab -e

A virtual environment was created to run the script, although not necessary but is recommended, which for the purpose of this test it was used.
The testing machine was on Windows 11 using Python 3.9 and a "pip install requests" command was used.

As I have chosen to make the script versatile for operating system, I therefore chose to make the elevation commands outside the script. However to run inside the script, you can use the following depending on the OS.
- Windows
  - Use a function to check if user is admin. Return false if not.
  - If user is admin, run the script. Else run the script again using runas which then triggers the true to the original if statement.
- Linux
  - Assuming the sudoers is in place, you can either make a .sh script to sudo python ./phocas-terraform-download-weekly.py
  - Alternatively to another script, you can do a similar ideaology used in the Windows version and open a new shell using the sudo command, however adding to the root crontab is easier.
  - If sudoers is not altered, then using the runas new shell with sudo in place with a check for elevation inside the script.

## What does the script do?
The script uses platform, requests, json, os, shutil, ctypes, sys; of which requests needs to be installed. Links to the hashicorp of terraform files is navigated by extracting the latest version on terraform's github page.
- The operating system and architecture type are extracted in aid of downloading the file which is labelled by OS and arch type.
- GitHub page is extracted and retained in JSON format in order to extract the tag_name attribute. A replace for the "v" is used to get just the numbers and full stops.
- Terraform URL is generated using the version number, os and arch type from previous functions.
- A check on the OS is made, for now it checks for Windows or Linux then sets the terraformLocalPath variable to the correct location and changes to this directory.
- A backup is performed, if there is a current file that is different the new expected file, it will move the old file to the backup folder. The backup folder is created if it does not exist.
- If the file is the same as the old one, it does not download. If the file is new it moves old and downloads the new file.

## How could the script be changed or improved?
For the purpose of this challenge, I chose to have most actions inside a function, particularly the getOSDetail function; this could be declared outside any functions. I chose to make it a function because it returns two values that I later need to use. 
Also as previously mentioned, elevation can be added to work inside the script however as stated because I've chosen to make it variable, to save on lines written I would make the scheduled task elevated. Although it can be kept variable to OS and include the equivalent elevation in the script; I chose not to as to keep the code clean to the challenge's purpose. As with 99% of scripts, there are always changes to be made at some point in the scripts life and I am no Python Master so there are bound to be changes/optimisations to be made.

## Why is it flexible?
The challenge does state to choose Windows or Linux, however I wrote a python script that looks at the system its running on to determine the version. I did this because I like to create programs that fix or work themselves. In this scenario, the script itself (assuming tasks are setup or the elevation talked previously is added), will run regardless of Windows or Linux. It can be moved/copied to either system without further input. Python again seemed the ideal choice for the flexibility, as easily installed on both Windows and Linux.
