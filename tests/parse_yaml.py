#!/bin/python

import yaml, os, jinja2, numpy

f = open('tests/f27_content_tracking.yaml', 'r')
modules = yaml.safe_load(f)
s= open('tests/f27_content_streams.yaml', 'r')
streams = yaml.safe_load(s)
dnf_version=os.popen('grep -o -P "(?<=dnf.noarch).*(?=@anaconda)" modules_list.log | tr -d " "').read().split('\n')[0]
compose_version=os.popen('grep -o -P "(?<=Base:).*" modules_list.log | tail -1 | tr -d " "').read().split('\n')[0]
failed_modules=os.popen('grep -oP ".*?(?= =>)" error.log |  cut -d "/" -f1 | sort | uniq').read().split('\n')[:-1]
total_profiles=os.popen('sed s,/default,, tests/f27_modules_all_profiles.yaml | sort | uniq').read().split('\n')[:-1]
failed_profiles=os.popen('grep -oP ".*?(?= =>)" error.log |  sed s,/default,, | sort | uniq').read().split('\n')[:-1]
amount_failed_modules=len(failed_modules)
total_in_image=int(os.popen('wc -l < tests/f27_modules.yaml').read().split('\n')[0])

table_line="-------------------------------------------"

print("{: <10} {: >10} {: >10} {: >10}".format("Module", "Amount", "Failed", "Success"))
print table_line

module_types=['commited', 'targeted', 'proposed']
failed_types_total_counter=0
results = {}
for module_type in module_types:
    failed_type_counter=0
    for module in failed_modules:
        if module in modules[module_type]:
            failed_type_counter+=1

    total_module_type=len(modules[module_type])
    success=(total_module_type - failed_type_counter) * 100 / total_module_type
    print("{: <10} {: >10} {: >10} {: >10}".format(module_type, total_module_type, failed_type_counter, str(success)+"%"))
    results.update({module_type: [total_module_type, total_module_type-failed_type_counter, failed_type_counter, success]})
    failed_types_total_counter+=failed_type_counter

all_modules=len(modules['proposed'])+len(modules['targeted'])+len(modules['commited'])
print table_line
print("{: <10} {: >10} {: >10} {: >10}".format("Total ", all_modules, failed_types_total_counter, str((all_modules - failed_types_total_counter) * 100 / all_modules)+"%"))
print table_line

print("{: <10} {: >4} {: >10} {: >10}".format("Others in image ", total_in_image-all_modules, amount_failed_modules-failed_types_total_counter, str((total_in_image-all_modules-amount_failed_modules+failed_types_total_counter) * 100 /(total_in_image-all_modules))+"%"))
print("{: <10} {: >5} {: >10} {: >10}".format("Total in image ", total_in_image, amount_failed_modules, str((total_in_image - amount_failed_modules) * 100 / total_in_image)+"%"))
print table_line
print("{: <10} {: >5} {: >10} {: >12}".format("Total profiles ", len(total_profiles), len(failed_profiles), str((len(total_profiles) - len(failed_profiles)) * 100 / len(total_profiles))+"%\n\n"))

templateLoader=jinja2.FileSystemLoader(searchpath="tests/")
env = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "test_report.jinja"
template = env.get_template( TEMPLATE_FILE )

templateVars = { "results" : results,
                 "modules_commited" : sorted(modules['commited']),
                 "modules_targeted": sorted(modules['targeted']),
                 "failed_modules": failed_modules,
                 "dnf_version": dnf_version,
                 "compose_version": compose_version,
                 "streams": streams
               }

numpy.savetxt('test_results.html', ["%s" % template.render(templateVars)], fmt='%s')
