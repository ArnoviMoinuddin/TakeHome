
## Setup 

To install packages before running script:

``` bash 
chmod +x install.sh
```

Run script to generate icons. This will take a user input for string and desired size then display and save a .png identicon:

```bash
python gen_identicon.py
```
   

To run unit tests (described below):
```bash
python unittests.py
```

### Objectives:

- Uniqueness: every input will generate a different identicon. Pixel pattern and color scheme are both determined by the SHA 256 hash values. This hash function is known to minimize possibility of collisions. No two users/strings will have the same identicon


- Repeateability: identicon consistently generated for same input string, so users' icons will not change
    - Consistency: identicon consistently generated for same input name, regardless of case (upper / lower) or special characters in input string


- Resizablility: size of icon set to 256 x 256, but can be as small as 8 x 8 and as large as necessary, as long as the size is a multiple of 8. Identicons maintain clarity and recognizability at every size of image. This works because we use 32 byte hash value which results in a square image when enforcing symmetry (64 pixels total = 8x8 image), instead of 64 byte hexadecimal hash value.
    - (originally included a function to resize image based on window size but that isn't a relevant use case so excluded)


- Appearance: every image is symmetrical and limited to use of three colors. Symmetry creates illusion of clarity and can sometimes resemble a face, body, or animal. 
    - In order to avoid the clashing of three colors on a small / finite scale, each color was given a different probability of selection such that two colors out of the three colors are predominant and the third be an accent to minimize chaos and better mimic an avatar. Therefore one color was assigned based on the criterion of being divisible by 17 (low probability), otherwise the color was picked through a parity condition (whether it is even or odd -- high probability) 


- Dissimilarity: Similar strings should yield equally as different identicons as dissimlar strings. "John" vs "Jon" should appear different in pattern and color scheme so that users can easily identify the owners of the identicons. 
    - I originally implemented a version which enforced a similarity constraint by using a phonetic hashing algorithm (soundex) and using SHA 256 to hash the soundex value to determine the colors so that similar sounding strings had the same color scheme. This generated a series of identicons which were different but looked similar in quick glance, defeating the pupose of the unique avatar (function excluded)


### Process:

- Input: String
- Output: PNG named after input
- get_hash(): 
    - input: initial string
    - returns SHA-256 hash value (32 byte length)
- get_color(): 
    - input: hash value from get_hash()
    - The first color uses the first three bytes of hash value, second color uses bytes 4-6, third uses bytes 7-9. Each color is a tuple of three elements (r,g,b)
    - returns three colors to set theme of identicon 
- get_color_array():
    - inputs: hash value from get_hash(), colors from get_color(), desired size (default: 256 x 256)
    - converts hash value to list of integers
    - creates a 8x4x3 numpy array where each element is the color of that pixel 
        - if hash integer divisible by 17: color 1
        - else if hash integer even: color 2
        - else if hash integer off: color 3
    - flips the array over y axis to ensure symmetry
    - concatenates flipped array and original array horizontally to create combined array
    - scales combined array to desired size using Kronecker product
    - returns scaled array 
- get_image():
    - inputs: initial string, desired size (default: 256 x 256, smallest possible: 8 x 8)
    - desired size must be multiple of 8
    - converts array from get_color_array() to image
    - returns and saves png named after input, shows image to user upon insput


### Unit Tests

- Tests to ensure:
    - different strings generate unique identicons
    - same strings generate the same identicons
        - regardless of case
        - regardless of sepcial charcacters
        - repeatable
