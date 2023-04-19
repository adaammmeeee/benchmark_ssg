import os

path = "./prism-games/prism/bin/prism "


#Models
models=dict()

models["cdmsn"]="./case-studies/cdmsn.prism ./case-studies/cdmsn.props"
models["cloud5"]="./case-studies/cloud_5.prism ./case-studies/cloud.props"
models["cloud6"]="./case-studies/cloud_6.prism ./case-studies/cloud.props"
models["mdsm1"]="./case-studies/mdsm.prism ./case-studies/mdsm.props -prop 1"
models["mdsm2"]="./case-studies/mdsm.prism ./case-studies/mdsm.props -prop 2"
#models["teamform3"]="./case-studies/team-form-3.prism ./case-studies/team-form.props"
#models["teamform4"]="./case-studies/team-form-4.prism ./case-studies/team-form.props"
models["AV10_10_1"]="./case-studies/AV10_10.prism ./case-studies/AV.props -prop 1"
models["AV10_10_2"]="./case-studies/AV10_10.prism ./case-studies/AV.props -prop 2"
models["AV10_10_3"]="./case-studies/AV10_10.prism ./case-studies/AV.props -prop 3"
models["AV15_15_1"]="./case-studies/AV15_15.prism ./case-studies/AV.props -prop 1"
models["AV15_15_2"]="./case-studies/AV15_15.prism ./case-studies/AV.props -prop 2"
models["AV15_15_3"]="./case-studies/AV15_15.prism ./case-studies/AV.props -prop 3"
models["charlton1"]="./case-studies/charlton.prism ./case-studies/charlton.props -prop 1"
models["charlton2"]="./case-studies/charlton.prism ./case-studies/charlton.props -prop 2"
models["dice10"]="./case-studies/dice10.prism ./case-studies/dice.props -prop 1"
models["dice20"]="./case-studies/dice20.prism ./case-studies/dice.props -prop 1"
models["dice50"]="./case-studies/dice50.prism ./case-studies/dice.props -prop 1"
#models["dice100"]="./case-studies/dice100.prism ./case-studies/dice.props -prop 1"
models["dice50MEC"]="./case-studies/dice50MEC.prism ./case-studies/dice.props -prop 1"
#models["dice100MEC"]="./case-studies/dice100MEC.prism ./case-studies/dice.props -prop 1"
models["hallway5_5_1"]="./case-studies/hallway5_5.prism ./case-studies/hallway.props -prop 1"
models["hallway5_5_2"]="./case-studies/hallway5_5.prism ./case-studies/hallway.props -prop 2"
models["hallway8_8_1"]="./case-studies/hallway8_8.prism ./case-studies/hallway.props -prop 1"
models["hallway8_8_2"]="./case-studies/hallway8_8.prism ./case-studies/hallway.props -prop 2"
models["hallway10_10_1"]="./case-studies/hallway10_10.prism ./case-studies/hallway.props -prop 1"
models["hallway10_10_2"]="./case-studies/hallway10_10.prism ./case-studies/hallway.props -prop 2"
models["cdmsnMEC"]="./case-studies/cdmsnMEC.prism ./case-studies/cdmsn.props"
#models["ManyMECs_1e1"] = "./case-studies/ManyMecs.prism ./case-studies/ManyMecs.props -const N=10"
models["ManyMECs_1e2"]="./case-studies/ManyMecs.prism ./case-studies/ManyMecs.props -const N=100"
models["ManyMECs_1e3"]="./case-studies/ManyMecs.prism ./case-studies/ManyMecs.props -const N=1000"
models["ManyMECs_1e4"]="./case-studies/ManyMecs.prism ./case-studies/ManyMecs.props -const N=10000"
#models["BigMec_1e1"] = "./case-studies/BigMec.prism ./case-studies/BigMec.props -const N=10"
models["BigMec_1e2"] = "./case-studies/BigMec.prism ./case-studies/BigMec.props -const N=100"
models["BigMec_1e3"] = "./case-studies/BigMec.prism ./case-studies/BigMec.props -const N=1000"
models["BigMec_1e4"] = "./case-studies/BigMec.prism ./case-studies/BigMec.props -const N=10000"
#models["hm_10_5"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=10,p=0.5"
#models["hm_10_1"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=10,p=0.1"
#models["hm_10_9"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=10,p=0.9"
#models["hm_20_5"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=20,p=0.5"
models["hm_30_5"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=30,p=0.5"
#models["hm_20_1"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=20,p=0.1"
#models["hm_20_9"]="./case-studies/haddad-monmege-SG.pm ./case-studies/haddad-monmege.prctl -const N=20,p=0.9"
models["adt"]="./case-studies/adt-infect.prism ./case-studies/adt-infect.props -prop 2"
models["two_investors"]="./case-studies/two_investors.prism ./case-studies/two_investors.props -prop 4"
models["coins"]="./case-studies/coins.prism ./case-studies/coins.props -prop 1"
models["prison_dil"]="./case-studies/prisoners_dilemma.prism ./case-studies/prisoners_dilemma.props -prop 9"

#models["ManyAct7"]="./case-studies/randomModels/maxi-requested/RANDOM_SIZE_20000_MODEL_02_ACTIONS_7.prism ./random-generated-models/generatedModels/models.props"
#models["ManyAct4"]="./case-studies/randomModels/maxi-requested/RANDOM_SIZE_20000_MODEL_03_ACTIONS_4.prism ./random-generated-models/generatedModels/models.props"
#models["ManyAct10"]="./case-studies/randomModels/maxi-requested/RANDOM_SIZE_40000_MODEL_10_ACTIONS_10.prism ./random-generated-models/generatedModels/models.props"

for e in models:
    cmd = path + " " + models[e]
    os.system(cmd)

#cmd = path + " " + models["adt"]
#os.system(cmd)

