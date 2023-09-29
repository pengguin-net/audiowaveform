
check-req:
	@which python3 > /dev/null || (echo "Python3 not found, please install it first." && exit 1)
	@which poetry > /dev/null || (echo "Poetry not found, please install it first." && exit 1)
	@which docker > /dev/null || (echo "Docker not found, please install it first." && exit 1)

install-deps: check-req
	poetry install
build: check-req
	poetry export --without-hashes -o requirements.txt
	docker build -t pengguin-audiowaveform-service .
