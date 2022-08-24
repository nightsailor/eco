classId = 1

classesFile = "mscoco_labels.names";
classes = None
with open(classesFile, 'rt') as f:
   classes = f.read().rstrip('\n').split('\n')

print(classes[classId])

ex_classesFile = "explanation.txt";
ex_classes = None
with open(ex_classesFile, 'rt') as f:
   ex_classes = f.read().rstrip('\n').split('\n')

print(ex_classes[classId])

# exec(open('test1.py').read())

img_dir = '/Users/shotomorisaki/Programming/eco/static/images/item3.jpg'
exec(open('img_classif.py ' + '--image=' + img_dir).read())
