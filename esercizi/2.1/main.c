// Write a program in C that, using the OpenSSL library, encrypts the content of a file
// using a user-selected algorithm. The filename is passed as the first parameter from the command line,
// and the algorithm is passed as the second parameter and must be an OpenSSL-compliant string (e.g.,
// aes-128-cbc or aes-256-ecb)

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
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

void init(uint8_t *iv, uint8_t *key, EVP_CIPHER_CTX **ctx) {
    
    // Load the human readable error strings for libcrypto 
    ERR_load_crypto_strings();
    // Load all digest and cipher algorithms
    OpenSSL_add_all_algorithms();

    // init PRNG
    if (RAND_load_file("/dev/random", BLOCK_SIZE) != BLOCK_SIZE) {
        handle_errors();
    }

    init_iv(iv);
    init_symmetric_key(key);

    if ((*ctx = EVP_CIPHER_CTX_new()) == NULL) {
        handle_errors();
    }

}

void deinit(EVP_CIPHER_CTX *ctx) {

    EVP_CIPHER_CTX_free(ctx);

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

int main(int argc, char **argv) {

    uint8_t iv[BLOCK_SIZE];
    uint8_t key[BLOCK_SIZE];

    EVP_CIPHER_CTX *ctx;

    init(iv, key, &ctx);

    const EVP_CIPHER *cipher = get_cipher(argc, argv);
    FILE *input = get_input_file(argc, argv);

    ctx = EVP_CIPHER_CTX_new();

    EVP_CipherInit(ctx, EVP_aes_128_cbc(), key, iv, ENCRYPT);

    FILE *output = fopen("./encrypted", "w");
    do_encrypt(input, output, ctx);


    fclose(input);
    fclose(output);
    deinit(ctx);


    // As a test read the ecrypted file and output it to stdout
    ctx = EVP_CIPHER_CTX_new();
    EVP_CipherInit(ctx, cipher, key, iv, DECRYPT);
    do_encrypt(fopen("./encrypted", "r"), stdout, ctx);
    fflush(stdout);

    return 0;
}