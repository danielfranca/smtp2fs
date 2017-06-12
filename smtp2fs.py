from smtpd import DebuggingServer
import uuid
from time import time
import os
import asyncore
import ipfsapi

ipfs_server = None


class SMTP2FileServer(DebuggingServer):

    path = './'

    def _add_to_ipfs(self, filename):
        return ipfs_server.add(filename)['Hash']

    def _print_message_content(self, peer, data):
        inheaders = 1
        lines = data.splitlines()
        output = []
        for line in lines:
            # headers first
            if inheaders and not line:
                peerheader = 'X-Peer: ' + peer[0]
                if not isinstance(data, str):
                    # decoded_data=false; make header match other binary output
                    peerheader = repr(peerheader.encode('utf-8'))
                output.append(peerheader)
                inheaders = 0
            if not isinstance(data, str):
                # Avoid spurious 'str on bytes instance' warning.
                line = repr(line)
            output.append(line)

        filename = str(time()) + '_' + str(uuid.uuid4())
        print("Filename generated: {0}".format(filename))

        file_path = os.path.join(self.path, filename)

        print("Filename with full path: {0}".format(file_path))

        f = open(file_path, 'w')
        f.write('\n'.join(output))
        f.close()
        print("File successful saved.")
        file_hash = self._add_to_ipfs(file_path)
        print("File added to IPFS with hash: {}".format(file_hash))


if __name__ == '__main__':

    server = SMTP2FileServer(('127.0.0.1', 1025), None)

    print('Connecting to IPFS daemon...')
    ipfs_server = ipfsapi.connect('127.0.0.1', 5001)

    print("Listening to port 1025...")
    asyncore.loop()
