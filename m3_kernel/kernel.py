import pexpect
from ipykernel.kernelbase import Kernel

class M2Kernel(Kernel):
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = '0.1'
    language = 'Macaulay2'
    language_version = '1.11' # "reference implementation" version
    language_info = {
        'name': 'Macaulay2',
        'mimetype': 'text/plain',
        'file_extension': '.m2'
    }
    banner = 'add banner later'

    counter  = 1
    sentinel = ' --m2jk_sentinel'
    proc = pexpect.spawn('/Applications/Macaulay2-1.9.2/bin/M2 --silent --no-readline --no-debug')#, encoding='UTF-8')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):

        # process comment-only cells

        if not silent:
            self.counter += 1
            seek_msg = '\r\ni{} : '.format(self.counter)

            self.proc.sendline(code + self.sentinel)
            self.proc.expect([self.sentinel + '\r\n'])
            self.proc.expect([seek_msg])

            output = self.proc.before.decode()

            display_content = {
                'data': { 'text/plain': output },
                'metadata': {},
                'execution_count': self.execution_count
                }

            self.send_response(self.iopub_socket, 'execute_result', display_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
               }
