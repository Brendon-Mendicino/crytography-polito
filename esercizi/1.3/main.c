// Writes a program in C that, using the OpenSSL library, randomly generates the private
// key to be used for encrypting data with AES128 in CBC mode and the IV.
// Pay attention to selecting the proper PRNG for both the “private” key and IV.

#include <stdio.h>
#include <openssl/rand.h>
#include <openssl/err.h>
#include <openssl/bn.h>


#define BLOCK_SIZE (128)


void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

void get_iv(BIGNUM *iv) {
    // BN_rand() generates a cryptographically strong pseudo-random number 
    // of bits in length and stores it in rnd. If bits is less than
    // zero, or too small to accomodate the requirements specified by the
    // top and bottom parameters, an error is returned. If top is -1, the 
    // most significant bit of the random number can be zero. If top 
    // is 0, it is set to 1, and if top is 1, the two most significant bits 
    // of the number will be set to 1, so that the product of two such random 
    // numbers will always have 2*bits length. If bottom is true, the number 
    // will be odd. The value of bits must be zero or greater. 
    // If bits is 1 then top cannot also be 1.

    if (BN_rand(iv, BLOCK_SIZE * 8, -1, 1) != 1) {
        handle_errors();
    }
}

void get_private_key(BIGNUM *p_key) {

    if (BN_priv_rand(p_key, BLOCK_SIZE * 8, -1, 1) != 1) {
        handle_errors();
    }
}

int main() {

    if (RAND_load_file("/dev/random", BLOCK_SIZE) != BLOCK_SIZE) {
        handle_errors();
    }

    BIGNUM *iv = BN_new();
    BIGNUM *p_key = BN_new();


    get_iv(iv);
    get_private_key(p_key);

    BN_print_fp(stdout, iv);
    printf("\n");
    BN_print_fp(stdout, p_key);
    printf("\n");



    BN_free(iv);
    BN_free(p_key);

    return 0;

}