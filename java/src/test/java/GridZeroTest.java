import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class GridZeroTest {
    //test([[1, 1], [0, 0]], 2)
    //test([[1, 1, 1], [1, 0, 0], [1, 0, 1]], -1)
    @Test
    public void testAnswerTwo() {
        final int[][] matrix = {{1,1},{0,0}};
        final int answer = GridZero.answer(matrix);
        assertEquals(2, answer);
    }

    @Test
    public void testAnswerThree() {
        final int[][] matrix = {{1,1,1},{1,0,0},{1,0,1}};
        final int answer = GridZero.answer(matrix);
        assertEquals(-1, answer);
    }

    @Test
    public void testAnswerThree1() {
        final int[][] matrix = {{1,1,0},{1,0,1},{0,1,1}};
        final int answer = GridZero.answer(matrix);
        assertEquals(2, answer);
    }

    @Test
    public void testAnswerThree2() {
        final int[][] matrix = {{0,1,0},{1,1,1},{0,1,0}};
        final int answer = GridZero.answer(matrix);
        assertEquals(1, answer);
    }

    @Test
    public void testAnswerThree3() {
        final int[][] matrix = {{0,0,1},{0,0,1},{1,1,1}};
        final int answer = GridZero.answer(matrix);
        assertEquals(1, answer);
    }

    @Test
    public void testInvertebility() {
        for(int matrixSize = 2; matrixSize <= 15; matrixSize++) {
            final int[][] matrix = new int[matrixSize][matrixSize];
            final int answer = GridZero.answer(matrix);
        }
        //final int[][] matrix = {{0,0,1},{0,0,1},{1,1,1}};
        //final int answer = GridZero.answer(matrix);
        //assertEquals(-1, answer);
    }

    @Test
    public void testKernel() {
        for (int i = 2; i <= 15; i++) {
            GridZero.answer(createMatrix(i));
        }

    }


    private int[][] createMatrix(int size) {
        int[][] matrix = new int[size][size];
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                matrix[i][j] = 1;
            }
        }
        return matrix;
    }
}
