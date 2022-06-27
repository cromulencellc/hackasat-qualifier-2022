#include <assert.h>
#include <errno.h>
#include <limits.h>   // for CHAR_BIT
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// Debug includes
#include "binbin.h"

#define HARDEST_ROT_PATH "hardest_rotations.nums"

#define NUM_LEVELS 3
// #define MAX_NUM_GUESSES (UINT16_MAX - 535)
#define MAX_NUM_GUESSES 100

// #define HARDEST_SIZE (UINT16_MAX+1)
#define HARDEST_SIZE UINT16_MAX

#define GET_RAND_NUM ((uint16_t)rand() % (UINT16_MAX))
#define GET_RAND_ROT ((uint16_t)rand() % 15)

// Global Variables
unsigned int seed;

static inline uint16_t rotl16 (uint16_t n, unsigned int c){
    const unsigned int mask = (CHAR_BIT*sizeof(n) - 1);  // assumes width is a power of 2.

    // assert ( (c<=mask) &&"rotate by type width or more");
    c &= mask;
    return (n<<c) | (n>>( (-c)&mask ));
}

static inline uint16_t rotr16 (uint16_t n, unsigned int c){
    const unsigned int mask = (CHAR_BIT*sizeof(n) - 1);

    // assert ( (c<=mask) &&"rotate by type width or more");
    c &= mask;
    return (n>>c) | (n<<( ((-c))&mask ));
}

// return success as boolean, on success write result through *guess as uint16_t:
bool getGuess(uint16_t *guess){
    long num;
    char buf[1024] = {0};
    char *endptr = NULL;

    printf("Guess: ");
    fflush(stdout);

    *guess = 0;

    if(!fgets(buf, 1023, stdin)){
        LOG_ERR("Okay... Peace out\n");
        exit(1);
    }

    errno = 0; // reset error number

    num = strtol(buf, &endptr, 10);
    if(errno == ERANGE)
        return false;
    else if(endptr == buf)
        return false;
    else if(*endptr && *endptr != '\n') // Did not convert entire input
        return false;
    else if(num > UINT16_MAX)
        return false;
    // write result through the pointer passed

    *guess = (uint16_t)num;

    return true;
}

uint16_t get_hardest_start_num(uint8_t *hardest_lookup){
    if(!seed || !hardest_lookup)
        return GET_RAND_NUM;

    uint8_t difficulty = 0;
    uint16_t reg = 1;

    while(difficulty != 16){    // Bein lzy. Have a 50% chance you'll get something with 16 difficulty.
        reg = GET_RAND_NUM + 1;
        if(!reg)
            continue;
        difficulty = hardest_lookup[reg-1];
    }

    return reg;
}

void get_hardest_nums(uint8_t **hardest_lookup){
    if(seed == 0)
        return;

    long sz = 0;
    FILE *fp = NULL;

    *hardest_lookup = (uint8_t*)calloc(sizeof(uint8_t), HARDEST_SIZE);
    if (*hardest_lookup == NULL){
        printf("(Contact an admin) Could not allocate space. Bailing out...\n");

        LOG_ERR("Could not allocate space. Bailing out...\n");
        exit(-1);
    }

    memset(*hardest_lookup, sizeof(uint8_t), HARDEST_SIZE);

    fp = fopen(HARDEST_ROT_PATH, "r");

    if(fp == NULL){
        printf("Could not open file %s.\n", HARDEST_ROT_PATH);
        LOG_ERR("Could not open file %s.\n", HARDEST_ROT_PATH);
        *hardest_lookup = NULL;
        return;
    }

    fseek(fp, 0L, SEEK_END);
    sz = ftell(fp);

    // 2 characters + space per number == (# of nums * 3)
    assert(sz == (HARDEST_SIZE*3));

    rewind(fp);

    char num[3] = {0};
    // Read in numbers in the format "%02d "
    for(unsigned int i = 0; i < HARDEST_SIZE; i++){
        fread(num, sizeof(uint8_t), 2, fp);
        fseek(fp, 1, SEEK_CUR);
        (*hardest_lookup)[i] = (uint8_t)atoi(num);
        if((*hardest_lookup)[i] > 16){
            printf("Bad difficulty for %d. Bailing out...\n", i);
            LOG_ERR("Bad difficulty for %d. Bailing out...\n", i);
            exit(-1);
        }
        // LOG("%hhu ", (*hardest)[i]);
    }

    LOG("\n");

    return;
}

bool lvl1(uint16_t *reg, uint16_t *num_guesses, uint8_t *hardest_lookup){
    printf("Level 1. FIGHT\n\n");

    uint16_t rot = GET_RAND_ROT + 1, guess = 0;
    LOG("rot: %hu\n", rot);

    *reg = get_hardest_start_num(hardest_lookup);

    for(; *num_guesses < MAX_NUM_GUESSES && *reg != 0; (*num_guesses)++){
        if(!getGuess(&guess)){
            LOG_ERR("Please provide a valid number between (0-%d)\n", UINT16_MAX);
            printf("Please provide a valid number between (0-%d)\n", UINT16_MAX);
            continue;
        }

        *reg = rotl16(guess, rot) ^ *reg;

        // printf("Z: %hu\n", U16_COUNT_ZEROS(*reg));
        if(!hardest_lookup)
            printf("Got %hu\n", guess);
        else if(*reg != 0)
            printf("%hhu\n", hardest_lookup[(*reg)-1]);

        // printf("Z: %hu\n", U16_COUNT_ZEROS(*reg));
        LOG("Guess: " U16_TO_BINARY_PATTERN " Reg: " U16_TO_BINARY_PATTERN "\n", U16_TO_BINARY(guess), U16_TO_BINARY(*reg));
    }

    if(!(*reg))
        return true;

    return false;
}

bool lvl2(uint16_t *reg, uint16_t *num_guesses, uint8_t *hardest_lookup){
    printf("Level 2. FIGHT\n\n");
    
    uint16_t rot, guess;

    *reg = get_hardest_start_num(hardest_lookup);;

    for(; *num_guesses < MAX_NUM_GUESSES && *reg != 0; (*num_guesses)++){
        if(!getGuess(&guess)){
            printf("Please provide a valid number between [0-%d]\n", UINT16_MAX);
            LOG_ERR("Please provide a valid number between [0-%d]\n", UINT16_MAX);
            continue;
        }

        rot = rand() % 16;

        *reg = rotl16(guess, rot) ^ (*reg);

        // printf("Z: %hu\n", U16_COUNT_ZEROS(*reg));
        if(!hardest_lookup)
            printf("Got %hu\n", guess);
        else if(*reg != 0)
            printf("%hhu\n", hardest_lookup[(*reg)-1]);

        LOG("rot: %hd", rot);
        LOG("Guess: " U16_TO_BINARY_PATTERN " Reg: " U16_TO_BINARY_PATTERN "\n", U16_TO_BINARY(guess), U16_TO_BINARY(*reg));
    }

    if(!(*reg))
        return true;

    return false;
}

bool lvl3(uint16_t *reg, uint16_t *num_guesses, uint8_t *hardest_lookup){
    if(!hardest_lookup){
        printf("Please make sure %s file is present and formatted properly.\n", HARDEST_ROT_PATH);
        return false;
    }

    if(!seed)
        return lvl2(reg,num_guesses,hardest_lookup);

    printf("Level 3. FIGHT\n\n");

    uint16_t guess, possible_num, idx, curr_difficulty, hardest_difficulty;
    uint16_t rotations[17] = {0};

    *reg = get_hardest_start_num(hardest_lookup);

    for(; *num_guesses < MAX_NUM_GUESSES && *reg != 0; (*num_guesses)++){
        if(!getGuess(&guess)){
            printf("Please provide a valid number between [0-%d]\n", UINT16_MAX);
            LOG_ERR("Please provide a valid number between [0-%d]\n", UINT16_MAX);
            continue;
        }

        // rotations[0] = 0;
        // rotations[1] = 0;
        *((uint32_t*)rotations) = 0;

        hardest_difficulty = 0;
        curr_difficulty = 0;
        for(idx=0; idx < 16; idx++){

            guess = rotl16(guess, 1);
            possible_num = *reg ^ guess;
            if(!possible_num)
                continue;

            // printf("reg: %u | possible_num: %u | curr_difficulty: %u \n", *reg, possible_num, curr_difficulty);

            // (UINT16_MAX+1) # of elements. possible_num is uint16_t type. 
            // No risk of overflow
            curr_difficulty = hardest_lookup[possible_num-1];

            if(rotations[0] > 16)
                exit(-1);
            
            if(curr_difficulty > hardest_difficulty){
                hardest_difficulty = curr_difficulty;
                rotations[0] = 0;
                rotations[rotations[0]+1] = possible_num;
                rotations[0] += 1;
            }
            else if(curr_difficulty == hardest_difficulty){
                rotations[rotations[0]+1] = possible_num;
                rotations[0] += 1;
            }
        }

        LOG("Hardest difficulty: %d\n", hardest_difficulty);

        if(!rotations[0]){
            *reg = rotations[1];
            return true;
        }
        else
            *reg = rotations[(rand() % rotations[0]) + 1];

        if(*reg != 0)
            printf("%hhu\n", hardest_lookup[(*reg)-1]);
        else
            return true;

        // LOG("Z: %hu\n", U16_COUNT_ZEROS(*reg));
        LOG("Guess: " U16_TO_BINARY_PATTERN " Reg: " U16_TO_BINARY_PATTERN "\n", U16_TO_BINARY(guess), U16_TO_BINARY(*reg));
    }

    if(!(*reg))
        return true;

    return false;
}

void hard_reset(){
    char *flag = getenv("FLAG");
    if(flag == NULL){
        flag = "flag{fake_flag}";
    }

    printf("Resetting satellite: %s\n", flag);

    return;
}

void assignSeed(){
    char *seed_s, *endptr=NULL;

    seed_s = getenv("SEED");

    if (!seed_s)
        seed_s = "0";

    errno = 0; // reset error number
    seed = (unsigned int)strtoll(seed_s, &endptr, 10);

    if(errno == ERANGE)
        seed = 0;
    else if(endptr == seed_s)
        seed = 0;
    else if(*endptr && *endptr != '\n') // Did not convert entire input
        seed = 0;
    else if(seed > UINT_MAX)
        seed = 0;

    srand(seed);
}

int main(){
    uint16_t reg = 0, num_guesses = 0;
    uint8_t *hardest_lookup = NULL;

    bool (*levels[NUM_LEVELS])(uint16_t*, uint16_t*, uint8_t*) = {lvl1,lvl2,lvl3};

    assignSeed();

    get_hardest_nums(&hardest_lookup);

    for(int lvl_idx = 0; lvl_idx < NUM_LEVELS; lvl_idx += 1){
        (*levels[lvl_idx])(&reg, &num_guesses, hardest_lookup);
        if (reg != 0){
            printf("Reset failed on round %d\n", lvl_idx+1);
            exit(0);
        }
        else{
            printf("Reset sequence round %d completed.\n", lvl_idx+1);
        }
    }

    if(reg == 0 && num_guesses < MAX_NUM_GUESSES){
        hard_reset();
        return 0;
    }

    return 1;
}