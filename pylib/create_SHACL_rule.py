def generate_shacl(in_row, out_row, ns, classes, relations):
    prefix_declarations_shacl = "\n".join([f"@prefix {prefix}: <{uri}> ." for prefix, uri in ns.items()])
    prefix_declarations_sparql = "\n".join([f"PREFIX {prefix}: <{uri}>" for prefix, uri in ns.items()])

    shacl_pattern = f"""dmn:prepare_inspections
    a sh:NodeShape ; 
    sh:target [
        a sh:SPARQLTarget ;
        sh:comment "Select all of eligible objects";
        sh:select \"""
            """

    pattern = f"""
    {prefix_declarations_shacl}
    {shacl_pattern}
    {prefix_declarations_sparql}
    SELECT ?this WHERE {{
    ?this a <{classes[in_row.iloc[0]]}> ."""

    # The types of the other elements
    for i in range(2, len(in_row), 2):
        pattern += f"\n?{in_row.iloc[i]} a <{classes[in_row.iloc[i]]}> ."

    # The relationships of ?this with the other elements
    for i in range(1, len(in_row), 2):
        pattern += f"\n?this <{classes[in_row.iloc[i]]}> ?{in_row.iloc[i+1]} ."

    pattern += '\n} \"""; \n];'

    query = f"""
    sh:comment "Create new Inspections to the target objects";
    sh:rule [
        a sh:SPARQLRule;
        sh:construct \""" 
        \n {prefix_declarations_sparql}
        CONSTRUCT {{\n"""
                
    # a-relationships
    for value in out_row:
        query += f"?{value} a <{classes[value]}>.\n"

    # Other relationships
    for relation, source, target in relations:
        if source not in out_row.values or target not in out_row.values:
            continue
        query += f"?{source} <{relation}> ?{target}.\n"

    query += f"?this ocqa:hasInspection ?{out_row.iloc[0]}.\n}}\n"

    query += f"""
    WHERE{{
        SELECT ?this"""

    # Select part of the query
    for value in out_row:
        query += f" ?{value}"
    
    query += "\n WHERE {\n"

    # Construct new URIs
    for value in out_row:
        query += f'BIND(IRI(CONCAT(STR(inst:), "{value}_", STR(CEIL((RAND() * 30000))))) as ?{value})\n'
    
    query+= f"?this a <{classes[in_row.iloc[0]]}> ."

    # The types of the other elements
    for i in range(2, len(in_row), 2):
        query+= f"\n?{in_row.iloc[i]} a <{classes[in_row.iloc[i]]}> ."

    # The relationships of ?this with the other elements
    for i in range(1, len(in_row), 2):
        query+= f"\n?this <{classes[in_row.iloc[i]]}> ?{in_row.iloc[i+1]} ."
    
    query += '\n}\n}\""" ; \n] ; \n .'

    whole_query = pattern +"\n" + query
    return whole_query
