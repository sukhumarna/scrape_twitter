# Scrape Twitter Project
This project provides services to get tweets data from hashtag keywords and tweets from user's feed.

##  **Project Structure**
```
├── app                     <- app python package
│   ├── models              <- data model schema package
│   │   └── tweets.py
│   ├── routers             <- routers package for API endpoints
│   │   └── tweets.py
│   ├── services            <- services package to get tweets
│   │   └── search_tweets.py
│   │   └── user_feed.py 
│   └── main.py             <- The main module
├── tests                   <- unittest package
├── Dockerfile              <- Dockerfile
└── requirements.txt        <- The requirements file for installing necessary packages

```

## **Installation**
### Running Locally
```
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

### Running on Docker
```
docker build -t scrape-twitter  .
docker run -d --name scrape-twitter-container -p 8000:8000 scrape-twitter
```

## **API Document**
FastAPI provides interactive API documentation.  
go to http://127.0.0.1:8000/docs for OpenAPI specification (swagger)
or go to http://127.0.0.1:8000/redoc for redoc
