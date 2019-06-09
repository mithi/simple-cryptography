#--------
# generate mnemonic words from a random sequence of bits.
#--------

# 1. Create a random sequence (entropy) of 128/160/192/224/256 bits.
# 2. Compute the SHA256 hash of the random sequence.
#        - Take the first (entropy-length/32) bits of its hash
#          as the checksum.
# 3. Concatenate the random sequence and the checksum.
# 4. Divide the result into sections of 11 bits.
# 5. Map each 11-bit value to a word from the predefined
#        dictionary of 2048 words.
# Print the mnemonic words in the correct order.

# IMPORTANT NOTE:
# bitwise operations are not defined on byte sequences—regardless
# of how much sense it would make to have them on a sequence of bytes.

# Entropy (bits)  Checksum (bits)     Mnemonic length (words)
# 128     4   12
# 160     5   15
# 192     6   18
# 224     7   21
# 256     8   24

import secrets
import hashlib
import words
import testmnemonic
import random

lenchecksum = {
    128: 4,
    160: 5,
    192: 6,
    224: 7,
    256: 8,
}


def generate_mnemonic(rsequence):

    lenseq = len(rsequence) * 8

    # random sequence in binary string
    i = int.from_bytes(rsequence, byteorder='big')
    entropy = bin(i)[2:]

    while (len(entropy) < lenseq):
        entropy = '0' + entropy

    # checksum in binary string
    h = hashlib.sha256()
    h.update(rsequence)

    c = int.from_bytes(h.digest(), byteorder='big')
    checksum = bin(c)[2:]

    while (len(checksum) < 256):
        checksum = '0' + checksum

    lencheck = lenchecksum[lenseq]
    checksum = checksum[:lencheck]

    # final binary string
    final_string = entropy + checksum

    # get mnemonic words
    mnemonic_words = []
    for i in range(0, len(final_string), 11):
        b = final_string[i:(i + 11)]
        x = int(b, 2)
        mnemonic_words.append(words.english_words[x])

    return mnemonic_words


if __name__ == "__main__":

    # --------------
    # Tests
    # --------------
    print("testing...", end="")

    testcases = testmnemonic.test_cases()
    random.shuffle(testcases)

    for i, (random_sequence, correct_mnemonic_words) in enumerate(testcases):

        mnemonic_words = generate_mnemonic(random_sequence)
        assert mnemonic_words == correct_mnemonic_words

    print("test complete. \n")

    # --------------
    # generate mnemonic words from a random sequence of bits.
    # --------------
    print("\nNew mnemonic! \n")
    nbytes = 32 # 256 bits
    random_sequence = secrets.token_bytes(nbytes)
    mnemonic_words = generate_mnemonic(random_sequence)

    for word in mnemonic_words:
        print(word)

    print()
