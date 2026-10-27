class Solution {
    public List<List<Integer>> generate(int numRows) {
        int n=numRows;
        List<List<Integer>> list=new ArrayList<>();
        for(int i=0;i<n;i++){
            list.add(helper(i));
        }
        return list;
    }

    public static List<Integer> helper(int n){
        List<Integer> temp=new ArrayList<>();
        int res=1;
        temp.add(res);
        for(int i=1;i<=n;i++){
            res=res*(n-i+1);
            res=res/i;
            temp.add(res);
        }
        return temp;
    }
}