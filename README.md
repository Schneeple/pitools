# Hello, welcome to a world where you have access to pitools.

## Windows Instructions:

1.  Make sure you have git installed on your computer. To test go to command prompt and type `git` and should see no errors. 

2. Open command prompt and type:
>  git clone https://github.com/schneeple/pitools.git

3. Go to environment variable -> system variables and create a variable called PYTHONPATH and set the value to be:
    `PYTHONPATH = C:\Users\{your-username}\`
    
4. Go to jupyter notebook or command prompt python and run:
>  from pitools import *

If there are no error then it worked and installed properly!

# Docker

7. Testing Dockerfile quick run. **This will delete all running containers**
```
docker rm -f $(docker ps -aq) ; 
docker build -t pitools -f Dockerfile . ; 
docker run -d -p 666:8888 -v $PWD:/opt/conda/lib/pitools pitools ; 
docker exec -it $(docker ps -n 1 -q) /bin/bash
```

