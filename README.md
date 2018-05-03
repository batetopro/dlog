This is my solution of a security competition.
The description could be found here:
https://crypto.iti.kit.edu/fileadmin/User/Lectures/Sicherheit/SoSe17/Sicherheit_Wettbewerb.pdf

It is a solution of the discrete logarithm operation, on which computational hardness is based the most of the security.
The modern operations are done with a recomendation of 1024-bit prime numbers, so that the real security comes from the
computational hardness of computing of the factorization of the prime number minus 1, for which quantum computers are supposed to be the key,
whuch does not exist yet. So this one uses a little bit cracked version of the cryptography. 

In its most rude form it is the operation, whcih breaks the El-Gamal cryptography:
https://en.wikipedia.org/wiki/ElGamal_encryption

The package includes implementation of the following algorithms, which all are checked for validity:
  - Calculation of the order of a group generator (using BinaryHeap, so that the complexity is NlogN)
  - Baby-Steps-Giant-Steps
  - Pollard's Rho Cycle finding:
     - Floyd's algorithm
     - Brent's algorithm
  - Pohling Hellman algorithm

More information about Pollard Rho algorithm could be found here:
https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch14.pdf

Performance:
The implementation of the Pollard's Rho uses almost no RAM compared to the Baby-Steps-Giant-Steps (which uses a lookup table of the size of several GBs).
The average time for cacluation of the diskret logratihm takes average 8.5 minutes and total time less than 3 hours with calculations based on the test case.











Some history:

The development of a the Baby-Steps-Giant-Steps and Pohling Hellman algorithm was enough to have excellent on the exam.
However I did not understood about that there was a competition until at some moment they presented some solutions, on which I was half-asleep.
I also did not have an exam permission, so I decided to coin one and to prepare for the exam by reading the versions which were given from 2009 until 2015.
However the exam was an one-hour nightmare with 5 problems, no test and they gave 50% new tasks, which were not given in previous versions. So it was a nightmare.
I decided to start working on the problem immediately after the exam (on 02.08.) and the full solution was ready on 10.08 - only a week later.
