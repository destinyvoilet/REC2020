import os
import csv
import hashlib


def get_md5(string):
    """Get md5 according to the string
    """
    byte_string = string.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(byte_string)
    result = md5.hexdigest()
    return result


def build_college(college_prep, college_import):
    """Create an 'college' file in csv format that can be imported into Neo4j.
    format -> college_id:id name fame label
    label->college
    """
    print('Writing to {} file...'.format(executive_import.split('/')[-1]))
    with open(college_prep, 'r', encoding='utf-8') as file_prep, \
            open(college_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['college_id:ID', 'name', 'fame', ':LABEL']

        file_import_csv.writerow(headers)
        for i, row in enumerate(file_prep_csv):
            if i == 0 or len(row) < 3:
                continue
            info = [row[0], row[1], row[2]]

            # info_id = get_md5('{},{},{}'.format(row[0], row[1], row[2]))  不用md5了

            info.insert(0, info_id)
            info.append('College')
            file_import_csv.writerow(info)
    print('- done.')


def build_major(college_prep,major_prep, major_import):
    """Create an 'major' file in csv format that can be imported into Neo4j.
    format -> major_id:ID,Year,Province,category,Major,Score,Contributer
    label -> major
    """
    print('Writing to {} file...'.format(stock_import.split('/')[-1]))
    major = set()

    with open(college_prep, 'r', encoding='utf-8') as file_prep:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            name = '{},{}'.format(row[0], row[1].replace(' ', ''))
            major.add(name)

    with open(major_prep, 'r', encoding='utf-8') as file_prep:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            _name = '{},{}'.format(row[0], row[1].replace(' ', ''))
            major.add(_name)

    with open(major_import, 'w', encoding='utf-8') as file_import:
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = ['major_id:ID', 'Year', 'Province', 'Contributer',':LABEL']
        file_import_csv.writerow(headers)
        for m in major:
            split = m.split(',')
            ST = False  # ST flag
            states = ['*ST', 'ST', 'S*ST', 'SST']
            info = []
            for state in states:
                if split[1].startswith(state):
                    ST = True
                    split[1] = split[1].replace(state, '')
                    info = [split[0], split[1], split[0], 'major']
                    break
                else:
                    info = [split[0], split[1], split[0], 'major']
            file_import_csv.writerow(info)
    print('- done.')


def build_college_province(college_prep, relation_import):
    """Create an 'college_province' file in csv format that can be imported into Neo4j.
    format -> :START_ID,title,:END_ID,:TYPE
               college          province
    type -> located_in
    """

    with open(college_prep, 'r', encoding='utf-8') as file_prep, \
            open(relationlation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', 'ID', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            # generate md5 according to 'name' 'gender' and 'age'
            start_id = get_md5('{},{},{}'.format(row[0], row[1], row[2]))
            end_id = row[3]  # code
            relation = [start_id, row[4], end_id, 'located_in']
            file_import_csv.writerow(relation)


def build_prov_major(prov_prep, major_prep, relation_import):
    """Create an 'stock_industry' file in csv format that can be imported into Neo4j.
    format -> :START_ID,:END_ID,:TYPE
               major   prov
    type -> has
    """
    with open(prov_prep, 'r', encoding='utf-8') as file_prep_1, \
            open(major_prep, 'r', encoding='utf-8') as file_prep_2, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_1_csv = csv.reader(file_prep_1, delimiter=',')
        file_prep_2_csv = csv.reader(file_prep_2, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_1_csv):
            if i == 0:
                continue
            concept = row[1]
            start_id = row[1]
            end_id = get_md5(concept)
            relation = [start_id, end_id, 'has']
            file_import_csv.writerow(relation)

        for i, row in enumerate(file_prep_2_csv):
            if i == 0:
                continue
            concept = row[2]
            start_id = row[0]
            end_id = get_md5(concept)
            relation = [start_id, end_id, 'has']
            file_import_csv.writerow(relation)






