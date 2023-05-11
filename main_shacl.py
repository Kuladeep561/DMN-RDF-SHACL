#%%
from pyshacl import validate
from pylib.DMNParser import *
from pylib.classes_relations import *
from pylib.create_SHACL_rule import *


### **parse DMN table as xml and create DataFrame**###

dmn_filepath = r"C:\Users\kuk\Downloads\geometric-inspections.dmn"


parser = DMNParser(dmn_filepath)
hit_policy = parser.extract_hit_policy()  # get DMN hit policy
inputs, outputs = parser.extract_inputs_outputs()
inputs, outputs = parser.FEEL_converter(inputs, outputs)  # Final inputs and Outputs
df_inputs, df_outputs = parser.dmn_as_dataframe(inputs, outputs)  # Convert into dataframes


###!SHACL validation and SPARQL construct based on hit polocy**###

if (hit_policy.lower() == "collect"):

    ontology = Graph().parse("./graphs/DMN-RDF-Dicon-OCQA-Tbox.ttl",
                             format="ttl")
    example_building = Graph().parse("./graphs/Duplex_A_20110505_LBD.ttl",
                                     format="ttl")
    
    _combined = ontology + example_building
    namespace = dict(_combined.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()}
    classes,objectProperties,annotationProperties,relationships,literals = classes_relations(ns)
    
    inferred_graph = Graph()
    for index, in_row in df_inputs.iterrows():
        output_row = df_outputs.iloc[index]
        
        shacl_rule = generate_shacl(in_row, output_row, ns, classes, relationships)
        with open(f'shacl_rule_{index}.ttl', 'w') as f:
            f.write(shacl_rule)
        
        rules_graph = Graph().parse(f"shacl_rule_{index}.ttl",
                                format="ttl")  # Load the SHACL rules graph

        # Validate the combined graph and apply the rules
        conforms, _inferred_graph, string = validate(_combined, shacl_graph=rules_graph,
                                            data_graph_format='turtle', shacl_graph_format='turtle',
                                            debug=True, advanced=True, inplace=True)
        inferred_graph += _inferred_graph

    new_graph = _combined + inferred_graph
    new_graph.serialize(
        destination="Inferred_geometry_inspections.ttl", format="ttl")

else:
    raise ValueError(f"The hit policy is: {hit_policy}, it is unsupported. The script supports only 'COLLECT'")

