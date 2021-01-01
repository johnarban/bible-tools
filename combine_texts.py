a = text.to_list()
out = re.sub("[^a-zA-Z ]+","",a)
outl = out.lower()
outs = outl.split(' ')