import java.util.Collections;
class Solution {
    public int[] findDiagonalOrder(int[][] mat) {
        int m=mat.length;
        int n=mat[0].length;
        int k=0;

        int[] res=new int[m*n];
        for(int i=0;i < m + n -1 ;i++){

            int rowIdx=i<n ? 0 : i-n+1;           
            int colIdx=i<n ? i : n-1;

            if(i%2 == 0){
                List<Integer> temp=new ArrayList<>();
                while(rowIdx < m && colIdx > -1){
                    temp.add(mat[rowIdx][colIdx]);
                    rowIdx += 1;
                    colIdx -= 1;
                }
                Collections.reverse(temp);
                for(int idx=0;idx < temp.size();idx++){
                    res[k]=temp.get(idx);
                    k++;
                }
            }else{
                while(rowIdx < m && colIdx > -1){
                    res[k]=mat[rowIdx][colIdx];
                    rowIdx += 1;
                    colIdx -= 1;
                    k++;
                }
            }
        }
        return res;
    }
}