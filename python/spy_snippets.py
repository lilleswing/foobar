
def answer(document, searchTerms):
    searchTerms = set(searchTerms)
    wordlist = document.split()
    best_length = 100000
    start = 0
    stop = 0
    for i in xrange(len(wordlist)):
        for j in xrange(i + 1, len(wordlist) + 1):
            snippet = set(wordlist[i:j])
            if snippet >= searchTerms:
                distance = j - i
                if distance < best_length:
                    start = i
                    stop = j
                    best_length = distance
    return " ".join(wordlist[start:stop])


print(answer("many google employees can program", ["google", "can"]))
print(answer("many google employees can program", ["google", "program"]))
