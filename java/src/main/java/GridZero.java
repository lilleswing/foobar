public class GridZero {

    private static boolean[][] makeEquations(int[][] a) {
        int size = a.length * a.length;
        boolean[][] matrix = new boolean[size][size + 1];

        for (int row = 0; row < a.length; row++) {
            for (int col = 0; col < a.length; col++) {
                int my_index = row * a.length + col;
                if (a[row][col] == 1) {
                    matrix[my_index][size] = true;
                }

                // mark the system of linear equations
                for (int i = 0; i < a.length; i++) {
                    int my_row = row * a.length + i;
                    int my_col = col + i * a.length;
                    matrix[my_index][my_row] = true;
                    matrix[my_index][my_col] = true;
                }
            }
        }
        return matrix;
    }


    public static int answer(int[][] matrix) {
        boolean[][] myEquations = makeEquations(matrix);
        //double[] answers = flatten(matrix);
        final GaussJordanElimination gaussJordanElimination = new GaussJordanElimination(myEquations);
        gaussJordanElimination.eliminate();
        gaussJordanElimination.display();

        int numMoves = 0;
        boolean[] moves = gaussJordanElimination.getMoves();
        for (int i = 0; i < myEquations.length; i++) {
            if (moves[i]) {
                numMoves += 1;
                int row = i / matrix.length;
                int col = i % matrix.length;
                flip(matrix, row, col);
            }
        }
        if (valid(matrix)) {
            return numMoves;
        }
        return -1;
    }

    private static boolean valid(int[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                if (matrix[i][j] == 1) {
                    return false;
                }
            }
        }
        return true;
    }

    private static void flip(int[][] matrix, int row, int col) {
        for (int i = 0; i < matrix.length; i++) {
            matrix[row][i] ^= 1;
            matrix[i][col] ^= 1;
        }
        matrix[row][col] ^= 1;
    }
}

class GaussJordanElimination {

    private boolean[][] matrix;
    private boolean[] moves;
    private boolean invertable;
    private int degreesOfFreedom = 0;

    public GaussJordanElimination(final boolean[][] matrix) {
        this.matrix = matrix;
        moves = new boolean[matrix.length];
        this.invertable = true;
    }

    private boolean setBit(int rowIndex, int colIndex) {
        if (matrix[rowIndex][colIndex]) {
            return true;
        }
        for (int i = rowIndex + 1; i < matrix.length; i++) {
            if (matrix[i][colIndex]) {
                xor(rowIndex, i);
                return true;
            }
        }
        return false;
    }

    private void xor(int rowIndex, int i) {
        for (int j = 0; j < matrix[0].length; j++) {
            matrix[rowIndex][j] = matrix[rowIndex][j] ^ matrix[i][j];
        }
    }

    public boolean eliminate() {
        int colIndex = 0;
        for (int rowIndex = 0; rowIndex < matrix.length; rowIndex++) {
            while (!setBit(rowIndex, colIndex)) {
                System.out.println("Matrix size: " + matrix.length + " not invertible");
                degreesOfFreedom++;
                this.invertable = false;
                colIndex++;
                if (colIndex >= matrix.length) {
                    return true;
                }
            }
            for (int j = 0; j < matrix.length; j++) {
                if (rowIndex == j) {
                    continue;
                }
                if (matrix[j][colIndex]) {
                    xor(j, rowIndex);
                }
            }
            colIndex++;
        }
        return true;
    }

    public boolean[] getMoves() {
        System.out.println("Degrees of Freedom: " + degreesOfFreedom);
        if (invertable) {
            return getMovesSimple();
        }
        return getMovesSimple();
    }

    private boolean[] getMovesSimple() {
        for (int i = 0; i < matrix.length; i++) {
            boolean on = matrix[i][matrix[0].length - 1];
            moves[i] = on;
        }
        return moves;
    }

    public void display() {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                if (matrix[i][j]) {
                    System.out.print("1");
                } else {
                    System.out.print("0");
                }
            }
            System.out.println();
        }

    }

}
