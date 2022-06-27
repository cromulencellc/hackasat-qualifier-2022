
// -----------------------------------------------------------
// compute.c is a wrapper for a FORTRAN matrix multiplication
// subroutine which simply multiplies two 3x3 matricies and 
// returns the result.
// There are several functions in this file used to verify
// the challenge but the encrypt_it function is what interfaces
// with both python and fortan.

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

//
// The EncodeMatrix is the 3x3 matrix used to encode the phrase
// The DecodeMatrix is the inverse of the EncodeMatrix used to
// decode an encoded phrase.
//   EM * phrase = encoded phrase
//   encoded phrase * DM = phrase
const long EncodeMatrix[3][3] = {{-3,-3,-4},{0,1,1},{4,3,4}};
const long DecodeMatrix[3][3] = {{1,0,1},{4,4,3},{-4,-3,-3}};

long * encrypt_it(long*);
void C_encode_decode(long [3][3], long phr[3][3]);
void make_F_array(long [3][3], long [3][3]);
void make_C_array(long [3][3], long [3][3]);
extern void mat_mult_(long*, long*, long*);
void print_array(int, int, long *, char *);

void main(void)
{
    int i=2,j;

    printf("Hello from C\n");
 
    return;
}

//
// print 3x3 matrix to stdio
void print_array(int cols, int rows, long *array, char *label)
{
    long *ap = array;

    printf("%s\n",label);
    for(int i=0; i<cols; ++i,ap+=3)
    {
        printf("C: |");
        for (int j=0; j<rows; ++j)
        {
            printf(" %ld ",*(ap+j) );
        }
        printf(" |\n");
    }
    printf("\n");
}

//
// Encode and then decode the phrase to verify data operations
// are correct.
void C_encode_decode(long mat[3][3], long phr[3][3])
{
    long result[3][3];
    long *r = &result[0][0];
    long solve[3][3];

    //printf("\n---------------------\n");
    //printf("  C Solution\n");
    //print_array(3,3,(long *)phr,"Start:");
    for(int i=0; i<3; ++i)
    {
        for(int j=0; j<3; ++j)
        {
            result[i][j] = 0;
            for(int k=0; k<3; ++k)
            {
                result[i][j] = result[i][j] + (EncodeMatrix[i][k]*phr[k][j]);
            }
        }
    }
    r = &result[0][0];
    //print_array(3,3,r,"C solution:");

    for(int i=0; i<3; ++i)
    {
        for(int j=0; j<3; ++j)
        {
            solve[i][j] = 0;
            for(int k=0; k<3; ++k)
            {
                solve[i][j] = solve[i][j] + (DecodeMatrix[i][k]*result[k][j]);
            }
        }
    }
    r = &solve[0][0];
    //print_array(3,3,r,"Decrypt:");
    //printf("---------------------\n");
}

//
// Convert a C ordered matrix to FORTRAN ordered
void make_F_array(long mat[3][3], long fmat[3][3])
{
    for(int c=0; c<3; ++c)
    {
        for(int r=0; r<3; ++r)
        {
            fmat[r][c] = mat[c][r];
        }
    }
    
}

//
// Convert a FORTRAN ordered matrix to a C ordered matrix
void make_C_array(long fmat[3][3], long mat[3][3])
{
    for(int c=0; c<3; ++c)
    {
        for(int r=0; r<3; ++r)
        {
            mat[r][c] = fmat[c][r];
        }
    }  
}

//
// convert character string phrase into it byte equivilent
void matrize_phrase(const void *phrase, long* result, int size)
{
    long *mp = (long *)phrase;
    long *rp = result;
    int sz = size;

    printf("Phrase size: %d\n",size);
    for(int i=0; i<size; ++i, ++mp)
    {
        printf("%ld, ", (long)(*mp));
    }
    printf(" \n");
    *rp = 0;  // only 8 chars in phase, pad matrix
}

long *encrypt_it( long *inphrase )
{
    long mat[3][3];
    long fmat[3][3];
    long fpharray[3][3];
    long (*pp)[3] = (void *)inphrase;
    long *result;

    // Allocate the matrix to pass the result back to python.
    result = malloc (9 * sizeof(long));
    if (result == NULL)
    {
        printf("ERROR: Could not allocate result array\n");
    }
    memset(result, 0, (9*sizeof(long)));

    // Solve problem in C space (for debug)
    C_encode_decode(mat, pp);

    // make a copy of encoder matrix for Fortran
    memcpy(mat,EncodeMatrix,(9*sizeof(long)));

    // make C orders arrays into F ordered arrays
    make_F_array(mat, fmat);
    make_F_array(pp, fpharray);
    //
    //Call to FORTRAN to multiply two 3x3 matricies.
    mat_mult_((long *)fmat, (long *)fpharray, (long *)result);

    //*** the problem here is that we don't convert the result
    //    matrix back to C order so the return to python is wrong.

    return result;
}
