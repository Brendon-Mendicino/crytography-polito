#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/bn.h>
#include <openssl/err.h>

#define ENCRYPT 1
#define DECRYPT 0

#define BUFFER_LEN (1024)

void handle_errors(void)
{
    ERR_print_errors_fp(stdout);
    abort();
}

void do_encrypt(FILE *input, FILE *output, EVP_CIPHER_CTX *ctx)
{
    uint8_t buffer[BUFFER_LEN];
    uint8_t ciphertext[BUFFER_LEN + EVP_MAX_BLOCK_LENGTH];
    int32_t n_read;
    int32_t ciphertext_len;

    while ((n_read = fread(buffer, sizeof(uint8_t), BUFFER_LEN, input)) > 0)
    {
        printf("bytes read: %d\n", n_read);

        if (!EVP_CipherUpdate(ctx, ciphertext, &ciphertext_len, buffer, n_read))
            handle_errors();

        printf("ciphertext lenght: %d\n", ciphertext_len);

        if (fwrite(ciphertext, sizeof(uint8_t), ciphertext_len, output) < ciphertext_len)
        {
            fprintf(stderr, "Error writing the output file\n");
            abort();
        }
    }

    EVP_CipherFinal_ex(ctx, ciphertext, &ciphertext_len);

    if (fwrite(ciphertext, sizeof(uint8_t), ciphertext_len, output) < ciphertext_len)
    {
        fprintf(stderr, "Error writing the output file\n");
        abort();
    }
}

int main()
{
    uint8_t key[] = "d35db7e39ebbf3d001083105d35db7e39ebbf3d001083105";
    uint8_t iv[] = "d35db7e39ebbf3d001083105d35db7e39ebbf3d001083105";

    // Load the human readable error strings for libcrypto
    ERR_load_crypto_strings();
    // Load all digest and cipher algorithms
    OpenSSL_add_all_algorithms();

    


    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!EVP_CipherInit(ctx, EVP_aes_192_cbc(), key, iv, DECRYPT))
        handle_errors();

    FILE *input = fopen("./ciphertext", "r");
    if (input == NULL)
        abort();

    
    do_encrypt(input, fopen("out", "w"), ctx);
    fflush(stdout);
    printf("\n");

    EVP_CIPHER_CTX_free(ctx);

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    // Remove error strings
    ERR_free_strings();

    return 0;
}
