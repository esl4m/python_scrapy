# python_scrapy


## User Story
```
As a developer
I want a tool to automatically check all the webpages in the website
So that I can quickly identify if the new features or the bug fixing changes introduced to the website break any existing pages.
```

## Acceptance Criteria
- All the public facing webpages in the website can be easily located and tested.
- Any error pages should be logged for further follow-ups.


## Getting Started
### To run the app on docker:
- Clone the repo to your local
- cd into folder.
- Run the following command:
`docker-compose up --build -d`

- To check the status of the running containers, run the following command:
`docker ps -a`

- To get inside the docker container using this: 
`docker exec -u 0 -it Container_ID bash`

### To do add tests ..
