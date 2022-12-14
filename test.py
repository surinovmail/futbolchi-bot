
s = input()
sentence = ''.join(s.split())

l = [i for i in sentence if i.isalpha()]
if len(sentence)==len(l):
    print("Barchasi harf")
else :
    print("Ichida harfdan boshqa belgilar ham  bor")