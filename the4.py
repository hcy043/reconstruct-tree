def help_ben_solo(tree,threshold):
    soldiers = {} #Name => force, father, height,index
    def max_depth2(tree):
        """Forked from http://user.ceng.metu.edu.tr/~ceng111/lab/examples/week14/max_depth.py"""
        if len(tree) == 2:
            return 1
        else:
            maximum = -1
            for child in tree[2:]:
                current = 1 + max_depth2(child)
                if current > maximum:
                    maximum = current
            return maximum
    top_height = max_depth2(tree)
    def order(tree=tree,father="God",height=top_height,index=1):
        if len(tree) == 2:
            soldiers[tree[0]] = tree[1],father,height,index
        else:
            soldiers[tree[0]] = tree[1],father,height,index
            inc = 0
            for i in tree[2:]:
                inc += 1
                order(i,tree[0],height-1,index+inc)
    order()
    for i,j in soldiers.iteritems():
	print i,j
    return ""
    def swap_soldiers(sold1,sold2):
        force1,father1,height1,index1 = soldiers[sold1]
        force2,father2,height2,index2 = soldiers[sold2]
        for key, content in sorted(soldiers.items(), key=lambda (k,v): (v[2],k),reverse=True):
            if key != sold1 and key != sold2:
                if content[1] == sold1:
                        soldiers[key] = content[0],sold2,content[2],content[3]
                elif content[1] == sold2:
                    soldiers[key] = content[0],sold1,content[2],content[3]
        if father1 == sold2:
            soldiers[sold1] = force1,father2,height2,index2
            soldiers[sold2] = force2,sold1,height1,index1
        elif father2 == sold1:
            soldiers[sold1] = force1,sold2,height2,index2
            soldiers[sold2] = force2,father1,height1,index1
        else:
            soldiers[sold1] = force1,father2,height2,index2
            soldiers[sold2] = force2,father1,height1,index1 
    #cons 1:
    def cons1():
        for key,soldier1 in sorted(soldiers.items(), key=lambda (k,v): (v[2],k)):# 2 height
            for key2,soldier2 in sorted(soldiers.items(), key=lambda (k,v): (v[2],k)):
                if  soldier1[2] > soldier2[2] and soldier1[0] < soldier2[0]:
                    swap_soldiers(key,key2)
                    return 1
        return False
    a = 1
    while a == 1: #avoid recursion depth limit exceed
        a = cons1()
    #/cons 1
    #cons 2:
    def commander_soldier(cmd,sld):
        checking_father = soldiers[sld][1]
        while True:
            if checking_father == cmd:
                return True
            elif checking_father=="God":
                return False
            else:
                checking_father = soldiers[checking_father][1]
    def c1_check(t1):
        for key,soldier1 in t1.iteritems():
            for key2,soldier2 in t1.iteritems():
                if  soldier1[2] > soldier2[2] and soldier1[0] < soldier2[0]:
                    return False
        return True
    deleted_ones = []
    def c2():
        for move,soldier in sorted(soldiers.items(), key=lambda (k,v): (v[0],k),reverse=True):
            if soldier[2] < threshold:
                flag = False
                for father,soldier2 in soldiers.iteritems():
                    if soldier2[2] <= threshold : continue
                    sum_of_child_force = 0
                    for key,child in soldiers.iteritems():
                        if child[1] == father:
                            sum_of_child_force += child[0]
                    if sum_of_child_force + soldiers[move][0] <= soldier2[0]:
                        if commander_soldier(father,move):
                            tmp_soldiers = soldiers.copy()
                            tmp_soldiers[move] = soldier[0],father,soldiers[father][2]-1,9
                            if c1_check(tmp_soldiers):
                                soldiers[move] = soldier[0],father,soldiers[father][2]-1,9
                                flag = True
                                return True
                if flag == False:
                    deleted_ones.append(move)
                    del soldiers[move]
                    return True
        return "gg"
    do_c2 = True
    while do_c2 == True:
        do_c2 = c2()
    #/cons 2
    #prepare for output
    def childs(father):
        result = []
        for key, value in sorted(soldiers.items(), key=lambda (k,v): (v[3],k)):
            if value[1] == father:
                result.append([key,value[0]])
        return result
    def get_childs(father):
        result = []
        for key, value in sorted(soldiers.items(), key=lambda (k,v): (v[3],k)):
            if value[1] == father:
                if childs(key) == []: 
                    result.append([key,value[0]])
                else:
                    resultx = [key,value[0]]
                    for i in get_childs(key):
                        if childs(i) == []:
                            resultx += [i] 
                        else:
                            resultx += get_childs(i[0])
                    result.append(resultx)
        return result
    return (get_childs("God")[0],deleted_ones[::-1])
