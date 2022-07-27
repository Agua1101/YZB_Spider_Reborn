import re



a = '''.zhengzhou{background:url(../images/zhengzhou/LogoBg.jpg) no-repeat top center;}/**郑州市政府**/
.jinshui{background:url(../images/jinshui/LogoBg.jpg) no-repeat top center;}/**郑州金水区政府**/
.zhongmou{background:url(../images/zhongmou/LogoBg.jpg) no-repeat top center;}/**中牟县政府**/
.xingyang{background:url(../images/xingyang/LogoBg.jpg) no-repeat top center;}/**荥阳市政府**/
.dengfeng{background:url(../images/dengfeng/LogoBg.jpg) no-repeat top center;}/**登封市政府**/
.zhongyuan{background:url(../images/zhongyuan/LogoBg.jpg) no-repeat top center;}/**中原区政府**/
.shangjie{background:url(../images/shangjie/LogoBg.jpg) no-repeat top center;}/**上街区政府**/
.huiji{background:url(../images/huiji/LogoBg.jpg) no-repeat top center;}/**惠济区政府**/
.gongyi{background:url(../images/gongyi/LogoBg.jpg) no-repeat top center;}/**巩义市政府**/
.gaoxin{background:url(../images/gaoxin/LogoBg.jpg) no-repeat top center;}/**高新区政府**/
.xinmi{background:url(../images/xinmi/LogoBg.jpg) no-repeat top center;}/**新密市政府**/
.xinzheng{background:url(../images/xinzheng/LogoBg.jpg) no-repeat top center;}/**新郑市政府**/
.erqi{background:url(../images/erqi/LogoBg.jpg) no-repeat top center;}/**二七区政府**/
.guancheng{background:url(../images/guancheng/LogoBg.jpg) no-repeat top center;}/**管城区政府**/
.zhengdong{background:url(../images/zhengdong/LogoBg.jpg) no-repeat top center;}/**郑东新区管委会**/
.hkgq{background:url(../images/hkgq/LogoBg.jpg) no-repeat top center;}/**综保区（港区）政府采购网**/
.jingji{background:url(../images/jingji/LogoBg.jpg) no-repeat top center;}/**郑州经济技术开发区**/
.kaifeng{background:url(../images/kaifeng/LogoBg.jpg) no-repeat top center;}/**开封市政府**/
.luoyang{background:url(../images/luoyang/LogoBg.jpg) no-repeat top center;}/**洛阳市政府**/
.yichuan{background:url(../images/yichuan/LogoBg.jpg) no-repeat top center;}/**洛阳市伊川县政府**/
.ruyang{background:url(../images/ruyang/LogoBg.jpg) no-repeat top center;}/**洛阳市汝阳县政府**/
.pingdingshan{background:url(../images/pingdingshan/LogoBg.jpg) no-repeat top center;}/**平顶山政府**/
.pdsslq{background:url(../images/pdsslq/LogoBg.jpg) no-repeat top center;}/**平顶山市石龙区政府**/
.pdszhq{background:url(../images/pdszhq/LogoBg.jpg) no-repeat top center;}/**平顶山市湛河区政府**/
.pdsxcq{background:url(../images/pdsxcq/LogoBg.jpg) no-repeat top center;}/**平顶山市新城区政府**/
.pdsxhq{background:url(../images/pdsxhq/LogoBg.jpg) no-repeat top center;}/**平顶山市新华区政府**/
.pdswdq{background:url(../images/pdswdq/LogoBg.jpg) no-repeat top center;}/**平顶山市卫东区政府**/
.pdsbfx{background:url(../images/pdsbfx/LogoBg.jpg) no-repeat top center;}/**平顶山市宝丰县政府**/
.pdsyx{background:url(../images/pdsyx/LogoBg.jpg) no-repeat top center;}/**平顶山市叶县政府**/
.pdsgxq{background:url(../images/pdsgxq/LogoBg.jpg) no-repeat top center;}/**平顶山市高新区**/
.ruzhou{background:url(../images/ruzhou/LogoBg.jpg) no-repeat top center;}/**平顶山汝州市政府**/
.pdslss{background:url(../images/pdslss/LogoBg.jpg) no-repeat top center;}/**平顶山鲁山市政府**/
.pdsjx{background:url(../images/pdsjx/LogoBg.jpg) no-repeat top center;}/**平顶山郏县政府**/
.pdswgs{background:url(../images/pdswgs/LogoBg.jpg) no-repeat top center;}/**平顶山舞钢市政府**/
.anyang{background:url(../images/anyang/LogoBg.jpg) no-repeat top center;}/**安阳市政府**/
.hebi{background:url(../images/hebi/LogoBg.jpg) no-repeat top center;}/**鹤壁市政府**/
.xinxiang{background:url(../images/xinxiang/LogoBg.jpg) no-repeat top center;}/**新乡市政府**/
.weihui{background:url(../images/weihui/LogoBg.jpg) no-repeat top center;}/**卫辉市政府**/
.jiaozuo{background:url(../images/jiaozuo/LogoBg.jpg) no-repeat top center;}/**焦作市政府**/
.wuzhi{background:url(../images/wuzhi/LogoBg.jpg) no-repeat top center;}/**武陟县政府**/
.puyang{background:url(../images/puyang/LogoBg.jpg) no-repeat top center;}/**濮阳市政府**/
.xuchang{background:url(../images/xuchang/LogoBg.jpg) no-repeat top center;}/**许昌市政府**/
.luohe{background:url(../images/luohe/LogoBg.jpg) no-repeat top center;}/**漯河市政府**/
.sanmenxia{background:url(../images/sanmenxia/LogoBg.jpg) no-repeat top center;}/**三门峡政府**/
.nanyang{background:url(../images/nanyang/LogoBg.jpg) no-repeat top center;}/**南阳市政府**/
.shangqiu{background:url(../images/shangqiu/LogoBg.jpg) no-repeat top center;}/**商丘市政府**/
.sqsxyx{background:url(../images/sqsxyx/LogoBg.jpg) no-repeat top center;}/**商丘市夏邑县政府采购网**/
.sqsmqx{background:url(../images/sqsmqx/LogoBg.jpg) no-repeat top center;}/**商丘市民权县政府采购网**/
.suixian{background:url(../images/suixian/LogoBg.jpg) no-repeat top center;}/**商丘市睢县政府采购网**/
.ningling{background:url(../images/ningling/LogoBg.jpg) no-repeat top center;}/**商丘市宁陵县政府采购网**/
.zhecheng{background:url(../images/zhecheng/LogoBg.jpg) no-repeat top center;}/**商丘市柘城县政府采购网**/
.yucheng{background:url(../images/yucheng/LogoBg.jpg) no-repeat top center;}/**商丘市虞城县政府采购网**/
.liangyuan{background:url(../images/liangyuan/LogoBg.jpg) no-repeat top center;}/**商丘市梁园区政府采购网**/
.suiyang{background:url(../images/suiyang/LogoBg.jpg) no-repeat top center;}/**商丘市睢阳区政府采购网**/
.kaifaqu{background:url(../images/kaifaqu/LogoBg.jpg) no-repeat top center;}/**商丘市开发区政府采购网**/

.xinyang{background:url(../images/xinyang/LogoBg.jpg) no-repeat top center;}/**信阳市政府**/
.huangchuan{background:url(../images/huangchuan/LogoBg.jpg) no-repeat top center;}/**信阳市潢川县政府**/
.zhoukou{background:url(../images/zhoukou/LogoBg.jpg) no-repeat top center;}/**周口市政府**/
.zhumadian{background:url(../images/zhumadian/LogoBg.jpg) no-repeat top center;}/**驻马店市政府**/
.jiyuan{background:url(../images/jiyuan/LogoBg.jpg) no-repeat top center;}/**济源市政府**/'''


# result = re.findall('\.(.*?){',a)
# print(result)

c_name = [[i.replace('政府采购网','').replace('政府','')] for i in ['郑州市政府', '郑州金水区政府', '中牟县政府', '荥阳市政府', '登封市政府', '中原区政府', '上街区政府', '惠济区政府', '巩义市政府', '高新区政府', '新密市政府', '新郑市政府', '二七区政府', '管城区政府', '郑东新区管委会', '综保区（港区）政府采购网', '郑州经济技术开发区', '开封市政府', '洛阳市政府', '洛阳市伊川县政府', '洛阳市汝阳县政府', '平顶山政府', '平顶山市石龙区政府', '平顶山市湛河区政府', '平顶山市新城区政府', '平顶山市新华区政府', '平顶山市卫东区政府', '平顶山市宝丰县政府', '平顶山市叶县政府', '平顶山市高新区', '平顶山汝州市政府', '平顶山鲁山市政府', '平顶山郏县政府', '平顶山舞钢市政府', '安阳市政府', '鹤壁市政府', '新乡市政府', '卫辉市政府', '焦作市政府', '武陟县政府', '濮阳市政府', '许昌市政府', '漯河市政府', '三门峡政府', '南阳市政府', '商丘市政府', '商丘市夏邑县政府采购网', '商丘市民权县政府采购网', '商丘市睢县政府采购网', '商丘市宁陵县政府采购网', '商丘市柘城县政府采购网', '商丘市虞城县政府采购网', '商丘市梁园区政府采购网', '商丘市睢阳区政府采购网', '商丘市开发区政府采购网', '信阳市政府', '信阳市潢川县政府', '周口市政府', '驻马店市政府', '济源市政府']]
e_name = ['zhengzhou', 'jinshui', 'zhongmou', 'xingyang', 'dengfeng', 'zhongyuan', 'shangjie', 'huiji', 'gongyi', 'gaoxin', 'xinmi', 'xinzheng', 'erqi', 'guancheng', 'zhengdong', 'hkgq', 'jingji', 'kaifeng', 'luoyang', 'yichuan', 'ruyang', 'pingdingshan', 'pdsslq', 'pdszhq', 'pdsxcq', 'pdsxhq', 'pdswdq', 'pdsbfx', 'pdsyx', 'pdsgxq', 'ruzhou', 'pdslss', 'pdsjx', 'pdswgs', 'anyang', 'hebi', 'xinxiang', 'weihui', 'jiaozuo', 'wuzhi', 'puyang', 'xuchang', 'luohe', 'sanmenxia', 'nanyang', 'shangqiu', 'sqsxyx', 'sqsmqx', 'suixian', 'ningling', 'zhecheng', 'yucheng', 'liangyuan', 'suiyang', 'kaifaqu', 'xinyang', 'huangchuan', 'zhoukou', 'zhumadian', 'jiyuan']

# print(len(c_name),len(e_name))


d_table = dict(zip(e_name,c_name))
print(d_table)
d_table = {'jinshui': ['金水区'], 'zhongmou': ['中牟县'], 'xingyang': ['荥阳市'], 'dengfeng': ['登封市'], 'zhongyuan': ['中原区'], 'shangjie': ['上街区'], 'huiji': ['惠济区'], 'gongyi': ['巩义市'], 'xinmi': ['新密市'], 'xinzheng': ['新郑市'], 'erqi': ['二七区'], 'guancheng': ['管城区'], 'zhengdong': ['郑东新区'], 'hkgq': ['综保区','港区'], 'jingji': ['郑州经济技术开发区'], 'yichuan': ['伊川县'], 'ruyang': ['汝阳县'], 'pdsslq': ['石龙区'], 'pdszhq': ['湛河区'], 'pdsxcq': ['新城区'], 'pdsxhq': ['新华区'], 'pdswdq': ['卫东区'], 'pdsbfx': ['宝丰县'], 'pdsyx': ['叶县'], 'pdsgxq': ['平顶山高新区','平顶山市高新区'], 'ruzhou': ['汝州市'], 'pdslss': ['鲁山市'], 'pdsjx': ['郏县'], 'pdswgs': ['舞钢市'], 'weihui': ['卫辉市'], 'wuzhi': ['武陟县'], 'sqsxyx': ['夏邑县'], 'sqsmqx': ['民权县'], 'suixian': ['睢县'], 'ningling': ['宁陵县'], 'zhecheng': ['商丘市柘城县'], 'yucheng': ['虞城县'], 'liangyuan': ['梁园区'], 'suiyang': ['睢阳区'], 'kaifaqu': ['商丘市开发区'], 'huangchuan': ['潢川县']}




