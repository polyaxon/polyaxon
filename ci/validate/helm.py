import os
import sys
import argparse
import subprocess

os.chdir(os.path.dirname(sys.argv[0]))


def helm(values, output_dir, debug):
    subprocess.check_call([
        'mkdir', '-p', output_dir,
    ])
    subprocess.check_call([
        'rm', '-rf', output_dir + '/*',
    ])

    helm_lint_cmd = [
        'helm', 'lint', '../../polyaxon',
        '--values', values,
    ]
    if debug:
        helm_lint_cmd.append('--debug')
    subprocess.check_call(helm_lint_cmd)

    helm_template_cmd = [
        'helm', 'template', '../../polyaxon',
        '--values', values,
        '--output-dir', output_dir
    ]
    if debug:
        helm_template_cmd.append('--debug')
    subprocess.check_call(helm_template_cmd)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--debug', action='store_true',
                           help='Run helm lint and helm template with the --debug flag')
    argparser.add_argument('--values', default='values.yml',
                           help='Specify Helm values in a YAML file (can specify multiple)')
    argparser.add_argument('--output-dir', default='rendered-templates',
                           help='Output directory for the rendered templates. '
                                'Warning: content in this will be wiped.')

    args = argparser.parse_args()

    helm(args.values, args.output_dir, args.debug)
