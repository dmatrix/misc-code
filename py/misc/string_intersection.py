
def intersect(s1, s2):
    res = ''
    if (len(s1) == 0) or (len(s2) == 0):
        return res
    else:
        larger = s1 if len(s1) >= len(s2) else s2
        for i in larger:
            if i in s2 and i not in res:
                    res += i
    return res


import collections

def intersect2(s, t):
    s = s.replace(' ', '')
    t = t.replace(' ', '')
    res = ''

    count = collections.Counter(s)

    for i in t:
        if count[i] != 0:
            res = res + i
            count[i] = count[i] - 1
    return res

if __name__ == '__main__':
    s1 = "Databricks and Apache Spark".replace(" ", "")
    s2 = "Developer Advocates".replace(" ", "")
    print(intersect(s1,s2))
    ss1 = set(s1)
    ss2 = set(s2)
    print(ss1.intersection(ss2))

    ss3 = set("DatrcdApe")
    ss4 = {'D', 'r', 'A', 'e', 't', 'a', 'p', 'c', 'd'}

    print(ss3 == ss4)

    print(intersect2(s1, s2))
    print(intersect2(s2, s1))
    print(intersect2(s1, s1))
