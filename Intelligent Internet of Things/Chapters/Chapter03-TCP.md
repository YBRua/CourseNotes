# Mechanism of the TCP Protocol

> TCP: Transmission Control Protocol
> Provides RELIABLE data transfer over unreliable Internet

## Overview

- The TCP protocol runs on senders and receivers
  - Classic TCP does not run on routers
  - Althogh there can be exceptions
- Functionalities of TCP
  - Reliable data transfer
  - Congestion Control
  - Flow Control
  - Connection Management

## Reliable Data Transfer

- Resolves 3 problems
  - Error
  - Loss
  - Performance

### Resolving Transmission Errors

What error?

- Bit flipping

#### Acknowledgement

- Received correctly: `ACK`
- Reveived incorrectly: `NACK`

But how to detect transmission errors?

##### Error Detection: Checksum

- Requires the sender to compute the **checksum** and include it in the packet
  - divide data into 16-bit words
