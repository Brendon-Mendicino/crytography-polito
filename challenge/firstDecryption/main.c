#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>


#define ENCRYPT (1)
#define DECRYPT (0)
#define BUFFER_LEN (1 << 10)
#define BLOCK_SIZE (128 / 8)

void handle_errors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

void init_iv(uint8_t *iv) {
    if (RAND_bytes(iv, BLOCK_SIZE) != 1) {
        handle_errors();
    }
}
 
void init_symmetric_key(uint8_t *key) {
    if (RAND_priv_bytes(key, BLOCK_SIZE) != 1) {
        handle_errors();
    }
}

void init() {
    
    // Load the human readable error strings for libcrypto 
    ERR_load_crypto_strings();
    // Load all digest and cipher algorithms
    OpenSSL_add_all_algorithms();

    // init PRNG
    if (RAND_load_file("/dev/random", BLOCK_SIZE) != BLOCK_SIZE) {
        handle_errors();
    }

}

void deinit() {

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    // Remove error strings
    ERR_free_strings();
}

const EVP_CIPHER *get_cipher(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Wrong usage: %s: INPUT CIPHER_NAME", argv[0]);
        abort();
    }

    const EVP_CIPHER *cipher;
    if ((cipher = EVP_get_cipherbyname(argv[2])) == NULL) {
        fprintf(stderr, "Wrong cipher name!");
        abort();
    }

    return cipher;
}

FILE *get_input_file(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Wrong usage: %s: INPUT CIPHER_NAME", argv[0]);
        abort();
    }

    FILE *input;
    if ((input = fopen(argv[1], "r")) == NULL) {
        fprintf(stderr, "File: \"%s\" does not exists!", argv[1]);
        abort();
    }

    return input;
}

void do_encrypt(FILE *input, FILE *output, EVP_CIPHER_CTX *ctx) {
    uint8_t buffer[BUFFER_LEN];
    uint8_t ciphertext[BUFFER_LEN + EVP_MAX_BLOCK_LENGTH];
    int32_t n_read;
    int32_t ciphertext_len;

    while ((n_read = fread(buffer, sizeof(uint8_t), BUFFER_LEN, input)) > 0) {
        printf("bytes read: %d\n",n_read);

        if (!EVP_CipherUpdate(ctx, ciphertext, &ciphertext_len, buffer, n_read)) {
            handle_errors();
        }

        printf("ciphertext lenght: %d\n", ciphertext_len);

        if (fwrite(ciphertext, sizeof(uint8_t), ciphertext_len, output) < ciphertext_len) {
            fprintf(stderr, "Error writing the output file\n");
            abort();
        }
    }

    EVP_CipherFinal_ex(ctx, ciphertext, &ciphertext_len);

    if (fwrite(ciphertext, sizeof(uint8_t), ciphertext_len, output) < ciphertext_len) {
        fprintf(stderr, "Error writing the output file\n");
        abort();
    }
}

void hex2bn(uint8_t *hex, uint8_t *binary) {

    for (int i = 0; i < strlen(hex)/2; i++) {
        sscanf(&hex[2*i],"%2hhx", &binary[i]);
    }
}

int main(int argc, char **argv) {

    const uint8_t *key_hex = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF";
    const uint8_t *iv_hex = "11111111111111112222222222222222";

    uint8_t key[64];
    uint8_t iv[32];
    
    hex2bn(key_hex, key);
    hex2bn(iv_hex, iv);

    init();
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    EVP_CipherInit(ctx, EVP_chacha20(), key, iv, DECRYPT);

    uint8_t buffer[BUFFER_LEN];
    uint8_t plain[BUFFER_LEN + EVP_MAX_BLOCK_LENGTH];
    uint32_t plain_len;
    uint32_t n_read; 
    
    FILE *in = fopen("./message.enc", "r");
    do_encrypt(in, stdout, ctx);
    fflush(stdout);
    printf("\n");


    deinit();

    return 0;
}