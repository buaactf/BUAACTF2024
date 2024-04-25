FROM zeroc0077/n1ctf2022-utility-payment-service:latest as builder

WORKDIR /app
COPY server ./server
COPY program ./program

RUN mkdir -p /app/challenge
COPY flag.txt /app/challenge/flag.txt

RUN cd server && make
RUN cd program && make

FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get -y install libudev-dev libssl-dev pkg-config

WORKDIR /app

COPY --from=builder /app/challenge/award-server /app/award-server
COPY --from=builder /app/challenge/award.so /app/award.so
COPY --from=builder /app/challenge/flag.txt /app/flag.txt

USER nobody
CMD ["/app/award-server"]
