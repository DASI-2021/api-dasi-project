# DASI API backend (Looking notice)

Looking notice is a project that consists of creating a sports news recommendation wizard in English, which will have a series of categories such as soccer, tennis, among others; Allowing the user to search for news through a series of interactions with an assistant called a chatbot using natural language, interaction with the user is extremely important for the search agent and the classifier agent, which are two complementary agents, to learn more accuracy of the user's request and have the ability to respond and learn from their dialogue to deliver the best news.

----

## 📖 Installation
This project can be installed via Pipenv, or virtual enviroment depending upon your setup.

```
$ git clone https://github.com/DASI-2021/api-dasi-project
$ cd api-dasi-project
```

### virtualenv

```
$ python3 -m venv api-dasi-project
$ source api-dasi-project/bin/activate
(api-dasi-project) $ pip install -r requirements.txt
(api-dasi-project) $ python flask-chatbot/app.py
```
The demo will be live at [http://localhost:5000/](http://localhost:5000/)

### Pipenv

```
$ pipenv install
$ pipenv shell
(api-dasi-project) $ pip install -r requirements.txt
(api-dasi-project) $ python flask-chatbot/app.py
```
The demo will be live at [http://localhost:5000/](http://localhost:5000/)