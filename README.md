# TgBigFileUploader
TgBigFileUploader is a Python script that will zip the subfolders in your designated folder with a password and slice them into 2GB segments to cope with Telegram's 2GB upload limit. Then, it will output into the output directory, upload the zip files on Telegram using the [FastTelethon](https://gist.github.com/painor/7e74de80ae0c819d3e9abcf9989a8dd6) script, and send the uploaded file into groups or channels.



Before using the bot, you will have to create a `.env` file, the content is as follows:
```
TELEGRAM_API_ID=<Telegram API ID>
TELEGRAM_API_HASH=<Telegram API Hash>
TELEGRAM_PHONE_NUMBER=<Phone Number>
ENCRYPT_PASSWORD=<Password used to encrypt>
TELEGRAM_GROUP_ID=<Telegram Group/Channel ID>
INPUT_DIRECTORY=<Directory that contains subfolder to zip>
OUTPUT_DIRECTORY=<Output directory of zipped files>
```



## Terms of Use
- You are not allowed to redistribute any part of the code and claim that is your work.
