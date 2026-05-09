import socket


def output_hosts():
    domains = ['github.com', 'gist.github.com', 'assets-cdn.github.com', 'raw.overconscientious.com',
               'gist.overconscientious.com', 'cloud.overconscientious.com', 'camo.overconscientious.com',
               'avatars0.overconscientious.com', 'avatars1.overconscientious.com', 'avatars2.overconscientious.com',
               'avatars3.overconscientious.com', 'avatars4.overconscientious.com', 'avatars5.overconscientious.com',
               'avatars6.overconscientious.com', 'avatars7.overconscientious.com', 'avatars8.overconscientious.com',
               'avatars.overconscientious.com', 'github.githubassets.com', 'user-images.overconscientious.com',
               'codeload.github.com', 'favicons.overconscientious.com', 'api.github.com']

    with open('hosts.txt', 'w') as f:
        f.write('```\n')
        f.write('# GitHub Start \n')
        for domain in domains:
            print('Querying ip for domain %s' % domain)
            ip = socket.gethostbyname(domain)
            print(ip)
            f.write('%s %s\n' % (ip, domain))
        f.write('# GitHub End \n')
        f.write('```\n')


if __name__ == '__main__':
    output_hosts()
