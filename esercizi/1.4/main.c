// Using OpenSSL, generate two 32-bit integers (int), multiply them (modulo 2^32) and
// print the result.

#include <stdio.h>
#include <openssl/rand.h>
#include <openssl/err.h>
#include <openssl/bn.h>


#define BLOCK_SIZE (128)


void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

void init_rand(void) {
    if (RAND_load_file("/dev/random", 128) != 128) {
        handle_errors();
    }
}

int main(int argc, char **argv) {

    BN_CTX *ctx = BN_CTX_new();

    BIGNUM *num1 = BN_new();
    BIGNUM *num2 = BN_new();
    BIGNUM *res = BN_new();
    BIGNUM *mod = BN_new();

    BN_hex2bn(&mod, "100000000");

    BN_rand(num1, 32, -1, 1);
    BN_rand(num2, 32, -1, 1);

    BN_mod_mul(res, num1, num2, mod, ctx);

    printf("num1: ");
    BN_print_fp(stdout, num1);
    printf("\n");
    
    printf("num2: ");
    BN_print_fp(stdout, num2);
    printf("\n");
    
    printf("mod: ");
    BN_print_fp(stdout, mod);
    printf("\n");

    printf("res: ");
    BN_print_fp(stdout, res);
    printf("\n");




    BN_free(num1);
    BN_free(num2);
    BN_free(res);
    BN_free(mod);

    return 0;
}