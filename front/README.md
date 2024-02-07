To run type in your console:
```
npm install
npm start
```

To create a docker image:
```
docker image build -t react:v1 .
```

To run this docker image:
```
docker run -dit -p 3000:80 --name react react:v1
```