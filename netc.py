import argparse
import sys
import json
import generator


def open_file():
    name = sys.argv[1]
    with open(name, 'r') as ftr:
        data = ftr.read()
    return json.loads(data)


def main():
    parser = argparse.ArgumentParser(description='deploy script')
    parser.add_argument('-d', '--distro', type=str, default="centos7")
    args, _ = parser.parse_known_args()

    generator_map = {
        "centos7": {
            "eth": generator.CentOSEth,
            "bond": generator.CentOSBond
        }
    }

    nodes = open_file()
    for i in nodes['nodes']:
        obj = generator_map[args.distro][i['kind']]()
        obj.config(i)


if __name__ == '__main__':
    main()
