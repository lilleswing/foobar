__author__ = 'leswing'


"""
    /**
     * Solution in java because I didn't want to optimize the python
     */
    public static int answer(int [] L, int k) {
        int[] last = new int[k];
        int[] now = new int[k];
        Arrays.fill(last, 0);
        Arrays.fill(now, 0);

        now[0] = L[0];
        int best = L[0];
        for(int i = 1; i < L.length; i++) {
            // Swap now and last
            int[] temp = now;
            now = last;
            last = temp;
            now[0] = L[i];

            for(int j = 1; j < k; j++) {
                now[j] = last[j-1] + L[i];
                if (now[j] > best) {
                    best = now[j];
                }
            }
        }

        return best;
    }
"""
