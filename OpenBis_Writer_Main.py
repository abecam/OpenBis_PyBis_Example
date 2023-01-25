from pybis import Openbis
import pandas as pd
from OpenBis_Reader import OpenBis_Viewer_Helper
import json
import base64
from datetime import datetime
from pandas import DataFrame

class OpenBis_Helper:

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

    def createExperiment(self, name):
        exp = self.o.new_experiment(
            code = name,
            type = 'DEFAULT_EXPERIMENT',
            project = 'PE_TABS'
        )

        exp.save()

        return exp

    def createExperiment(self, name, new_type):
        exp = self.o.new_experiment(
            code = name,
            type = new_type,
            project = 'PE_TABS'
        )
        exp.set_props({'parameter_file': 'parameters_petab.tsv'})
        exp.set_props({'format_version': 1})
        exp.set_props({'condition_files': 'experimentalCondition_petab.tsv'})
        exp.set_props({'measurement_files': 'measurementData_petab.tsv'})
        exp.set_props({'sbml_files': 'model_petab.xml'})
        exp.set_props({'observable_files': 'observables_petab.tsv'})

        exp.save()

        return exp

    def getExperiment(self, name):
        exp = self.o.get_experiment(name)

        return exp

    # Objects are Samples
    def createObject(self, name, new_type, for_experiment):
        obj = self.o.new_object(
            type = new_type,
            code = name,
            space='Openbisapiuser',
            experiment=for_experiment,
            props={"name": name, "description": name + " for PETAB"}
        )
        self.setSpreadSheetFromFile(obj, 'pet_tab_measurementdata')

        obj.save()

        return obj

    def setSpreadSheetFromFile(self, for_object, for_property_type):
        data = pd.read_csv("C:\\path\\a_tsv_file.tsv",sep='\t')

        print(data)

        spreadsheet = {}

        spreadsheet["headers"] = ["A","B","C","D","E","F","G","H","I"]

        print("HEADERS\n")
        print(spreadsheet)
        spreadsheet["data"] = data.iloc[1:].to_numpy().tolist()

        print("WITH DATA\n")
        print(spreadsheet)

        print(json.dumps(spreadsheet))

        for_object.set_props({for_property_type: "<DATA>" + str(
            base64.b64encode(bytes(json.dumps(spreadsheet), encoding='utf-8')), encoding='utf-8') + "</DATA>"})


    def createObjectType(self, name):
        objType = self.o.new_object_type(
            code = name,
            generatedCodePrefix='PETAB',
            validationPlugin=None
        )
        objType.save()

        return objType

    def get_object_type(self, name):
        objType = self.o.get_object_type(name)
        return objType

    def createExperimentType(self, name):
        expType = self.o.new_experiment_type(
            code = name,
            description="PE Tab experiment type",
            validationPlugin=None
        )
        expType.save()

        return expType

    def get_experiment_type(self, name):
        expType = self.o.get_experiment_type(name)
        return expType

    def createSpreadSheet(self, name, new_label, new_description):
        pt_spread = self.o.new_property_type(
            code="PET_TAB_"+name,
            label=new_label,
            description=new_description,
            dataType='XML',
            metaData={'custom_widget': 'Spreadsheet'}
        )
        pt_spread.save()

        return pt_spread

    def assignProperty(self, to_what, property_name_to_assign, is_mandatory=True):
        # Should check that the to_what can be assigned a property
        to_what.assign_property(
            prop="PET_TAB_"+property_name_to_assign,  # mandatory
            section='',
            ordinal=1,
            mandatory=is_mandatory,
            initialValueForExistingEntities='initial value',
            showInEditView = True,
            showRawValueInForms = False
        )

    # Actually not a good idea to do both creation and assignment in the same method->
    # If a creation fails, the property is still there, creating it again will not work.
    def createAndAttachPETabProperties(self, to_what):
        pt_text = self.o.new_property_type(
            code='parameter_file',
            label='parameter_file',
            description='parameter_file',
            dataType='VARCHAR',
        )
        pt_text.save()

        to_what.assign_property(
            prop='parameter_file',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='parameters_petab.tsv',
            showInEditView=True,
            showRawValueInForms=False
        )

        pt_int = self.o.new_property_type(
            code='format_version',
            label='format_version',
            description='format_version',
            dataType='INTEGER',
        )
        pt_int.save()

        to_what.assign_property(
            prop='format_version',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities=1,
            showInEditView=True,
            showRawValueInForms=False
        )

        pt_text = self.o.new_property_type(
            code='condition_files',
            label='condition_files',
            description='condition_files',
            dataType='VARCHAR',
        )
        pt_text.save()

        to_what.assign_property(
            prop='condition_files',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='experimentalCondition_petab.tsv',
            showInEditView=True,
            showRawValueInForms=False
        )

        pt_text = self.o.new_property_type(
            code='measurement_files',
            label='measurement_files',
            description='measurement_files',
            dataType='VARCHAR',
        )
        pt_text.save()

        to_what.assign_property(
            prop='measurement_files',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='measurementData_petab.tsv',
            showInEditView=True,
            showRawValueInForms=False
        )

        pt_text = self.o.new_property_type(
            code='sbml_files',
            label='sbml_files',
            description='sbml_files',
            dataType='VARCHAR',
        )
        pt_text.save()

        to_what.assign_property(
            prop='sbml_files',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='model_petab.xml',
            showInEditView=True,
            showRawValueInForms=False
        )

        pt_text = self.o.new_property_type(
            code='observable_files',
            label='observable_files',
            description='observable_files',
            dataType='VARCHAR',
        )
        pt_text.save()

        to_what.assign_property(
            prop='observable_files',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='observables_petab.tsv',
            showInEditView=True,
            showRawValueInForms=False
        )

    def setDefaultPE_Tab_Values(self, for_experiment):
        for_experiment.set_props({'parameter_file': 'parameters_petab.tsv'})
        for_experiment.set_props({'format_version': 1})
        for_experiment.set_props({'condition_files': 'experimentalCondition_petab.tsv'})
        for_experiment.set_props({'measurement_files': 'measurementData_petab.tsv'})
        for_experiment.set_props({'sbml_files': 'model_petab.xml'})
        for_experiment.set_props({'observable_files': 'observables_petab.tsv'})

        for_experiment.save()

    def createAndAttachNameAndDescProperties(self, to_what):
        #pt_text = self.o.new_property_type(
        #    code='name',
        #    label='name',
        #    description='name',
        #    dataType='VARCHAR',
        #)
        #pt_text.save()

        to_what.assign_property(
            prop='name',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='None',
            showInEditView=True,
            showRawValueInForms=False
        )

        to_what.assign_property(
            prop='description',  # mandatory
            section='',
            ordinal=1,
            mandatory=True,
            initialValueForExistingEntities='None',
            showInEditView=True,
            showRawValueInForms=False
        )

    def createDataSet(self, for_file, for_object, for_exp):
        ds_new = self.o.new_dataset(
            type='ANALYZED_DATA',
            experiment=for_exp,
            sample=for_object,
            files=[for_file]
        )
        ds_new.save()

    def createDataSetFromZip(self, for_file, for_object):
        ds_new = self.o.new_dataset(
            type='ANALYZED_DATA',
            sample=for_object,
            zipfile=for_file
        )
        ds_new.save()

if __name__ == '__main__':
    oBisHelper = OpenBis_Helper('https://some-openbis.org')

    # At minimum with write permission on his own space
    oBisHelper.connect("APIUser", "password")

    # Longer validity:
    # pat = oBisObject.get_or_create_personal_access_token(sessionName="OpenBIS_Api_Work")
    # oBisObject.set_token(pat, save_token=True)

    print(f"Session is active: {oBisHelper.o.is_session_active()} and token is {oBisHelper.o.token}")

    # Only once
    # Need to be instance admin! So might not be practical (or secured) as API call
    #oBisHelper.createSpreadSheet("measurementData", "PETab_MeasurementData", "Data for measurement")

    # Only once! Need to be instance admin! So might not be practical (or secured) as API call
    #petTabExperimentType = oBisHelper.createExperimentType("PE_Tab_Test_Type")
    #petTabExperimentType = oBisHelper.get_experiment_type("PE_Tab_Test_Type")

    #petTabObjectType = oBisHelper.createObjectType("PE_Tab_Object_Test_Type")
    #petTabObjectType = oBisHelper.get_object_type("PE_Tab_Object_Test_Type")

    #oBisHelper.assignProperty(petTabObjectType, "measurementData")

    #oBisHelper.createAndAttachNameAndDescProperties(petTabObjectType)
    # Only once
    #oBisHelper.createAndAttachPETabProperties(petTabExperimentType)

    #onePeTabExperiment = oBisHelper.createExperiment("PE_Tab_Test_5", "PE_Tab_Test_Type")
    onePeTabExperiment = oBisHelper.getExperiment("/OPENBISAPIUSER/PE_TABS/PE_TAB_TEST_3")

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H%M%S")

    onePeTabObject = oBisHelper.createObject("PE_Tab_Test_Object_"+dt_string, "PE_Tab_Object_Test_Type", onePeTabExperiment)
    #oBisHelper.setDefaultPE_Tab_Values(onePeTabExperiment)

    # if not working, OpenBis need to be configured maybe.
    #oBisHelper.createDataSet("C:\\path\\tsv_file.tsv", "/OPENBISAPIUSER/PE_TABS/PE_TAB_TEST_3/PE_Tab_Test_Object_2", "/OPENBISAPIUSER/PE_TABS/PE_TAB_TEST_3")

    # Could encounter the same issue as before
    #oBisHelper.createDataSetFromZip(
    #    "C:\\path\\example_petab.zip",
    #    "/OPENBISAPIUSER/PE_TABS/PE_TAB_TEST_3/PE_Tab_Test_Object_2")


    oBisHelper.logout()

    oBisViewHelper = OpenBis_Viewer_Helper('https://some-openbis.org')

    # At minimum with *read* permission on his own space
    oBisViewHelper.connect("APIUser", "password")

    print(f"Session is active: {oBisViewHelper.o.is_session_active()} and token is {oBisViewHelper.o.token}")

    oBisViewHelper.getTestExperiments()
    oBisViewHelper.getPETaBsExperiments()
    oneExperiment = oBisViewHelper.getPETABsExperiment("PE_TAB_TEST_3")
    print("PE_TAB_TEST_3 Experiment")
    print(oneExperiment.props.all())

    #oneSample = oBisViewHelper.getSample("PE_Tab_Test_Object_3", oneExperiment)
    #print(oneSample.props.all())
    oneSample = oBisViewHelper.getSampleById('20221228164934354-42')
    print(oneSample.props.all())
    result = oBisViewHelper.getSpreadsheet(oneSample.props['pet_tab_measurementdata'])
    print(result)
    #spreadsheet["data"] = df.to_numpy().tolist()

    oneProject = oBisViewHelper.getProject("PE_TABS")
    print("All Experiments in PE_TABS project")
    allPE_TABS_experiments = oBisViewHelper.getExperiments(oneProject)

    for anExperiment in allPE_TABS_experiments:
        print(anExperiment.props.all())
        allSamples = oBisViewHelper.getSamples(anExperiment)

        for aSample in allSamples:  # iterate over search results
            print(aSample.props.all())

    oneProject = oBisViewHelper.getProject("TESTCONTENT")
    print("All Experiments in TESTCONTENT project")
    oBisViewHelper.getExperiments(oneProject)

    print("EXP5 Experiment in TESTCONTENT project")
    anotherExperiment = oBisViewHelper.getExperimentByFullPath("/OPENBISAPIUSER/TESTCONTENT/TESTCONTENT_EXP_1")
    print(anotherExperiment.props.all())

    print("All samples in EXP5 Experiment")
    allSamples = oBisViewHelper.getSamples(anotherExperiment)

    for aSample in allSamples:  # iterate over search results
        print(aSample.props.all())

    print("TESTCOLLECTION1 Experiment in TESTCONTENT project, containing our dataset")
    collExperiment = oBisViewHelper.getExperimentByFullPath("/OPENBISAPIUSER/TESTCONTENT/TESTCOLLECTION1")
    print(collExperiment.props.all())
    allDataSetsInColl = oBisViewHelper.getAllDatasetInCollection(collExperiment)

    print("Datasets in TESTCOLLECTION1 Experiment")
    for aDataset in allDataSetsInColl:  # iterate over search results
        print(aDataset.props())
        print(aDataset.file_list)

    dataset = oBisViewHelper.getDataset("20221227143950020-29")
    print(dataset.props())
    print(dataset.file_list)
    dataset.download()

    oBisViewHelper.logout()