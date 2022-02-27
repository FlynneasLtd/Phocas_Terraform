import platform, requests, json, os, shutil, ctypes, sys

# as this is flexible per linux/windows this should be elevated at schedule level.
# for linux, you should edit sudoers to allow the designated user access to run this specific python file as sudo without password, then schedule in cron
# for windows, you should run as administrator when scheduling the script

githubURL = "https://api.github.com/repos/hashicorp/terraform/releases/latest"
terraformURL = "https://releases.hashicorp.com/terraform/"

def getOSDetail():
    osType = platform.system()
    osArch = platform.machine()
    return osType,osArch

def getLatestGitHub(versionUrl):
    makeRequest = requests.get(versionUrl)
    gitHubContent = json.loads(makeRequest.content)
    latestVersionV = gitHubContent['tag_name']
    latestVersion = latestVersionV.replace('v','')
    return latestVersion

def getLatestTerraform(version, masterUrl, os, arch):
    os = os.lower()
    arch = arch.lower()
    latestUrl = masterUrl + version + "/terraform_" + version + "_" + os + "_" + arch + ".zip" 
    return latestUrl

def downloadTerraformFile(fileDownload, location):
    fileToDownload = requests.get(fileDownload)
    newFileName = fileDownload.split('/')[-1]
    fileToDownload.raise_for_status()
    savedPath = location + newFileName
    savedFile = open(savedPath,'wb')
    savedFile.write(fileToDownload.content)
    savedFile.close()

def backUpPreviousFile(filePath, backupFolder):
    if os.path.isdir(backupFolder):
        print("") # folder exists
    else: # create expected folder
        os.path.join(filePath,'backup')
    fileName = os.listdir(filePath)[1]
    if os.path.isfile(fileName): # file exists, move to backup
        fullFilePath = filePath + fileName
        fullBackup = backupFolder + fileName
        shutil.move(fullFilePath, fullBackup)
    else:
        print("") # no file no action needed

osTypeData, osArchData = getOSDetail()
latestVersion = getLatestGitHub(githubURL)
fullURL = getLatestTerraform(latestVersion, terraformURL, osTypeData, osArchData)

# determine file location dependent on OS
if osTypeData == 'Windows':
    terraformLocalPath = 'C:/Program Files/Terraform/'
    os.chdir(terraformLocalPath)
else:
    terraformLocalPath = '/usr/bin/terraform/'
    os.chdir(terraformLocalPath)

newFileName = terraformLocalPath + 'terraform_' + latestVersion + '_' + osTypeData + '_' + osArchData + '.zip'
if os.path.isfile(newFileName):
    print("") # new version is same as current. no action. line 
else: 
    # backup old version, get new version
    terraformBackup = terraformLocalPath + 'backup/'
    backUpPreviousFile(terraformLocalPath,terraformBackup)
    downloadTerraformFile(fullURL, terraformLocalPath)



