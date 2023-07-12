// Write a program in C that, using the OpenSSL library, generates two 128-bit random
// strings. Then, it XOR them (bitwise/bytewise) and prints the result on the standard output as a hex
// string.

#include <stdio.h>
#include <openssl/rand.h>
#include <openssl/err.h>

#define MAX_BYTE_LEN 64

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(){
    uint8_t str1[MAX_BYTE_LEN];
    uint8_t str2[MAX_BYTE_LEN];

    if(RAND_load_file("/dev/random", MAX_BYTE_LEN) != MAX_BYTE_LEN)
        handle_errors();

    if(!RAND_bytes(str1, MAX_BYTE_LEN))
        handle_errors();

    if(!RAND_bytes(str2, MAX_BYTE_LEN))
        handle_errors();

    printf("str1 generated: ");
    for(int i = 0; i < MAX_BYTE_LEN; i++)
        printf("%02x-", str1[i]);
    printf("\n");

    printf("str2 generated: ");
    for(int i = 0; i < MAX_BYTE_LEN; i++)
        printf("%02x-", str2[i]);
    printf("\n");

    // strings are initialized
    printf("str1 xor str2: ");
    for (int i = 0; i < MAX_BYTE_LEN; i++) {
        printf("%02x-", str1[i] ^ str2[i]);
    }
    printf("\n");

    return 0;

}