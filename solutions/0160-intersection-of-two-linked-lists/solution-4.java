/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        // approach 4
        ListNode currA = headA;
        ListNode currB = headB;

        int lenA =0;
        int lenB =0;

        while(currA != null){
            lenA++;
            currA = currA.next;
        }

        while(currB != null){
            lenB++;
            currB = currB.next;
        }

        currA = headA;
        currB = headB;
        int diff=Math.abs(lenA - lenB);

        if(lenA > lenB){
            int i =0;
            currA = headA;
            while(i < diff){
                currA = currA.next;
                i++;
            }
        }else{
            int i =0;
            currB = headB;
            while(i < diff){
                currB = currB.next;
                i++;
            }
        }

        while(currA !=null && currB != null && currA != currB){
            currA = currA.next;
            currB = currB.next;
        }

        return currA;
    }
}