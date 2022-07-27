


page_new = 100


def get_page(page_new):
    '''

    获取当前共有多少页，减去上一次获取的页数，得到新增页数
    '''
    try:
        with open('page_ccgp.txt', 'r') as r:
            page_old = r.readlines()
        # print(page_old)
        with open('page_ccgp.txt', 'w') as w:
            w.writelines([str(page_new)])
        if page_old == []:
            return page_new
        page_old = int(page_old[0])
        if page_old > page_new:
            return page_new
        elif page_old < page_new:
            return page_new - page_old

        return page_new
    except:
        with open('page_ccgp.txt', 'w') as w:
            w.writelines([str(page_new)])

        return page_new


print(get_page(page_new))



