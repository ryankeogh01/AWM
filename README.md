# AWM-Assignment

For my GeoDjango assignment I will break down into steps every aspect of the project which was completed and then attempted.

Link to site : https://ryankeogh.xyz/

# 1 Creating Docker Containers
After installing all the necessary libraries and packages successfully I created 3 docker containers to run my project. A postgis container, a pgAdmin container
and a container of my project 'geodjango' using the docker image I built which is essentially a snapshot of the current state of the project.

I used the following command to build the image of my project:

- docker build djangogeo .

I used the following commands to do this:

- docker create network awm2022

- docker create --name gis2022 --network awm2022 --network-alias gis2022_db -t -p 25432:5432 -e POSTGRES_USER=docker -e POSTGRES_PASS=docker -v    gis2022:/var/lib/postgresql kartoza/postgis

- docker create --name pgadmin2022 --network awm2022 --network-alias mypgadmin4_2022 -p 20080:80 -t -e PGADMIN_DEFAULT_EMAIL=myemail -e PGADMIN_DEFAULT_PASSWORD=mypassword -v my_pgadmin4_data:/var/lib/pgadmin dpage/pgadmin4

After running these commands I was able to run my project through these containers and maintain all functionality such as logging in, singning up, updating the databas and finding user location.

# 2 App Functionality

My project contains a GeoSpatial database with functionality that will find a users location on the map after logging in or signing up. After displaying the users location to them on the map the user is prompted with a toast informing them that their location has been sent to the database. This then updates the database with the users point location in the database.

Below are some screenshots of the project in action whilst running through the containers created above:

- Landing Page

<img width="755" alt="image" src="https://user-images.githubusercontent.com/79484404/200816455-02f641ba-f730-45cf-ad8d-b46bc84276e4.png">

- Login Page

<img width="757" alt="image" src="https://user-images.githubusercontent.com/79484404/200816696-42b16ff2-2d7f-40aa-a62d-1bebe9b37c88.png">

- Sign Up Page

<img width="1507" alt="image" src="https://user-images.githubusercontent.com/79484404/200816898-3006b935-f627-4117-8509-ac9fc123d456.png">

- Map Page

<img width="760" alt="image" src="https://user-images.githubusercontent.com/79484404/200817221-c5ce14f8-ff0d-41cf-a08b-cbde98d21591.png">

- Map Page with DB Update

<img width="1508" alt="image" src="https://user-images.githubusercontent.com/79484404/200817397-125fa9c5-96bc-4300-96c8-0b8d4f6d950c.png">

- Django Admin Page with Updates of Created Users

<img width="764" alt="image" src="https://user-images.githubusercontent.com/79484404/200817756-75c3be90-cb43-4558-85a7-2d1092d2847c.png">

- PGAdmin Updated Tables with user last location

<img width="682" alt="image" src="https://user-images.githubusercontent.com/79484404/200818418-e5987801-4b72-40b3-8778-9d3511223301.png">

# 3 Deployment Pre-Requisites

The next steps I took for deployment I will outline below

- 1

I created a domain name ryankeogh.xyz using namecheap.com

- 2 

I created a docker vm droplet using Digital Ocean and configured it with my domain name.

- 3 

I appended my settings.py file in my project to be ready for deployment which is shown in the committed code, as well as this I added a .env file to store variables regarding my project secret key and database local and docker information. After this I migrated using python manage.py migrate.

- 4 

I pushed latest docker image to my docker hub repo called assignment for the image to be ready to pull into the VM when needed.

- docker tag 300db14a8d20 dockerhubusername/myassignment:latest

- docker push dockerhubusername/myassignment:latest

# 4 Deployment using my Digital Ocean Droplet 

I logged into my Digital Ocean droplet console called 'assignment' and ran the following commands to create containers within it for deployment:

- docker network create wmap_network (creation of network)

I then created a dockerfile inside the vm using vim to create and store it, the dockerfile looked like this:

FROM nginx
MAINTAINER Ryan Keogh
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install software-properties-common certbot python3-certbot-nginx

From here I built the image of wmap_nginx_certbot and created the container using the commands:

- docker build -t wmap_nginx_certbot .

- docker create --name wmap_nginx_certbot --network wmap_network --network-alias wmap-nginx-certbot -p 80:80 -p 443:443 -t -v wmap_web_data:/usr/share/nginx/html -v $HOME/wmap_nginx_certbot/conf:/etc/nginx/conf.d -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot -v html_data:/usr/share/nginx/html/static  wmap_nginx_certbot

Then I created ssh into the wmap_nginx_certbot container using docker exec -it  wmap_nginx_certbot /bin/bash and ran the certbot certonly --nginx command which was successful. This ws my output:

![image](https://user-images.githubusercontent.com/79484404/200850902-45a03f50-e6f0-48f9-9c4e-ea8db17a2a06.png)


Next I created the containers for PGAdmin and Postgis using these commands:

- docker create --name wmap_pgadmin4 --network wmap_network --network-alias wmap-pgadmin4 -t -v wmap_pgadmin_data:/var/lib/pgadmin -e 'PGADMIN_DEFAULT_EMAIL=ryankeogh2014@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=mypassword' dpage/pgadmin4

- docker create --name wmap_postgis --network wmap_network --network-alias wmap-postgis -t -v wmap_postgis_data:/var/lib/postgresql -e 'POSTGRES_USER=docker' -e 'POSTGRES_PASS=docker' kartoza/postgis

The next step for me was to create the Django Docker image, to do this I completed the following steps:

- I ran the command docker pull ryankeogh2001/myassignment to pull my django image I pushed to my docker hub repo

- I then created the container using:

- docker create --name myassignment --network wmap_network --network-alias wmap_alias ryankeogh2001/assignment

My next step which I completed was to configure my nginx proxy. I did this by creating the headers.conf and server.conf files in the etc/nginx/conf.d directory. These files had to be configured to match my domain name as well as my django and pgadmin container alias'.

After completing these steps I began running my containers using the command:

- docker start container-name

Upon doing this my postgis, pgadmin and wmap_nginx_certbot containers all ran as instructed apart from my Django container, which would stop immediately as I tried to run it. In the next section I will go through some of my error and the methods I took to troubleshoot this. 

After I fixed my error after some time I managed to use docker exec -it amdcontainer21 /bin/bash to get inside the container. From here I ran pyton manage.py migrate which worked successfully and gave me the following:

![image](https://user-images.githubusercontent.com/79484404/200851491-1f16c78c-fa89-423b-a87f-365f64660959.png)

After this i ran python manage.py collectstatic which also ran successfully.

Next I made sure to run all of the containers in order which appeared successful, below is a screenshot of these containers:

![image](https://user-images.githubusercontent.com/79484404/200852375-afe298f4-6869-4c2c-8d0f-378b0007da66.png)


# 5 Errors and Troubleshooting

Here is an image of my currently running containers inside the VM 

![image](https://user-images.githubusercontent.com/79484404/200827567-d5355999-e58c-4973-ae70-755ec1cf9e29.png)

These all work as directed apart from my Django Container, below is a screenshot of the output:

![image](https://user-images.githubusercontent.com/79484404/200827842-8f3995b4-ed47-4ab5-9a1c-8f14108819d5.png)

As we can see the container has an Exited(1) status and stops straight away.

Here is an image of the container appearing to run as commanded:

![image](https://user-images.githubusercontent.com/79484404/200828327-292ce900-274b-49f8-8dbf-9a0859b56818.png)

However the docker ps -a command still shows that it has exited immediately.

From this issue I have tried to delete the container and create it again, push a new image to the docker hub repo, pull it and create a new container using the new image, created a new droplet and ran all of the previous commands again to create the containers and the conf files, all of which have brought me the same error I have.

However, I continued to delve deeper into the issue and found that the issue I was getting was a Mac M1 issue. Docker was building the image using Macs arm64 architecture, but the linux VM environment required an amd64 architecture. To fix this, I needed to create a new image using the commmand

- docker buildx build --platform=linux/amd64 -t amdimage  . 

This command specified that the image be created for linux amd64. After pushing this image to the docker repo and pulling it to the VM and creating a container with it, I was able to get the container up and running successfully.

![image](https://user-images.githubusercontent.com/79484404/200837368-7d364b16-1e85-41de-b7d3-bec49b8e2994.png)

Finally i had an issue on the domain where I get this error of 502 bad gateway.
I  tried changing the proxy pass in the server.conf file to match my server of 127.0.0.1:8000 but this was worng. I then fixed the issue when i changed the proxy pass to the alias name of the django container that I had created.

![image](https://user-images.githubusercontent.com/79484404/200869128-892b21eb-58fc-4b93-b73a-423e5b06e7b7.png)

Upon deploying the application to my domain I had a few small issues. One being that my marker for the page wouldnt load but the blue circle would. If i had more time to go back to my code I would have fixed this issue along with a small issue on mobile devices which wouldnt let mobile users drop down the navbar. I would have fixed both of these with a small bit more time.

# 6 Conclusions

To conclude, for this assignment I created and ran a geospatial locations tracking application which I deployed locally during Docker. This application allows for users to sign in, log in, find their location on the map and for their location and user details to be posted to the database. After this I worked to deploy to my domain name and after some trial and error managed to get it up and running successfully. This was done using Digital Ocean where i created a droplet and and created the first 3 containers of postgis, pgadmin and nginx along with the certificate. The next step I took was to create a linux amd64 image using docker of my project and push it to docker hub. I pulled the image into my VM and created the django container using it. From here I launched up my containers and ensured that the site was deployed, which it was successful.








