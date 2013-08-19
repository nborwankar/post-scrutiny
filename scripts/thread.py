import mailbox
import re

PATH = "../mozilla.governance"
brackets = re.compile(r"<([^<>]+)>")

mb = mailbox.mbox(PATH)

print(mb.values()[1].as_string())

# An implementation of JMZ's email threading algorithm


def thread(mb):
    '''
    Threads a mailbox.
    '''
    id_table = {}

    for mb_message in mb.values():
        message = JMZMessage(mb_message)
        buildContainer(message, id_table)

    # Find the root set -- walk over elementsof id_table,
    # return those with no parents
    root_set = find_root_set(id_table)

    # Prune empty containers
    prune_empty_containers(root_set)

    #discard id_table -- not needed any more


    # Group root set by subject

    # done threading .. put into a tighter data structure

    # sort the siblings

    print(id_table)



    return id_table



def buildContainer(message,id_table):
        mid = message.message_id
        mcontainer = None

        if id_table.has_key(mid) and id_table.get(mid).is_empty():
            #if there is a container for this ID with no message
            #enter the message
            id_table.get(mid).message = message
        else:
            #If there is no container for this ID, make one
            id_table[mid] = JMZContainer(message)
        #There is a third case here, if there is a container
        #which already contains a message.
        #In the jmz Java code, a duplicate message is made to prevent
        #clobbering.  

        parent = None

        for rid in message.references:
            rcontainer = None
            if id_table.has_key(rid):
                rcontainer = id_table.get(rid)
            else:
                rcontainer = JMZContainer()
                id_table[rid] = rcontainer
        
            # link the reference fields Containers together        
            # but not if it would create a loop
            if (parent is not None and #there is a parent
                rcontainer.parent == None and # no parent already
                parent is not rcontainer and # not a tight loop
                not parent.find_child(rcontainer)): # not a wide loop
        
                rcontainer.link_to_parent(parent)

            parent = rcontainer

        # We mill make the last reference the parent of this container,
        # unless one of several conditions holds.
        mcontainer = id_table.get(mid)

        # unless that would introduce a circularity
        # then there is not parent
        if (parent is not None and
            (parent is not mcontainer or
            mcontainer.find_child(parent))):
            
            parent = None
            
        # if this has a parent already, then is has appeared
        # in another message's reference field.
        # This new information takes precedence.
        # We now need to correct the child-list of the parent.
        if mcontainer.parent is not None:
            mcontainer.parent.unlink_child(mcontainer)

        if parent is not None:
            mcontainer.link_to_parent(parent)

class JMZContainer:
    # argument message should be None or JMZMessage
    def __init__(self,message=None):
        self.message = message

    def is_empty(self):
        return self.message == None

    def find_child(self,target):
        if self.child is None:
            return False
        elif self.child == target:
            return True
        else:
            return self.child.find_child(target)

    def link_to_parent(self,parent):
        self.parent = parent
        self.next = parent.child
        parent.child = self

    def unlink_child(self,target):
        prev = None
        rest = self.child

        while(rest is not target and rest is not None):
            prev = rest
            rest = rest.next

        if rest is None:
            print "We got problems"

        if prev is None:
            self.child = target.next;
        else:
            prev.next = target.next;

        target.next = None;
        target.parent = None;

    #JMZMessage message
    message = None
    #JMZContainer parent
    parent = None
    #JMZContainer child
    child = None
    #JMZContainer nextm (next is a Python keyword)
    nextm = None


class JMZMessage:
    def __init__(self,message):
        self.subject = message.get('Subject')
        self.message_id = brackets.match(message.get('Message-ID')).group(1)
        if message.has_key('References'):
            for mid in brackets.match(message.get('References')).groups():
                self.references.append(mid)
        if message.has_key('In-Reply-To'):
            # Use only the first item in In-Reply-To 
            # as the rest are probably email addresses
            try:
                self.references.append(brackets.match(message.get('In-Reply-To')).group(1))
            except:
                print("Error parsing 'In-Reply-To': " + message.get('In-Reply-To'))
        self.data = message

    #String subject
    subject = None
    # ID message_id
    message_id = None
    # ID *references
    references = []
    #extra data
    data = None

