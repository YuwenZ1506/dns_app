References to run the code for practice purposes. 
To set up on the docker:

# Create images for three servers:
docker build -t user_server -f Dockerfile_us .
docker build -t fibonacci_server -f Dockerfile_fs .
docker build -t authoritative_server -f Dockerfile_as .

# Run three servers
docker run -d --name authoritative_server -p 53533:53533 authoritative_server
docker run -d --name fibonacci_server -p 9090:9090 fibonacci_server
docker run -d --name user_server -p 8080:8080 user_server

When all three servers running normally, identify the IP address for FS server and for AS server. Then create FS registration follow below format:
curl -X PUT http://localhost:9090/register -H "Content-Type: application/json" -d '{ "hostname": "fibonacci.com", "ip": IP address for FS server ,"as_ip": IP address for AS server, "as_port": 53533 }'

Then run the website to calculate any Fibonacci number of any digit.
http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=6&as_ip= IP address 
