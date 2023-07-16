#include <openssl/bn.h>
#include <string.h>


int main() 
{
    BIGNUM *rand1 = BN_new();
    BIGNUM *rand2 = BN_new();
    BIGNUM *k1 = BN_new();
    BIGNUM *k2 = BN_new();

    uint8_t buffer1[strlen("633b6d07651a09317a4fb4aaef3f7a55d03393521e81fb631126ed9e8ea710f6639deb9290eb760b905aebb475d3a1cfd29139c189328422124e77574d258598")/2];

    uint8_t buffer2[strlen("633b6d07651a09317a4fb4aaef3f7a55d03393521e81fb631126ed9e8ea710f6639deb9290eb760b905aebb475d3a1cfd29139c189328422124e77574d258598")/2];
    uint8_t buffer3[strlen("633b6d07651a09317a4fb4aaef3f7a55d03393521e81fb631126ed9e8ea710f6639deb9290eb760b905aebb475d3a1cfd29139c189328422124e77574d258598")/2];
    uint8_t buffer4[strlen("633b6d07651a09317a4fb4aaef3f7a55d03393521e81fb631126ed9e8ea710f6639deb9290eb760b905aebb475d3a1cfd29139c189328422124e77574d258598")/2];

    BN_hex2bn(&rand1, "633b6d07651a09317a4fb4aaef3f7a55d03393521e81fb631126ed9e8ea710f6639deb9290eb760b905aebb475d3a1cfd29139c189328422124e77574d258598");

    BN_hex2bn(&rand2, "9205d8b5fa8597b622f4bd2611cf798cdb4a2827bbd331567416dfcbf561a79d18c26392f1cbc36d2b7719aa21078efe8b1a4f7d706ea47bc86830431250301e");


    BN_bn2bin(rand1, buffer1);
    BN_bn2bin(rand2, buffer2);

    size_t len = strlen( "9205d8b5fa8597b622f4bd2611cf798cdb4a2827bbd331567416dfcbf561a79d18c26392f1cbc36d2b7719aa21078efe8b1a4f7d706ea47bc86830431250301e") / 2;

    for (int i = 0; i < len; i++) {
        buffer3[i] = buffer1[i] | buffer2[i];
        buffer4[i] = buffer1[i] & buffer2[i];

        buffer1[i] = buffer3[i] ^ buffer4[i];

        printf("%02x%s", buffer1[i], i != len - 1 ? "-" : "");
    }


    BN_free(rand1);
    BN_free(rand2);
    BN_free(k1);
    BN_free(k2);

    return 0;
}