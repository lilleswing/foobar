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
}
