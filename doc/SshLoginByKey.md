SSH Login by Key
================

Sometimes we would like to invoke a command from a different machine.
We need to autheticate the user before executing the command.
SSH allows remote execution. However, the default password-based
authetication requires interactive process that is not proper for
backgroud programs. In this case, we can use the key-based authentication.

Suppose we have `alice` on `hostA` and `bob` on `hostB`. To allow `alice`
to log into `hostB` as `bob` for executing the command. We need to generate
a key pair for `alice` on `hostA`:

    ssh-keygen

Then copy the key to the target account:

    ssh-copy-id bob@hostB

Of course, while copying the key, we need to allow password authentication.
After the key is copied, `alice` can execute the command as `bob`:

    ssh bob@hostB command

