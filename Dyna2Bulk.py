#######################
# Dyna2Bulk Conversion
#######################
# Converts LS-Dyna model to Bulk format
# Things converted:-
# *CONSTRAINED_EXTRA_NODES_NODE --> RBE2
# *CONSTRAINED_EXTRA_NODES_SET --> RBE2
# *CONSTRAINED_RIGID_BODIES --> RBE2
# *MAT_RIGID --> RBE2
# *CONSTRAINED_JOINT_SPHERICAL --> CBUSH
# *CONSTRAINED_JOINT_REVOLUTE --> CBUSH
# *CONTACT --> RBE3 or CGAPG
# 
#
import os
import ansa
import time
import datetime
from ansa import base
from ansa import constants
from ansa import connections
from ansa import utils
from ansa import guitk
		
def ConstrainedExtraNodesNode(Include='None',PutInInclude='0'):	
	print("Inlude File Name:%s ,ID:%s" % (Include._name,Include._id))

	dogy = list()
	if(Include == 'None'):
		ExtraNodes = base.CollectEntities(constants.LSDYNA,None, "CONSTRAINED_EXTRA_NODES_NODE" ,  False)
	else:		
		ExtraNodes = base.CollectEntities(constants.LSDYNA, Include , "CONSTRAINED_EXTRA_NODES_NODE" ,  False)
	print ("    Starting ConstrainedExtraNodesNode To RBE2 %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(ExtraNodes)))
	for ExtraNode in ExtraNodes:
		PID = base.GetEntityCardValues(constants.LSDYNA, ExtraNode , ('PID',))['PID']
		NID = base.GetEntityCardValues(constants.LSDYNA, ExtraNode, ('NID',))['NID']
		PartEntity = base.GetEntity(constants.LSDYNA,'__PROPERTIES__',PID)
		PartNodes = base.CollectEntities(constants.LSDYNA,PartEntity,"NODE",recursive=True)
		if(len(PartNodes)==0):
			print("            ***Warning: Part %s has no nodes" % (PartEntity._id))
			continue
		PartNode1 = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=PartNodes[0], fields=('NID',))['NID']
		RBE2 = base.CreateEntity(constants.NASTRAN, "RBE2",{'GN':PartNode1,'GM1':NID,'No.of.Nodes':'2','CM':'123456'})
		dogy .append(RBE2)
	print ("    Finished ConstrainedExtraNodesNode To RBE2 %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)

def ConstrainedExtraNodesSet(Include='None',PutInInclude='0'):
	dogy = list()
	if(Include == 'None'):
		ExtraNodes = base.CollectEntities(constants.LSDYNA,None , "CONSTRAINED_EXTRA_NODES_SET" ,  False)
	else:
		ExtraNodes = base.CollectEntities(constants.LSDYNA,Include , "CONSTRAINED_EXTRA_NODES_SET" ,  False)
	print ("    Starting ConstrainedExtraNodesSet To RBE2 %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(ExtraNodes)))
	for ExtraNode in ExtraNodes:
		PID = base.GetEntityCardValues(constants.LSDYNA, ExtraNode , ('PID',))['PID']
		NSID = base.GetEntityCardValues(constants.LSDYNA, ExtraNode, ('NSID',))['NSID']
		SetEntity = base.GetEntity(constants.LSDYNA,'SET',NSID)
		PartEntity = base.GetEntity(constants.LSDYNA,'__PROPERTIES__',PID)
		PartNodes = base.CollectEntities(constants.LSDYNA,PartEntity,"NODE",recursive=True)
		if(len(PartNodes)==0):
			print("            ***Warning: Part %s has no nodes" % (PartEntity._id))
			continue
		PartNode1 = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=PartNodes[0], fields=('NID',))['NID']
		NodeEntity = base.GetEntity(constants.LSDYNA,'NODE',PartNode1)
		base.AddToSet(SetEntity,NodeEntity)
		RBE2 = base.CreateEntity(constants.NASTRAN, "RBE2",{'GN':PartNode1,'GM NSET':NSID,'CM':'123456'})
		dogy .append(RBE2)
	print ("    Finished ConstrainedExtraNodesSet To RBE2 %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)

def ConstrainedRigidBodies(Include='None',PutInInclude=0):
	dogy = list()
	if(Include == 'None'):
		RigidBodies = base.CollectEntities(constants.LSDYNA,None , "CONSTRAINED_RIGID_BODIES" ,  False)
	else:
		RigidBodies = base.CollectEntities(constants.LSDYNA,Include , "CONSTRAINED_RIGID_BODIES" ,  False)
	print ("    Starting ConstrainedRigidBodies To RBE2 %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(RigidBodies)))
	for RigidBody in RigidBodies:
		PIDM = base.GetEntityCardValues(constants.LSDYNA, RigidBody , ('PIDM',))['PIDM']
		PartEntity = base.GetEntity(constants.LSDYNA,'__PROPERTIES__',PIDM)
		PartNodes = base.CollectEntities(constants.LSDYNA,PartEntity,"NODE",recursive=True)
		if(len(PartNodes)==0):
			print("            ***Warning: Part %s has no nodes" % (PartEntity._id))
			continue
		PartMNode1 = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=PartNodes[0], fields=('NID',))['NID']
		PIDS = base.GetEntityCardValues(constants.LSDYNA, RigidBody , ('PIDS',))['PIDS']
		PartEntity = base.GetEntity(constants.LSDYNA,'__PROPERTIES__',PIDS)
		PartNodes = base.CollectEntities(constants.LSDYNA,PartEntity,"NODE",recursive=True)
		if(len(PartNodes)==0):
			print("            ***Warning: Part %s has no nodes" % (PartEntity._id))
			continue
		PartSNode1 = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=PartNodes[0], fields=('NID',))['NID']
		RBE2 = base.CreateEntity(constants.NASTRAN, "RBE2",{'GN':PartMNode1,'GM1':PartSNode1,'No.of.Nodes':'2','CM':'123456'})
		dogy .append(RBE2)
	print ("    Finished ConstrainedRigidBodies To RBE2 %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)
		
def ConstrainedJointSpherical(Include='None',PutInInclude='0'):
	dogy = list()
	if(Include == 'None'):
		Joints = base.CollectEntities(constants.LSDYNA,None , "CONSTRAINED_JOINT_SPHERICAL" ,  False)
	else:
		Joints = base.CollectEntities(constants.LSDYNA,Include , "CONSTRAINED_JOINT_SPHERICAL" ,  False)
	print ("    Starting ConstrainedJointSpherical To CBUSH %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(Joints)))
	PBUSH = base.CreateEntity(constants.NASTRAN, 'PBUSH',{'K1':'1E6','K2':'1E6','K3':'1E6','K4':'0','K5':'0','K6':'0'})
	
	for Joint in Joints:
		N1 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N1',))['N1']
		N2 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N2',))['N2']
		CBUSH = base.CreateEntity(constants.NASTRAN, 'CBUSH', {'PID':PBUSH._id,'GA':N1,'GB':N2,'Orient':'With Cord','CID':'0'})
		dogy .append(CBUSH)
	print ("    Finished ConstrainedJointSpherical To CBUSH %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)

def ConstrainedJointRevolute(Include='None',PutInInclude='0'):
	dogy = list()
	if(Include == 'None'):
		Joints = base.CollectEntities(constants.LSDYNA,None , "CONSTRAINED_JOINT_REVOLUTE" ,  False)
	else:
		Joints = base.CollectEntities(constants.LSDYNA,Include , "CONSTRAINED_JOINT_REVOLUTE" ,  False)
	
	PBUSH = base.CreateEntity(constants.NASTRAN, 'PBUSH',{'K1':'1E6','K2':'1E6','K3':'1E6','K4':'0','K5':'0','K6':'0'})
	print ("    Starting ConstrainedJointRevolute To CBUSH %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(Joints)))	
	for Joint in Joints:
		N1 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N1',))['N1']
		N2 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N2',))['N2']
		N3 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N3',))['N3']
		N4 = base.GetEntityCardValues(constants.LSDYNA, Joint , ('N4',))['N4']
		CBUSH = base.CreateEntity(constants.NASTRAN, 'CBUSH', {'PID':PBUSH._id,'GA':N1,'GB':N2,'Orient':'With Cord','CID':'0'})
		CBUSH = base.CreateEntity(constants.NASTRAN, 'CBUSH', {'PID':PBUSH._id,'GA':N3,'GB':N4,'Orient':'With Cord','CID':'0'})
		dogy .append(CBUSH)
	print ("    Finished ConstrainedJointSpherical To CBUSH %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)

def MatRigid(Include='None',PutInInclude='0'):
	dogy = list()
	Mat20 =  base.CollectEntities(constants.LSDYNA, None , 'MAT20 MAT_RIGID' , False)
	PartsMat20 = Parts = base.CollectEntities(constants.LSDYNA, Mat20 , '__PROPERTIES__' , prop_from_entities=True)
	if(Include == 'None'):
		PartsInclude = base.CollectEntities(constants.LSDYNA, None , '__PROPERTIES__' , False)
	else:
		PartsInclude = base.CollectEntities(constants.LSDYNA, Include , '__PROPERTIES__' , False)
	Parts =  list(set(PartsMat20) & set(PartsInclude))
	print ("    Starting MatRigid To RBE2 %s" % (datetime.datetime.now()))
	print ("        Proccesing %s entities" % (len(Parts)))	
	for Part in Parts:
		# MatType = base.GetEntityCardValues(constants.LSDYNA,Part,('MID->__type__',)) # See page 27
		PartNodes = base.CollectEntities(constants.LSDYNA,Part,"NODE",recursive=True)
		NodeSet = base.CreateEntity(constants.LSDYNA, "SET", {'OUTPUT TYPE':'SET_NODE'})
		base.AddToSet(NodeSet,PartNodes)
		if(len(PartNodes)==0):
			print("            ***Warning: Part %s has no nodes" % (Part._id))
			continue
		RBE2 = base.CreateEntity(constants.NASTRAN, "RBE2",{'GN':PartNodes[0]._id,'GM NSET':NodeSet._id,'CM':'123456'})
		dogy .append(RBE2)
	print ("    Finished MatRigid To RBE2 %s" % (datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)
		
def TiedContacts(TiedConvertionType='RBE3',Tol=50,FileAppend=0,Include='None',PutInInclude='0',WorkDir="./"):
	dogy = list()
	if(TiedConvertionType=='CGAPG'):
		if(Include == 'None'):
			FileName = 'None'
		else:
			FileName = Include._name
		OutFile = open(WorkDir + FileName + '.CGAPG','w+')

	if(Include == 'None'):
		Contacts = base.CollectEntities(constants.LSDYNA,None , "CONTACT" ,  False)
	else:
		Contacts = base.CollectEntities(constants.LSDYNA,Include , "CONTACT" ,  False)
	print ("    Starting Contact To %s %s" % (TiedConvertionType,datetime.datetime.now()))
	ents = list()
	grid_coords = list()
	new_grids_list= list()
	parts_list = list()
	connections_list = list()
	refgrid_list = list()
	for Contact in Contacts:
		Counter = 0		
		#contact = ansa.base.GetEntity(constants.LSDYNA, "CONTACT", contact_id)
		contact = Contact
		contact_card = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=contact, fields=('SSID', 'MSID','SSTYP','MSTYP'))
		# Master
		if not ('MSTYP' in contact_card and 'SSTYP' in contact_card):
			continue
		if (contact_card['MSTYP'] == '2: Part  set'):
			MasterEntities= ansa.base.GetEntity(constants.LSDYNA, "SET", contact_card['MSID'])
			biw_containers = ansa.base.CollectEntities(constants.NASTRAN, MasterEntities, "__PROPERTIES__", recursive=True)
			elems = ansa.base.CollectEntities(constants.NASTRAN, biw_containers, "__ELEMENTS__", recursive=True)
		if (contact_card['MSTYP'] == '3: Part  id'):
			biw_containers = base.GetEntity(constants.LSDYNA, "__PROPERTIES__", contact_card['MSID'])	
			elems = ansa.base.CollectEntities(constants.NASTRAN, biw_containers, "__ELEMENTS__", recursive=True)
		if (contact_card['SSTYP'] == '2: Part  set') or (contact_card['SSTYP'] == '4: Node  set'):	
			SlaveEntities = ansa.base.GetEntity(constants.LSDYNA, "SET", contact_card['SSID'])
			grids = ansa.base.CollectEntities(constants.NASTRAN, SlaveEntities, "GRID", recursive=True)
		if (contact_card['SSTYP'] == '3: Part  id'):	
			SlaveEntities = ansa.base.GetEntity(constants.LSDYNA, "__PROPERTIES__", contact_card['SSID'])
			grids = ansa.base.CollectEntities(constants.NASTRAN, SlaveEntities, "GRID", recursive=True)
		print ("        Contact ID = %s, Slave nodes = %s, Master elements = %s, Tol = %s" % (contact._id,len(grids),len(elems),Tol))	
		grid_coords_list = list()
		for grid in grids:	
			grid_card = ansa.base.GetEntityCardValues(constants.LSDYNA, entity=grid, fields=('NID','X', 'Y', 'Z'))
			grid_coords = (grid_card['X'], grid_card['Y'], grid_card['Z'])
			grid_coords_list.append(grid_coords)
		NearestElements = ansa.base.NearestShell(search_entities = biw_containers, tolerance = Tol, coordinates = grid_coords_list)
		if (TiedConvertionType == 'CGAPG'):
			val = {'KA':'1E6','KB':'1E6','Kt':'1E6'}
			PGAP = base.CreateEntity(constants.NASTRAN, "PGAP",val)
			CONM1 = base.CreateEntity(constants.NASTRAN, "CONM1", {'GA':grids[0]._id})
			MaxID = CONM1._id
			base.DeleteEntity(CONM1,True)
			i=0
			for i in range(len(NearestElements)):
				if(NearestElements[i]):
					OutFile.write("\nCGAPG,%s,%s,%s,ELEM\n,%s" % (i+MaxID,PGAP._id,grids[i]._id,NearestElements[i]._id))
					Counter=Counter+1

		if (TiedConvertionType == 'RBE3'):
			i=0
			refc = '123456'
			for i in range(len(NearestElements)):
				if(NearestElements[i]):
					elem_type = base.GetEntityCardValues(constants.NASTRAN, entity=NearestElements[i], fields=('EID','type'))
					if "QUAD" in elem_type['type']:
						elem_ret = ansa.base.GetEntityCardValues(constants.NASTRAN, entity=NearestElements[i], fields=('G1','G2','G3','G4'))
						vals = {'REFGRID':grids[i]._id, 'REFC':refc, 'WT1':1.0, 'C1':'123', 'G1':elem_ret['G1'], 'G2':elem_ret['G2'], 'G3':elem_ret['G3'], 'G4':elem_ret['G4'], 'No.of.Nodes':5}
						RBE3 = ansa.base.CreateEntity(constants.NASTRAN, "RBE3", vals)
						dogy .append(RBE3)
					if "TRIA"  in elem_type['type']:
						elem_ret = ansa.base.GetEntityCardValues(constants.NASTRAN, entity=NearestElements[i], fields=('G1','G2','G3'))
						vals = {'REFGRID':grids[i]._id, 'REFC':refc, 'WT1':1.0, 'C1':'123', 'G1':elem_ret['G1'], 'G2':elem_ret['G2'], 'G3':elem_ret['G3'],'No.of.Nodes':4}
						RBE3 = ansa.base.CreateEntity(constants.NASTRAN, "RBE3", vals)
						dogy .append(RBE3)
					Counter=Counter+1
		print("            %s out of %s nodes succesfuly projected" % (Counter,len(grids)))
	print ("    Finished Contact To %s %s" % (TiedConvertionType,datetime.datetime.now()))
	if(PutInInclude == 1 and Include != 'None'):
		base.AddToInclude(Include, dogy)

def Gui():
	w = guitk.BCWindowCreate('Simple BCWindow', guitk.constants.BCOnExitDestroy)
	le1 = guitk.BCLineEditCreate(w, 'RBE3')
	le2 = guitk.BCLineEditCreate(w, '50')
	le3 = guitk.BCLineEditCreate(w, './')
	cb9 = guitk.BCCheckBoxCreate(w, 'Maintain Include File structure')
	cb1 = guitk.BCCheckBoxCreate(w, 'ExtraNodesNode')
	cb2 = guitk.BCCheckBoxCreate(w, 'ExtraNodesSet')
	cb3 = guitk.BCCheckBoxCreate(w, 'RigidBodies')
	cb4 = guitk.BCCheckBoxCreate(w, 'MatRigid')
	cb5 = guitk.BCCheckBoxCreate(w, 'JointSpherical')
	cb6 = guitk.BCCheckBoxCreate(w, 'JointRevolute')
	cb7 = guitk.BCCheckBoxCreate(w, 'Contact')
	cb8 = guitk.BCCheckBoxCreate(w, 'Append File')
	cb10 = guitk.BCCheckBoxCreate(w, 'Add Comments')
	f = guitk.BCFrameCreate(w)
	l = guitk.BCBoxLayoutCreate(f, guitk.constants.BCHorizontal)
	b1 = guitk.BCPushButtonCreate(l, "RUN", doda, [le1,le2,cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8,cb9,cb10,le3])
	guitk.BCShow(w)

def doda(WidgetInfo,listy):
	Type = guitk.BCLineEditGetText(listy[0])
	Tol = guitk.BCLineEditGetText(listy[1])
	WorkDir = guitk.BCLineEditGetText(listy[12])
	Switch_Xnn = guitk.BCCheckBoxIsChecked(listy[2])
	Switch_Xns = guitk.BCCheckBoxIsChecked(listy[3])
	Switch_Rb = guitk.BCCheckBoxIsChecked(listy[4])
	Switch_Mr = guitk.BCCheckBoxIsChecked(listy[5])
	Switch_Js = guitk.BCCheckBoxIsChecked(listy[6])
	Switch_Jr = guitk.BCCheckBoxIsChecked(listy[7])
	Switch_C = guitk.BCCheckBoxIsChecked(listy[8])
	Switch_FileAppend = guitk.BCCheckBoxIsChecked(listy[9])
	switch_Include = guitk.BCCheckBoxIsChecked(listy[10])

	Includes = base.CollectEntities(constants.LSDYNA, None, "INCLUDE", False)
	if(switch_Include == 1 and len(Includes) > 0):
		for Include in Includes:
			if(Switch_Xnn==1):
				ConstrainedExtraNodesNode(Include=Include,PutInInclude=switch_Include)
			if(Switch_Xns==1):
				ConstrainedExtraNodesSet(Include=Include,PutInInclude=switch_Include)
		
			if(Switch_Rb==1):
				ConstrainedRigidBodies(Include=Include,PutInInclude=switch_Include)
			if(Switch_Mr==1):
				MatRigid(Include=Include,PutInInclude=switch_Include)
			if(Switch_Js==1):
				ConstrainedJointSpherical(Include=Include,PutInInclude=switch_Include)
			if(Switch_Jr==1):
				ConstrainedJointRevolute(Include=Include,PutInInclude=switch_Include)
			if(Switch_C==1):
				TiedContacts(TiedConvertionType=Type,Tol=float(Tol),FileAppend=Switch_FileAppend,Include=Include,PutInInclude=switch_Include,WorkDir=WorkDir)
	else:
		Include = 'None'
		if(Switch_Xnn==1):
			ConstrainedExtraNodesNode(Include=Include,PutInInclude=switch_Include)
		if(Switch_Xns==1):
			ConstrainedExtraNodesSet(Include=Include,PutInInclude=switch_Include)
		if(Switch_Rb==1):
			ConstrainedRigidBodies(Include=Include,PutInInclude=switch_Include)
		if(Switch_Mr==1):
			MatRigid(Include=Include,PutInInclude=switch_Include)
		if(Switch_Js==1):
			ConstrainedJointSpherical(Include=Include,PutInInclude=switch_Include)
		if(Switch_Jr==1):
			ConstrainedJointRevolute(Include=Include,PutInInclude=switch_Include)
		if(Switch_C==1):
			TiedContacts(TiedConvertionType=Type,Tol=float(Tol),FileAppend=Switch_FileAppend,Include=Include,PutInInclude=switch_Include,WorkDir=WorkDir)

def debug():
	Type = 'CGAPG'
	Tol = 50
	Switch_Xnn = 0
	Switch_Xns = 0
	Switch_Rb = 0
	Switch_Mr = 0
	Switch_Js = 0
	Switch_Jr = 0
	Switch_C = 1
	Switch_FileAppend = 0
	switch_Include = 1
	Includes = base.CollectEntities(constants.LSDYNA, None, "INCLUDE", False)
	WorkDir = 'C:/skrish/Tempy/'
	if(switch_Include == 1 and len(Includes) > 0):
		for Include in Includes:
			print("Inlude File Name:%s ,ID:%s" % (Include._name,Include._id))
			if(Switch_Xnn==1):
				ConstrainedExtraNodesNode(Include=Include,PutInInclude=switch_Include)
			if(Switch_Xns==1):
				ConstrainedExtraNodesSet(Include=Include,PutInInclude=switch_Include)
		
			if(Switch_Rb==1):
				ConstrainedRigidBodies(Include=Include,PutInInclude=switch_Include)
			if(Switch_Mr==1):
				MatRigid(Include=Include,PutInInclude=switch_Include)
			if(Switch_Js==1):
				ConstrainedJointSpherical(Include=Include,PutInInclude=switch_Include)
			if(Switch_Jr==1):
				ConstrainedJointRevolute(Include=Include,PutInInclude=switch_Include)
			if(Switch_C==1):
				TiedContacts(TiedConvertionType=Type,Tol=float(Tol),FileAppend=Switch_FileAppend,Include=Include,PutInInclude=switch_Include,WorkDir=WorkDir)

	else:
		Include = 'None'
		if(Switch_Xnn==1):
			ConstrainedExtraNodesNode(Include=Include,PutInInclude=switch_Include)
		if(Switch_Xns==1):
			ConstrainedExtraNodesSet(Include=Include,PutInInclude=switch_Include)
		if(Switch_Rb==1):
			ConstrainedRigidBodies(Include=Include,PutInInclude=switch_Include)
		if(Switch_Mr==1):
			MatRigid(Include=Include,PutInInclude=switch_Include)
		if(Switch_Js==1):
			ConstrainedJointSpherical(Include=Include,PutInInclude=switch_Include)
		if(Switch_Jr==1):
			ConstrainedJointRevolute(Include=Include,PutInInclude=switch_Include)
		if(Switch_C==1):
			TiedContacts(TiedConvertionType=Type,Tol=float(Tol),FileAppend=Switch_FileAppend,Include=Include,PutInInclude=switch_Include,WorkDir=WorkDir)

Gui()
#debug()
