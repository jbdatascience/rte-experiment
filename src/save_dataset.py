# Bismillahi-r-Rahmani-r-Rahim
#
# Entailment dataset saver

from xml.dom.minidom import Document

def save(positive, negative, path):
    pairs = ([x + (True,) for x in positive] +
             [x + (False,) for x in negative])
    save_pairs(pairs, path)

def save_pairs(pairs, path):
    doc = Document()
    corpus = doc.createElement('entailment-corpus')
    doc.appendChild(corpus)
    
    i = 0
    for pair in pairs:
        try:
            text, hypothesis, entailment = pair
        except ValueError:
            print "Too many values: ", pair
            continue
        i += 1
        pair = doc.createElement('pair')
        pair.setAttribute('id', str(i))
        pair.setAttribute('value', str(entailment).upper())
        corpus.appendChild(pair)
        
        t = doc.createElement('t')
        pair.appendChild(t)
        
        t_text = doc.createTextNode(text)
        t.appendChild(t_text)
        
        h = doc.createElement('h')
        pair.appendChild(h)
        
        h_text = doc.createTextNode(hypothesis)
        h.appendChild(h_text)
    f = open(path, 'w')
    doc.writexml(f, addindent=' ', newl='\n')

