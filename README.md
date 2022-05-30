## Genetic Algorithm
A toy implementation of GA in Python

- HW after ***Intro to AI*** course
- implemented by Python
- supported optimized function with 2 variables
- Procedure：
  - define how to encode/decode 
  - generate 10 individuals
  - calculate fitness value and normalized it
  - select randomly via roulette wheel 
  - cross
    - two points cross
  - variation
    - one point cross
  - select 2-top descendants and select other 8 individuals randomly via roulette wheel 
  - repeat the above process until get the best fitness value (less than 1000 iterations)
