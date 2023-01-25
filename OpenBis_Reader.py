from pybis import Openbis
import json
import base64
from pandas import DataFrame

class OpenBis_Viewer_Helper:

    def __init__(self, url):
        self.o = Openbis(url)  # https:// is assumed

    def connect(self, username, password):
        self.o.login(username, password, save_token=True)  # save the session token in ~/.pybis/example.com.token

    def logout(self):
        self.o.logout()

    def getToken(self):
        token = self.o.token()

    def connectUsingPersonalAccessToken(self):
        self.pat = self.o.get_or_create_personal_access_token(sessionName="PETabViaAPI")
        self.o.set_token(self.pat, save_token=True)

    def getPETABsExperiment(self, name):
        exp = self.o.get_experiment("/OPENBISAPIUSER/PE_TABS/"+name)

        return exp

    def getTestExperiments(self):
        # /OPENBISAPIUSER/TESTCONTENT/TESTCONTENT_EXP_1
        experiments = self.o.get_experiments(
            project='TESTCONTENT',
            space='OPENBISAPIUSER'
        )

        #print("Found "+experiments.count.str()+" experiments")

        for experiment in experiments:  # iterate over search results
            print(experiment.props.all())

        return experiments

    def getPETaBsExperiments(self):
        experiments = self.o.get_experiments(
            project='PE_TABS',
            space='OPENBISAPIUSER',
            type='PE_Tab_Test_Type',
            tags='*',
            finished_flag=False,
            props=['name', 'finished_flag']
        )

        #print("Found "+experiments.count.str()+" experiments")

        for experiment in experiments:  # iterate over search results
            print(experiment.props.all())

        return experiments

    def getExperiments(self, for_project):
        # /OPENBISAPIUSER/TESTCONTENT/TESTCONTENT_EXP_1
        experiments = for_project.get_experiments()

        #print("Found "+experiments.count.str()+" experiments")

        for experiment in experiments:  # iterate over search results
            print(experiment.props.all())

        return experiments

    def getProject(self, name):
        pro = self.o.get_project("/OPENBISAPIUSER/"+name)

        return pro

    def getSamples(self, for_experiment):
        samples = for_experiment.get_samples()

        return samples

    def getSample(self, name, for_experiment):
        sample = for_experiment.get_sample(name)

        return sample

    def getSampleById(self, id):
        sample = self.o.get_sample(id)

        return sample

    def getExperiment(self, name, for_project):
        exp = for_project.get_experiment(code=name)

        return exp

    def getExperimentByFullPath(self, path):
        exp = self.o.get_experiment(path)

        return exp

    def getDataset(self, id):
        dataset = self.o.get_dataset(id)

        return dataset

    def getAllDatasetInCollection(self, forCollection):
        datasets = forCollection.get_datasets()

        return datasets

    def getSpreadsheet(self, for_content):
        spreadsheet = json.loads(base64.b64decode(for_content[6:-7]))
        df = DataFrame(spreadsheet["data"], columns=spreadsheet["headers"])

        print("Original spreadsheet\n")
        print(spreadsheet)

        spreadsheet["data"] = df.to_numpy().tolist()
        print("The list\n")
        print(df.to_numpy().tolist())
        print("The resulting spreadsheet\n")
        print(spreadsheet)
        print("End\n")
        return df