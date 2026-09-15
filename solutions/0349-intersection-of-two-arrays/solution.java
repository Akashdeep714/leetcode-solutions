class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set=new HashSet<>();
        for(int num:nums1){
            set.add(num);
        }
        int k=0;
        for(int num:nums2){
            if(set.remove(num)){
                nums1[k++]=num;
            }
        }
        return Arrays.copyOf(nums1,k);
    }
}