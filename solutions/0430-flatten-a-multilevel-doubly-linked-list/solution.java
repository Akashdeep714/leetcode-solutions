/*
// Definition for a Node.
class Node {
    public int val;
    public Node prev;
    public Node next;
    public Node child;
};
*/

class Solution {
    public Node flatten(Node head) {
        if(head == null){
            return null;
        }

        Node pHead = new Node();
        Node prev = pHead;

        Stack<Node> stack = new Stack<>();

        stack.add(head);
        // stack: 1
        // 1 -> 2
        // 3
        // 1 -> 3 -> 2
        // curr = 1
        // prev: 0<->1
        // prev: 1
        // pHead: 0
        while(!stack.isEmpty()){
            Node curr = stack.pop();

            curr.prev = prev;
            prev.next = curr;

            if(curr.next != null){
                stack.add(curr.next);
            }
            if(curr.child != null){
                stack.add(curr.child);
            }

            prev = curr;
            curr.child = null;
        }

        pHead.next.prev = null;
        return pHead.next;
    }
}