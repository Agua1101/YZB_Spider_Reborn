import regex as re

class ProjectIdEx():
    def __init__(self,page_url='',url_tag=None):
        self.page_url = page_url
        self.url_tag = url_tag

    def pj_id_ex(self):
        tag_dict = {
            'ccgp-shandong':self.ccgp_shandong,'ccgp-shanxi':self.ccgp_shanxi,'gdgpo.gov':self.gdgpo_gov,'ccgp-jiangsu':self.ccgp_jiangsu,
            'ccgp-anhui':self.ccgp_anhui,'ccgp-sichuan':self.ccgp_sichuan,'ccgp-guangxi':self.ccgp_guangxi,'ccgp-guizhou':self.ccgp_guizhou,
            'ccgp-shaanxi':self.ccgp_shaanxi,'ccgp-xinjiang':self.ccgp_xinjiang,'ccgp-neimenggu-in':self.ccgp_neimenggu_in
        }
        return tag_dict[self.url_tag]()

    def ccgp_neimenggu_in(self):
        project_id = self.page_url.split('=').pop()
        # print(project_id)
        return project_id

    def ccgp_shandong(self):
        project_id = self.page_url.split('=').pop()
        # print(project_id)
        return project_id

    def ccgp_shanxi(self):
        project_id = self.page_url.split('=').pop()
        # print(project_id)
        return project_id

    def gdgpo_gov(self):
        project_id = self.page_url.split('/id/').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_jiangsu(self):
        project_id = self.page_url.split('/').pop()
        # print(project_id)
        return project_id

    def ccgp_anhui(self):
        project_id = self.page_url.split('newsId=').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_sichuan(self):
        project_id = self.page_url.split('/').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_guangxi(self):
        project_id = self.page_url.split('/').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_guizhou(self):
        project_id = self.page_url.split('/').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_shaanxi(self):
        project_id = self.page_url.split('noticeguid=').pop()[:32]
        # print(project_id)
        return project_id

    def ccgp_xinjiang(self):
        project_id = re.findall('ZcyAnnouncement10016/(.*?)==.html?',self.page_url)
        if project_id:
            return project_id[0]
        # project_id = self.page_url.split('noticeguid=').pop()[:32]
        # print(project_id)
        return project_id