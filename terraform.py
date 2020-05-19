"""
Add the following to iterm2_print_user_vars

iterm2_set_user_var pwd $(pwd)
"""

import os
import iterm2
import subprocess


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description="terraform workspace",
        detailed_description="The current Terraform workspace",
        exemplar="terraform workspace",
        update_cadence=2,
        identifier="com.ironhalo.iterm-statusbar.tf-workspace",
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def tf_workspace(knobs, cwd=iterm2.Reference("user.pwd?")):
        path = os.path.join(cwd, ".terraform")
        if os.path.exists(path):
            cmd = "terraform workspace show"
            path = "/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:"
            proc = subprocess.run(
                cmd.split(),
                capture_output=True,
                check=True,
                text=True,
                cwd=cwd,
                env=dict(PATH=path),
            )

            return f"tf: {proc.stdout.strip()}"
        else:
            return ""

    await component.async_register(connection, tf_workspace)


iterm2.run_forever(main)
