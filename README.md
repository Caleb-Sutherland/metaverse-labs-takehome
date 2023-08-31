Thank you for taking the time to talk to me and send me this technical assignment. I don't have much experience doing projects with GPT or AI in general, so this took a bit of time and I was
unable to complete the part of saving embeddings to a vector DB (although I do get the embedding). 

Further, for the sake of time, I implemented a vanilla python server since I am not very familiar with Python Frameworks used for backend development. This server simply serves the index.html, which can take a prompt, send it to the serve and recieve a generated response from GPT2. 

In a production environment, I would use a backend framework for handling HTTP requests (Django, Express, or NestJS). To containerize the application, I would write a Docker file to create an Image. This image would provide the instructions on how to create a running container such as installing the dependencies (PyTorch and Transformers) and start the server by executing main.py.The image can be placed in the cloud (e.g. AWS EC2) so that containers can be spun up and served from a public IP address/domain. I don't have any experience using container orchestration services such as Kubernetes, but from my understanding it can be used to monitor containers health (especially when having more than one running) and can take down or spin up new containers depending on traffic or other requirements.

Thanks again,
Caleb