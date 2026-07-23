This file is meant to be read by a human.
Written completely by a human

Basically for all software development tasks we have 3 different kinds of requests:
1. A request which makes some changes in a database and returns something, (basic crud, getting something from database and modifying it using business logic)
2. Async requests, a request made which takes some time to run and is done on backend
3. Scheduled runs, A task or function we need to run at X hour everyday.


Here the way we have this repository is such that for backend each request is first routed either towards 1 , 2 or 3. If it is 1 and requires some changes in api we make those changes, if it is 2 and requires a celery job we create that celery job and so on.

Any ai model you will be using will already see the instructions for writing tests, linting and ensuring consistency in devlelopment.
There isnt much of strict rules to ensure that ai have the flexibility to do it as it sees fit but still there are some devleopment guidelines like
its necessary to use service class for business logic, its necessary to write tests for the api we are writing. 

This repository at the time of writing does NOT support websockets so implementing websockets is the next, we will be implementing https://centrifugal.dev/ for this.

Everything folder the repository will initiate a docker container which will run our application. 

This is kind of like a boilerplate framework for developing applications. 

This is not a perfect repository there are many other things that needs to be done here which we are expecting you to do as this is an open source repository. 