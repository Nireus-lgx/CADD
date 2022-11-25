# Updated by Zengrui Wu, LMMD, ECUST, 2022-08-01
import zipfile, sys, re

input_file  = zipfile.ZipFile(r'E:\CADD\课题相关\基于网络\DTI_DATABASE\BindingDB_All_2022m10.tsv.zip', 'r')
output_file = open('./BindingDB_2022m10.txt', 'w')
output_list = [set() for i in range(14)]
for line_n, line in enumerate(input_file.open(input_file.namelist()[0], 'r')):
    t = tuple([x.strip() for x in line.decode(encoding = 'utf-8').split('\t')])
    if line_n == 0:
        i_ligand_smiles = t.index('Ligand SMILES')
        i_monomer_id    = t.index('BindingDB MonomerID')
        i_uniprot_ac    = t.index('UniProt (SwissProt) Primary ID of Target Chain')
        i_target_name   = t.index('Target Name Assigned by Curator or DataSource')
        i_organism      = t.index('Target Source Organism According to Curator or DataSource')
        i_chain_n       = t.index('Number of Protein Chains in Target (>1 implies a multichain complex)')
        i_pubmed_id     = t.index('PMID')
        i_activity_list = (
            t.index('Ki (nM)'),
            t.index('IC50 (nM)'),
            t.index('Kd (nM)'),
            t.index('EC50 (nM)'),
            t.index('kon (M-1-s-1)'),
            t.index('koff (s-1)'))
        s_activity_type = tuple([t[i].split(' ')[0].strip()             for i in i_activity_list])
        s_activity_unit = tuple([t[i].split(' ')[1].strip('()').strip() for i in i_activity_list])
        sys.stdout.write('# Activity Type: ' + str(s_activity_type) + '\n')
        sys.stdout.write('# Activity Unit: ' + str(s_activity_unit) + '\n')
        sys.stdout.flush()
    elif len(t[i_ligand_smiles]) > 0 and t[i_chain_n] == '1':
        head = (
            t[i_ligand_smiles],             # 1: Ligand SMILES
            t[i_monomer_id],                # 2: Ligand ID
            t[i_target_name],               # 3: Target Name
            '',                             # 4: Target ID
            t[i_uniprot_ac].split(',')[0],  # 5: Target UniProt AC
            '',                             # 6: Target Type
            t[i_organism],                  # 7: Target Organism
        )
        tail = (
            t[i_pubmed_id],                 # 13: Reference (PubMed ID)
            'BindingDB_2022m6'              # 14: Data Source
        )
        for i_i, i in enumerate(i_activity_list):
            if i < len(t) and len(t[i]) > 0:
                match = re.match('([^0-9.]*)([0-9.]*)', t[i])
                body = head + (
                    s_activity_type[i_i],   # 8: Activity Type
                    match.group(1).strip(), # 9: Activity Relation
                    match.group(2).strip(), # 10: Activity Value
                    s_activity_unit[i_i],   # 11: Activity Unit
                    ''                      # 12: Activity Comment
                ) + tail
                assert len(body) == len(output_list)
                for j, x in enumerate(body):
                    if len(x) > 0:
                        output_list[j].add(x)
                output_file.write('\t'.join(body) + '\n')
output_file.close()
input_file.close()
assert len(output_list[-1]) == 1
assert sorted(output_list[7])  == sorted(set(s_activity_type))
assert sorted(output_list[8])  == sorted(set(['<', '>']))
assert sorted(output_list[10]) == sorted(set(s_activity_unit))
sys.stdout.write('# Output: %s / %u\n' % (str([len(x) for x in output_list]), line_n))
sys.stdout.flush()