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

##### Error Detection: Checksum

How to detect transmission errors?

- Requires the sender to compute the **checksum** and include it in the packet

##### Handling Corrupted Acknowledgements

- If an acknowledgement is corrupted and sender cannot determine whether it is `ACK` or `NACK`
- Consider it as `NACK` and resend
- Problem
  - How can the receiver, which has just sent an `ACK`, know that the incoming data is a re-sent old data instead of a new packet?
- Solution
  - Use **sequence number**
    - Sender sends `pkt0`, `pkt1`
    - Receiver sends `ack0`, `ack1`

> To this point, the `NACK` is actually unnecessary
> > sender sends `pkt0` (success)
> > receiver replies `ack0`
> > sender sends `pkt1` (fail)
> > receiver still replies `ack0`

### Resolving Packet Loss

- Set retransmission timer
  - the timer estimates a timeout interval

### Improving Performance

- Pipelining
- Sender
  1. Transmit packets in a sliding window and start a timer
     - `[0,1,2,3],4,5,6,7,8,9`
     - each number is a packet id
  2. If receives `ACK` in correct order, then move the window forward
     - On receiving `ack0`
     - `0,[1,2,3,4],5,6,7,8,9`
     - Immediately send `pkt4`
  3. If `ACK` not in order, then do not move the window
- Receiver
  1. Also has a sequence of packet numbers, indicating the expected order of incoming packets
  2. If receives a packet in the expected order, then returns `ack` and move the window forward
  3. Otherwise the window is not moved
