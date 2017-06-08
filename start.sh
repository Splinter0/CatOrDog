GOPATH=$(pwd)
export GOPATH
cd src/network/ && python network.py &
cd src/app/ && go build . && ./app
