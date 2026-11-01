# Build context:
#   docker build --platform linux/amd64 -f testing/docker/Dockerfile -t osintko-smoke:amd64 .
#   docker build --platform linux/arm64 -f testing/docker/Dockerfile -t osintko-smoke:arm64 .
FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y --no-install-recommends \
		python3 python3-pip python3-dev python3-tk \
		git curl wget build-essential cmake pkg-config \
		libjpeg-dev libpng-dev zlib1g-dev libssl-dev libffi-dev \
		libxml2-dev libxslt1-dev libsqlite3-dev libseccomp-dev libsodium-dev \
		golang-go cargo rustc \
	&& rm -rf /var/lib/apt/lists/*

ENV GOPATH=/root/go
ENV PATH="/root/go/bin:/root/.cargo/bin:${PATH}"

COPY testing/docker/install-tools.sh /opt/install-tools.sh
COPY testing/docker/test-tools.sh /opt/test-tools.sh
RUN chmod +x /opt/install-tools.sh /opt/test-tools.sh

RUN /opt/install-tools.sh

ENTRYPOINT ["/opt/test-tools.sh"]