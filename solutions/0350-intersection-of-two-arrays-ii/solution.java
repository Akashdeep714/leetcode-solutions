class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        Arrays.sort(nums1);
        Arrays.sort(nums2);
        
        int[] res=new int[nums1.length];
        int k=0;
        int i=0;
        int j=0;
        while(i<nums1.length && j<nums2.length){
            if(nums1[i]==nums2[j]){
                res[k]=nums1[i];
                k=k+1;
                i=i+1;
                j=j+1;
            }else if(nums1[i]>nums2[j]){
                j=j+1;
            }else{
                i=i+1;
            }
        }
        return Arrays.copyOfRange(res,0,k);
    }
}