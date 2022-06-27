
!
!  print_array is not used except to debug the code
SUBROUTINE PRINT_ARRAY(rows, cols, mat1, mat2, res)
      IMPLICIT NONE
      INTEGER, INTENT(IN) :: rows
      INTEGER, INTENT(IN) :: cols
      INTEGER*8, INTENT(IN), DIMENSION(3,3)  :: mat1
      INTEGER*8, INTENT(IN), DIMENSION(3,3)  :: mat2
      INTEGER*8, INTENT(IN), DIMENSION(3,3)  :: res

      CHARACTER :: sporx, sporeq
      INTEGER*2 :: i

      PRINT *," "
      DO i = 1, rows
            IF (i == 2) THEN 
                  sporx = 'X'
                  sporeq = '='
            ELSE
                  sporx = ' '
                  sporeq = ' '
            END IF
            PRINT '("F|",I10,I10,I10," | ",A," |",I10,I10,I10," |  ",A," |",I10,I10,I10," |" )',& 
                  mat1(i,1), mat1(i,2), mat1(i,3), sporx, &
                  mat2(i,1), mat2(i,2), mat2(i,3), sporeq, &
                  res(i,1), res(i,2), res(i,3)
      END DO
      PRINT *," "

END SUBROUTINE PRINT_ARRAY

!
!  multiply two 3x3 matricies and return the result to the
!  caller.
SUBROUTINE MAT_MULT(mat1, mat2, result)
      IMPLICIT NONE
      INTEGER*8, INTENT(IN), DIMENSION(3,3) :: mat1
      INTEGER*8, INTENT(IN), DIMENSION(3,3) :: mat2
      INTEGER*8, INTENT(INOUT), DIMENSION(3,3):: result

      INTEGER i, j, k
      ! PRINT *, "FORTRAN: called from C"

      DO i = 1, 3
            DO j = 1, 3
                  result(i,j) = 0
                  DO k = 1, 3
                        result(i,j) = result(i,j) + (mat1(i,k) * mat2(k,j))
                  ENDDO
            ENDDO
      ENDDO
      ! CALL PRINT_ARRAY(3, 3, mat1, mat2, result)

      ! PRINT *, "FORTRAN: return to C"
END SUBROUTINE MAT_MULT



