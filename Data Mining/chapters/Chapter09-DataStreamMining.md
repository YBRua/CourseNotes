# Mining Data Streams

## Data Streams

- In many data mining scenarios, we do not know the entire data set in advance
  - Instead, the data come in streams and change with time
  - Can think of data as **infinite** and **non-stationary**

### Stream Model

- Input elements enter at a rate, at one or more input ports
  - Elements of the stream is called **tuples**
- The system **cannot** sotre the entire stream

#### SGD as Stream Algorithm

- SGD is a type of stream algorithm
- In machine learning this is referred to as **online learning**
