import graphviz
from rolestereotype import RoleStereotype as rs
from csv import reader

CONNECTIONS = {
    'calls': lambda a,b : (a,b,{'arrowhead':'vee', 'style':'dashed', 'label':'calls'}),
    'creates': lambda a,b : (a,b,{'dir':"back", 'arrowtail':"diamond", 'label':'creates'}),
    'uses': lambda a,b : (a,b,{'arrowhead':"vee", 'style':"dashed", 'label':'uses'}),
    'has': lambda a,b : (a,b,{'dir':"back", 'arrowtail':"odiamond", 'label':'has'}),
    'references': lambda a,b : (a,b,{'arrowhead':"vee", 'label':'references'}),
    'inherits': lambda a,b : (b,a,{'dir':"back", 'arrowtail':"empty"}),
    'realizes': lambda a,b : (b,a,{'dir':"back", 'style':"dotted", 'arrowtail':"empty"}),
    'aggregates': lambda a,b : (a,b,{'dir':"back", 'arrowtail':"diamond"}),
    'composites': lambda a,b : (a,b,{'dir':"back", 'arrowtail':"odiamond"}),
    'associates': lambda a,b : (a,b,{'arrowhead':"none", 'arrowtail':"none"}),
}

class Connection:
    def __init__(self, name, participants):
        self.name = name
        self.participants = participants
    @property
    def edge(self):
        return CONNECTIONS[self.name](self.participants[0],self.participants[1])
    def __str__(self):
        return f"{_escape(self.participants[0])} {self.name} {_escape(self.participants[1])}"

class Member:
    def __init__(self, name, classname, annot=None, stereotype=None):
        self.name = name
        self.classname = classname
        self.annot = annot
        self.stereotype = stereotype
    @property
    def label(self):
        annot = f"«{self.annot}» " if self.annot else ''
        return f"<{{{annot}{_escape(self.classname)}|}}>"
    @property
    def attrs(self):
        attr = {'shape':'record'}
        if self.stereotype:
            attr['fillcolor']=self.stereotype.bcolor
            attr['color']=self.stereotype.fcolor
            attr['style']='filled'
        return attr
    def __str__(self):
        return ', '.join(str(s) for s in [self.annot, self.classname, self.stereotype] if s)

def graph(name, members, connections):
    dot = graphviz.Digraph(name=name)
    for m in members:
        dot.node(m.name, m.label, _attributes=m.attrs)
    for c in connections:
        a,b,attr = c.edge
        dot.edge(a, b, _attributes=attr)

    return dot

def _cleanup(str):
    return ''.join(c for c in str if c.isalnum())

def _escape(str):
    map = {
        '"': '&quot;',
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    }
    s = str
    for m in map:
        s = s.replace(m, map[m])
    return s

def read_csv(members_csv, connections_csv, csv_has_headers=True, graph_name="Class Diagram"):

    members = []
    conns = []

    with open(members_csv, "r") as csv_file:
        csv_reader = reader(csv_file)
        if csv_has_headers:
            _ = next(csv_reader)

        for row in csv_reader:
            row = [r.strip() for r in row]
            members.append(Member(_cleanup(row[0]), row[0], annot=row[1], stereotype=rs.from_str(row[2])))

    with open(connections_csv, "r") as csv_file:
        csv_reader = reader(csv_file)
        if csv_has_headers:
            _ = next(csv_reader)

        for row in csv_reader:
            row = [r.strip() for r in row]
            conns.append(Connection(row[0], tuple(_cleanup(r) for r in row[1:])))

    return graph(graph_name, members, conns)

if __name__ == "__main__":
    import sys
    if len(sys.argv)<4:
        sys.exit('arguments needed: members CSV, connections CSV, and output filename (png or svg)')
    a = sys.argv[1]
    b = sys.argv[2]
    o = sys.argv[3]
    g = read_csv(a, b)
    g.render(outfile=o)
