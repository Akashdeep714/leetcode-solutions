/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

class Solution {
    public Node copyRandomList(Node head) {
        // approach 2
        // 1.Stitching
        // 1-1_n-2-2_n-3-3_n
        // 2.Update random pointer of new nodes
        // 3.Untangle old and new list

        if(head == null){
            return null;
        }
        Node curr= head;
        Node newCurr= head;
        //1.Stitching
        //1---1_n--2
        // curr - 1
        // node -1_n
        // currNext - 2
        while(curr != null){
            Node node = new Node(curr.val);
            Node currNext = curr.next;
            node.next = curr.next;
            curr.next = node;
            curr = currNext;
        }

        //2.Update random pointer of new nodes
        curr = head;
        // 1_o-->1_n--->2_o--->2_n
        while(curr != null){
            Node newNode = curr.next;
            newNode.random = curr.random != null ? curr.random.next : null;
            curr = curr.next.next;
        }

        //3.Untangle old and new list
        Node oldHead = head;
        Node newHead = head.next;
        Node resultHead = head.next;
        // 1_o-->1_n--->2_o--->2_n
        // oldHead = 1_o
        // newhead = 1_n
        // head = 1_o -> 2_o
        // resultHead = 1_n -> 2_n
        while(oldHead != null){
            oldHead.next = newHead.next;
            oldHead = newHead.next;
            newHead.next = oldHead != null ? oldHead.next : null;
            newHead = newHead.next;
        }
        return resultHead;
    }
}