import os
import requests
from bs4 import BeautifulSoup
import sys

def get_html(url):
    return requests.get(url).content


base_url = "http://codeforces.com/"

class Problem:

    link = None
    name = None
    inputs = None
    outputs = None
    soup = None

    def __init__(self, name, link):
        self.link = link
        self.name = name
        self.inputs = []
        self.outputs = []
        self.soup = BeautifulSoup(get_html(link), "html.parser")

    def find_inputs(self):
        samples = self.soup.select("div.sample-test")[0]
        inputs = samples.select("div.input")
        for inp in inputs:
            pre = inp.find("pre")
            self.inputs.append(pre.text)

    def find_outputs(self):
        samples = self.soup.select("div.sample-test")[0]
        outputs = samples.select("div.output")
        for out in outputs:
            pre = out.find("pre")
            self.outputs.append(pre.text)

class Contest:

    id = None
    link = None
    problems = []

    def __init__(self, id):
        self.id = id
        self.link = base_url + "/contest/" + id

    def find_problems(self):
        soup = BeautifulSoup(get_html(self.link), "html.parser")
        table = soup.select(".problems")[0]
        trs = table.select("tr")[1:]
        for tr in trs:
            td = tr.find("td")
            a = td.find("a")
            self.problems.append(Problem(a.text.strip().lower(), base_url[:-1] + a.attrs.get("href")))


    def make_folders(self):
        os.system("rm -rf " + self.id)
        for problem in self.problems:
            os.system("mkdir -p {}/{}".format(self.id, problem.name))
    
    def make_templates(self):
        from os.path import expanduser
        home = expanduser("~")
        with open(home + "/contests/codes/main.cpp", "r") as tpl_file:
            for problem in self.problems:
                with open("{}/{}/{}.cpp".format(self.id, problem.name, problem.name), "w") as new_file:
                    new_file.write(tpl_file.read())

    def make_inputs(self):
        for problem in self.problems:
            problem.find_inputs()
        for problem in self.problems:
            sample_id = 0
            for inp in problem.inputs:
                with open("{}/{}/in{}".format(self.id, problem.name, str(sample_id)), "w") as new_inp:
                    new_inp.write(inp)
                sample_id += 1

    def make_outputs(self):
        for problem in self.problems:
            problem.find_outputs()
        for problem in self.problems:
            sample_id = 0
            for out in problem.outputs:
                with open("{}/{}/out{}".format(self.id, problem.name, str(sample_id)), "w") as new_out:
                    new_out.write(out)
                sample_id += 1

def main():
    contest_id = sys.argv[1]
    con = Contest(contest_id)
    con.find_problems()
    con.make_folders()
    con.make_templates()
    con.make_inputs()
    con.make_outputs()

if __name__ == '__main__':
    main()
