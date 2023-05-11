from rdflib import RDFS, XSD

def classes_relations(ns):
    classes_props  = {
        'Stair':ns['beo'].Stair
        ,'Property':ns['opm'].Property
        ,'Inspection': ns['ocqa'].Inspection
        ,'InspectionEquipment': ns['ocqa'].InspectionEquipment
        ,'InspectionProcedure': ns['ocqa'].InspectionProcedure
        ,'ISCode': ns['dmn'].ISCode
        ,'Agent': ns['dica'].Agent
        ,'Location': ns['dice'].Location
        ,'actualNumberOfRisers': ns['props'].actualNumberOfRisers
        ,'maximumRiserHeight':ns['props'].maximumRiserHeight
        ,'Inspection_Number_Of_Risers':ns['dmn'].Inspection_Number_Of_Risers
        ,'Inspection_Dimension_of_the_Riser':ns['dmn'].Inspection_Dimension_of_the_Riser
        ,'one_time':ns['dmn'].one_time
    }
    annotationProperties={
        'actualNumberOfRisers': ns['props'].actualNumberOfRisers
        ,'maximumRiserHeight':ns['props'].maximumRiserHeight
    }
    objectProperties={

    }
    literals = {
        'Comment': XSD.string
        ,'hasStartDate':XSD.dateTime
        ,'hasEndDate':XSD.dateTime
        ,'hasActivityStartDate':XSD.dateTime
}

    relations = [
    (ns['dice'].isPartOf, 'Inspection_Number_Of_Risers', 'ISCode'),
    (ns['dica'].hasAgent, 'Inspection_Number_Of_Risers', 'Agent'),
    (ns['ocqa'].hasInspectionEquipment, 'Inspection_Number_Of_Risers', 'InspectionEquipment'),
    (ns['dicp'].hasLocation, 'Inspection_Number_Of_Risers', 'Location'),
    (ns['ocqa'].hasInspectionProcedure, 'Inspection_Number_Of_Risers', 'InspectionProcedure'),
    (ns['dmn'].hasFrequency, 'Inspection_Number_Of_Risers', 'One_time'),
    (RDFS.comment, 'Inspection_Number_Of_Risers', 'Comment'),
    
    (ns['dice'].isPartOf, 'Inspection_Dimension_of_the_Riser', 'ISCode'),
    (ns['dica'].hasAgent, 'Inspection_Dimension_of_the_Riser', 'Agent'),
    (ns['ocqa'].hasInspectionEquipment, 'Inspection_Dimension_of_the_Riser', 'InspectionEquipment'),
    (ns['dicp'].hasLocation, 'Inspection_Dimension_of_the_Riser', 'Location'),
    (ns['ocqa'].hasInspectionProcedure, 'Inspection_Dimension_of_the_Riser', 'InspectionProcedure'),
    (ns['dmn'].hasFrequency, 'Inspection_Dimension_of_the_Riser', 'One_time'),
    (RDFS.comment, 'Inspection_Dimension_of_the_Riser', 'Comment')
]

    return classes_props,objectProperties,annotationProperties,relations,literals
