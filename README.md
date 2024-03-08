# Florgon CC Pastes Bot

Simple telegram bot for **Florgon CC Pastes** using it official [api](https://github.com/florgon/cc-api), written in python using aiogram.

It is free software and licensed under **AGPLv3 or later**.

## Deploy

For deployment you should create telegram bot at BotFather and install docker with docker-compose via your package manager.

1.
```
cd src
cp config_example.env config.env
```

2. Open `config.env` file and fill in your values for environment variables.
3. (I recommend you to use docker with docker-compose)
```
docker-compose build
docker-compose up
```
4. Check docker logs and then check the bot with `/start` command

## Using

Available commands:
- */start* - Standart start bot command.
-
```
/paste ```<language>
<code>```
```
Create new paste with *language* and *code* (text). *Language* is optional. *Code* may be multiline.

- */read <url>* - Print text and info about paste. *Url* is url to paste.
- */stats <url>* - Print statistics about paste if allowed. *Url* is url to paste.

## Contribution
Contributors are welcome! You can send issues and PRs.
