public class GridZero {

    private static boolean[][] makeEquations(int[][] a) {
        int size = a.length * a.length;
        boolean[][] matrix = new boolean[size][size + 1];

        for (int row = 0; row < a.length; row++) {
            for (int col = 0; col < a.length; col++) {
                int my_index =  row * a.length + col;
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

    private static double[] flatten(int[][] matrix) {
        double[] retval = new double[matrix.length* matrix.length];
        int index = 0;
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                retval[index++] = matrix[i][j];
            }
        }
        return retval;
    }


    public static int answer(int[][] matrix) {
        boolean[][] myEquations = makeEquations(matrix);
        //double[] answers = flatten(matrix);
        final GaussJordanElimination gaussJordanElimination = new GaussJordanElimination(myEquations);
        gaussJordanElimination.eliminate();

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
                if(matrix[i][j] == 1) {
                    return false;
                }
            }
        }
        return true;
    }

    private static void flip(int[][] matrix, int row, int col) {
        for(int i = 0; i < matrix.length; i++) {
            matrix[row][i] ^= 1;
            matrix[i][col] ^= 1;
        }
        matrix[row][col] ^= 1;
    }
}

class GaussJordanElimination {

    private boolean[][] matrix;
    private boolean[] moves;
    private boolean[] noRank;

    public GaussJordanElimination(final boolean[][] matrix) {
        this.matrix = matrix;
        moves = new boolean[matrix.length];
        noRank = new boolean[matrix.length];
    }

    private boolean setBit(int rowIndex) {
        if(matrix[rowIndex][rowIndex]) {
            return true;
        }
        for (int i = rowIndex + 1; i < matrix.length; i++) {
            if (matrix[i][rowIndex]) {
                xor(rowIndex, i);
                return true;
            }
        }
        return false;
    }

    private void xor(int rowIndex, int i) {
        for(int j = 0; j < matrix[0].length; j++) {
            matrix[rowIndex][j] = matrix[rowIndex][j] ^ matrix[i][j];
        }
    }

    public boolean eliminate(){
        for(int rowIndex = 0; rowIndex < matrix.length; rowIndex++) {
            if (!setBit(rowIndex)) {
                System.out.println("error, no element in " + rowIndex);
                noRank[rowIndex] = true;
                continue;
            }
            for (int j = rowIndex + 1; j < matrix.length; j++) {
                if(matrix[j][rowIndex]) {
                    xor(j, rowIndex);
                }
            }
        }

        // Clear upper now
        for (int rowIndex = 0; rowIndex < matrix.length; rowIndex++) {
            for (int colIndex = rowIndex + 1; colIndex < matrix.length; colIndex++) {
                if(matrix[rowIndex][colIndex]) {
                    xor(rowIndex, colIndex);
                }
            }
        }
        return true;
    }

    public boolean[] getMoves() {
        for(int i = 0; i < matrix.length; i++) {
            if(noRank[i]) {
                continue;
            }
            boolean on = matrix[i][matrix[0].length - 1];
            if (on) {
                for(int j = 0; j < matrix.length; j++) {
                    if(matrix[i][j]) {
                        moves[j] ^= true;
                    }
                }
            }
        }
        return moves;
    }
}
