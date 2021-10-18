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

## Congestion Control Mechanism

1. Detect congestion
2. Reduce impact of congestion

### Limit Data Rate

- Window size is used to limit data rate
- Larger window means higher efficiency
- and higher risk of congestion
  - Congestion window `cwnd`

### Perceive Congestion

- indicators
  - duplicate `ack`s
    - perhaps the buffer of some random router is full so the packet is dropped
  - timeout events
    - slowa

### Congestion Algorithm

- Tentatively increase window size
- If congestion occurs, then cut the window size

#### Slow Start

- Sender
  - Set `cwnd = 1`
  - Double `cwnd` every time a transmission succeeds
    - termed as Round-Trip Time RTT
  - Grows exponentially but is somehow referred to as 'slow' start

#### Congestion Avoidance

- Set slow start threshold `ssthresh`
- If `cwnd >= ssthresh`
  - stop slow start
  - enter congestion avoidance mode
  - `cwnd = cwnd + 1` for each RTT

#### On Timeout Events

1. Drop `cwnd = 1`
2. Enter slow start mode
3. Set `ssthresh = cwnd / 2`

#### On Duplicated ACK Events

- Duplicated ACK is considered a better situation than Timeout
  - since the sender is still able to receive data from receiver
  - at least something can be sent, instead of getting lost

##### TCP Tahoe

1. Set `cwnd = 1`
2. Enter slow start
3. `ssthresh = cwnd / 2`

##### TCP Reno

1. `ssthresh = cwnd / 2`
2. Set `cwnd = ssthresh`
3. Enter Congestion Avoidance

### Estimating RTT Timeout

$$EstimatedRTT = (1-\alpha)\cdot EstimatedRTT + \alpha \cdot SampledRTT$$

- Typical $\alpha = 0.125$

$$ TimeoutInterval = EstimatedRTT + 4 \cdot DevRTT $$

where $DevRTT$ is an estimated deviation RTT and serves as a safety margin

### Explicit Congestion Notification

- Modern improved TCP supports ECN
- Requires router involvements
  - routers explicitly acknowledges senders
