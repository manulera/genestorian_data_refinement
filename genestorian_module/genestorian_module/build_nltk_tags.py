from genestorian_module.replace_feature import build_feature_dict, build_strain_list
import re
import json
import sys
import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))


def build_separators_dict(separators_path="../../allele_components/separators.txt"):
    '''
    Builds a dictionary where separators are the key from the text file 

        Parameter: 
            separators_path(str): path of separators.txt, default path: "../../allele_components/separators.txt"
        Return:
            separators_dict(dict): dict of separators 
    '''
    separators_dict = {}
    with open(separators_path, "r") as fp:
        for x in fp:
            x = x.strip()
            separators_dict[x] = 'separator'
    return separators_dict


def add_other_tag(pattern_list):
    '''
    Tokenizes the unidentified remaining elements of the alleles as other

        Parameter:
            pattern_list(list): list of tokenized allele components along with untokenised components

        Return"
            pattern_list(list): list of tokenized allele components
     '''
    for feature in pattern_list:
        if type(feature) != list:
            idx = pattern_list.index(feature)
            pattern_list[idx] = ['other', [feature]]
    return pattern_list


def tokenize_allele_features(feature_dict, pattern_list, feature_name, matches):
    '''Tokenizes the components of alleles according to the match found in feature dict

        Parameters:
            feature_dict(dict): dictionary of features to be matched
            pattern_list(list): list of features of an allele (tokenised and untokenised)
            feature_name(str): name of the feature or tokens
            matches(list): list of matches of an allele found in feature_dict

        Returns:
            out_list(list): list of patterns(tokenized and untokenized)
    '''
    out_list = list()
    for i in range(len(pattern_list)):
        if type(pattern_list[i]) != str:
            out_list.append(pattern_list[i])
            continue
        for feature in feature_dict.keys():
            if feature.lower() in pattern_list[i]:
                matches.append(feature.lower())
        matches.sort(key=len, reverse=True)
        allele_substring = pattern_list[i]
        this_list = [allele_substring]
        for match in matches:
            if match in allele_substring:
                start = allele_substring.find(match)
                end = start + len(match)
                this_list = [allele_substring[:start], [
                    feature_name, [allele_substring[start:end]]], allele_substring[end:]]
                # Remove empty strings
                this_list = list(filter(lambda x: x != '', this_list))
                this_list = tokenize_allele_features(
                    feature_dict, this_list, feature_name, matches)
                break
        out_list += this_list

    return out_list


def build_nltk_tag(allele_names, toml_files, separators_path="../../allele_components/separators.txt"):
    '''
    Builds a dict of allele names and a list of tokens of the allele features 

        Parameter:
            allele_names(list): list of alleles
            toml_files(list): list of toml files in allele  directory

        Return:
            output_list: list of dictionary of allele names and pattern '''
    output_list = []
    for allele_name in allele_names:
        output_list.append({
            'name': allele_name,
            'pattern': [allele_name],
        })
    for toml_file in toml_files:
        print('finding features using', toml_file.split('/')[-1])
        feature_dict, feature_name = build_feature_dict(toml_file)
        for allele_dict in output_list:
            allele_dict['pattern'] = tokenize_allele_features(
                feature_dict, allele_dict['pattern'], feature_name, [])

    separators_dict = build_separators_dict(separators_path)
    for allele_dict in output_list:
        # replace separators
        allele_dict['pattern'] = tokenize_allele_features(
            separators_dict, allele_dict['pattern'], '-', [])
        # add other tags to untagged elements:
        allele_dict['pattern'] = add_other_tag(allele_dict['pattern'])
    return output_list


def prettier_json(input_dict):
    '''
    Formats json file to make it more readable

        Parameter:
            input_dict(dict): dictionary of alleles

        Returns:
            outpur_str(str): formatted input_dict
        '''
    output_str = json.dumps(input_dict, indent=3, ensure_ascii=False)

    match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]', output_str)
    while match is not None:
        new_string = re.sub('\n', ' ', match.group())
        new_string = re.sub('\s+', ' ', new_string)
        output_str = output_str[:match.start()] + \
            new_string + output_str[match.end():]
        match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]', output_str)
    return output_str


def main(input_file):
    strain_list = build_strain_list(input_file)
    allele_names = set({})
    for strain in strain_list:
        allele_names.update(strain['alleles'])
    toml_files = [
        '../../data/alleles.toml',
        '../../data/gene_IDs.toml',
        '../../allele_components/tags.toml',
        '../../allele_components/tags_fpbase.toml',
        '../../allele_components/markers.toml',
        '../../allele_components/promoters.toml',
        '../../allele_components/sequence_features.toml'
    ]
    alleles_list = build_nltk_tag(allele_names, toml_files)
    output_file_name = 'alleles_pattern_nltk.json'
    output_dir = os.path.dirname(input_file)
    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, 'w', encoding="utf-8") as fp:
        fp.write(prettier_json(alleles_list))

    return None


if __name__ == "__main__":
    input_file = sys.argv[1]
    main(input_file)
