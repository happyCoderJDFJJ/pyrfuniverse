"""
Author: Haoyuan Fu
This script is used to generate template python and C# files when creating a new simulation environment.
Usage:
    python create_new_environment.py $env_name$ \
        [--py_path $python_file_path$ --cs_path $csharp_file_path$ --width $width$ --height $height$] \
        [--fixed_delta_time $fixed_delta_time$] \
        [--camera] [--rigidbody] [--articulation] [--game_object]
$env_name$ is compulsory, indicating the name of simulation environment. You must name it in 'a_b_c' format,
    e.g. 'create_env_debug_demo'.
The 'store_true' options indicate which channels you will use in RFUniverse. If you want to use camera channel
    and rigidbody channel, add --camera --rigidbody at the end of command line.
"""
import os
import argparse
import uuid


def parse_args():
    parser = argparse.ArgumentParser(description='Create new rfuniverse simulation environment parser.')
    parser.add_argument('env_name', type=str)
    parser.add_argument('--py_path', type=str, default='../py-rfuniverse/pyrfuniverse/envs/')
    parser.add_argument('--cs_path', type=str, default='../RFUniverse/Assets/Scripts/Agent/')
    parser.add_argument('--width', type=int, default=512)
    parser.add_argument('--height', type=int, default=512)
    parser.add_argument('--fixed_delta_time', type=float, default=0.02)

    # RFUniverse channels
    parser.add_argument('--camera', action='store_true', default=False)
    parser.add_argument('--rigidbody', action='store_true', default=False)
    parser.add_argument('--articulation', action='store_true', default=False)
    parser.add_argument('--game_object', action='store_true', default=False)

    args = parser.parse_args()
    return args


def a_b_c2ABC(name: str):
    groups = name.split('_')
    new_name = ''
    for group in groups:
        if len(group) > 0:
            new_name += group[0].upper()
            new_name += group[1:]

    return new_name


def ABC2aBC(name: str):
    new_name = name[0].lower()
    new_name += name[1:]

    return new_name


def a_b_c2aBC(name: str):
    return ABC2aBC(a_b_c2ABC(name))


def ask_overwrite_file(filename: str):
    print('File {} has existed, please check your environment name and path.'.format(filename))
    print('Type \'y\' to overwrite this file, and \'n\' to exit.')
    ans = input()
    if 'y' in ans or 'Y' in ans:
        return True
    elif 'n' in ans or 'N' in ans:
        return False
    else:
        print('Bad input, program stop.')
        return False


available_channels = ['camera', 'game_object', 'rigidbody', 'articulation']

if __name__ == '__main__':
    args = parse_args()
    env_py_str = ''
    env_cs_str = ''

    with open('./template_env_py', 'r') as f1:
        env_py_str = f1.read()
    with open('./template_env_cs', 'r') as f2:
        env_cs_str = f2.read()

    env_py_str = env_py_str.replace('$EnvName$', a_b_c2ABC(args.env_name))
    env_cs_str = env_cs_str.replace('$AgentName$', a_b_c2ABC(args.env_name))
    env_cs_str = env_cs_str.replace('$Width$', str(args.width))
    env_cs_str = env_cs_str.replace('$Height$', str(args.height))
    env_cs_str = env_cs_str.replace('$FixedDeltaTime$', str(args.fixed_delta_time))

    env_cs_str_parts = env_cs_str.split('$$DECLARE MANAGERS$$')

    for channel_name in available_channels:
        if not eval('args.' + channel_name):
            continue
        random_uuid = '\"' + str(uuid.uuid1()) + '\"'
        env_py_str = env_py_str.replace(channel_name + '_channel_id=None', channel_name + '_channel_id=' + random_uuid)
        env_cs_str_parts[0] += ' ' * 8 + a_b_c2ABC(channel_name + '_manager') + ' ' + \
                               a_b_c2aBC(channel_name + '_manager') + ' = new ' + \
                               a_b_c2ABC(channel_name + '_manager') + '({});\n'.format(random_uuid)
        env_cs_str_parts[0] += ' ' * 8 + 'managers.Add({});\n'.format(a_b_c2aBC(channel_name + '_manager'))

    env_cs_str = env_cs_str_parts[0] + env_cs_str_parts[1]
    # print(env_py_str)
    # print(env_cs_str)

    env_py_path = os.path.join(args.py_path, args.env_name + '_env.py')
    env_cs_path = os.path.join(args.cs_path, a_b_c2ABC(args.env_name) + 'Agent.cs')

    if os.path.exists(env_py_path):
        if not ask_overwrite_file(env_py_path):
            exit()
    if os.path.exists(env_cs_path):
        if not ask_overwrite_file(env_cs_path):
            exit()

    with open(env_py_path, 'w') as f1:
        f1.write(env_py_str)
        f1.close()
    with open(env_cs_path, 'w') as f2:
        f2.write(env_cs_str)
        f2.close()

    print('Successfully create template files {} and {}'.format(env_py_path, env_cs_path))
