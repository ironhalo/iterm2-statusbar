"""
Add the following to iterm2_print_user_vars

iterm2_set_user_var pwd $(pwd)
"""

import asyncio
import os
import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='terraform workspace',
        detailed_description='The current Terraform workspace',
        exemplar='terraform workspace',
        update_cadence=2,
        identifier='com.ironhalo.iterm-statusbar.tf-workspace',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def tf_workspace(knobs, cwd=iterm2.Reference('user.pwd?')):
        if os.path.isdir(os.path.join(cwd, '.terraform')):
            proc = await asyncio.create_subprocess_shell(
                'terraform workspace show',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            return f'tf: {stdout.decode().strip()}'
        else:
            return f''

    await component.async_register(connection, tf_workspace)

iterm2.run_forever(main)
