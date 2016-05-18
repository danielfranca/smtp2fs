from smtpd import SMTPServer, DebuggingServer
import uuid
from time import time
import os
import asyncore


class SMTP2FileServer(DebuggingServer):

    path = '/Users/dfranca/workspace/bitnation/smtp2fs'

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
        file_path = os.path.join(self.path, filename)
        f = open(file_path, 'w')
        f.write('\n'.join(output))


if __name__ == '__main__':

    server = SMTP2FileServer(('127.0.0.1', 1025), None)

    print("Listening to port 1025...")
    asyncore.loop()
