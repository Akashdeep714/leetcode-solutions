class Solution {
    public List<Integer> getRow(int rowIndex) {
        List<Integer> prev=new ArrayList<>();
        prev.add(1);

        for(int idx=1;idx <= rowIndex;idx++){
            List<Integer> curr=new ArrayList<>();
            curr.add(1);

            for(int i=1;i <= idx-1;i++){
                curr.add(prev.get(i)+prev.get(i-1));
            }
            curr.add(1);
            prev=curr;
        }
        return prev;   
    }
}