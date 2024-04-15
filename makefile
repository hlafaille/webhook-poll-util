build_bin:
	python -m nuitka --standalone --onefile --output-dir=target --output-filename=webhookpollutil src/main.py

build_oci:
	docker build . -t ${IMAGE_TAG}